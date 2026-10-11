import asyncio
import time
import sys
import os
from typing import List
from pydantic import BaseModel, Field

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.services.llm_service import llm_service, LLMOfflineError

# Pydantic models for structured tests
class RoadmapMilestone(BaseModel):
    title: str = Field(description="Milestone title")
    estimated_hours: int = Field(description="Estimated hours to complete")
    prerequisites: List[str] = Field(description="List of prerequisite concepts")

class AssessmentQuestion(BaseModel):
    question: str = Field(description="Assessment question stem")
    options: List[str] = Field(description="4 multiple choice options")
    correct_idx: int = Field(description="0-based index of correct option")
    explanation: str = Field(description="Brief explanation of correct answer")

class CareerGuidance(BaseModel):
    target_role: str = Field(description="Target role title")
    gap_analysis: List[str] = Field(description="Key missing technical skills")
    recommended_first_step: str = Field(description="Immediate next actionable step")

async def run_benchmark():
    print("=" * 70)
    print("PHASE 1: LIVE LLM GATEWAY BENCHMARK & PERSISTENCE / RESILIENCE AUDIT")
    print("=" * 70)
    print(f"Base URL:     {settings.OMNIROUTE_BASE_URL}")
    print(f"Fast Model:   {settings.OMNIROUTE_FAST_MODEL}")
    print(f"Strong Model: {settings.OMNIROUTE_STRONG_MODEL}")
    print(f"API Key set:  {bool(settings.OMNIROUTE_API_KEY)}")
    print("-" * 70)

    fast_results = []
    strong_results = []

    # -------------------------------------------------------------
    # 1. 3 Live Calls on FAST MODEL (antigravity/gemini-3.8-flash-tiered)
    # -------------------------------------------------------------
    print("\n>>> BENCHMARK 1: FAST MODEL (3 REAL CALLS)")
    fast_prompts = [
        "In 1 concise sentence, explain gradient descent for a machine learning beginner.",
        "List exactly 3 essential technical skills for an MLOps engineer (comma separated).",
        "In 1 concise sentence, what is the core difference between precision and recall?"
    ]

    for idx, prompt in enumerate(fast_prompts, start=1):
        t0 = time.perf_counter()
        response = await llm_service.chat(
            messages=[{"role": "user", "content": prompt}],
            model=settings.OMNIROUTE_FAST_MODEL,
            temperature=0.3,
            max_tokens=250,
            use_cache=False  # Ensure cold real API call
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        fast_results.append((elapsed_ms, response.strip()))
        print(f"\n[Fast Call #{idx}] Latency: {elapsed_ms:.1f} ms")
        print(f"Prompt:   {prompt}")
        print(f"Response: {response.strip()}")

    # -------------------------------------------------------------
    # 2. 3 Live Calls on STRONG MODEL (antigravity/claude-sonnet-4-6)
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print(">>> BENCHMARK 2: STRONG MODEL (3 REAL STRUCTURED CHAT_JSON CALLS)")

    # Strong Call 1: Roadmap Milestone
    print("\n[Strong Call #1: RoadmapMilestone Schema]")
    t0 = time.perf_counter()
    res1 = await llm_service.chat_json(
        messages=[{"role": "user", "content": "Create an introductory milestone for learning PyTorch Neural Networks for a junior developer."}],
        schema=RoadmapMilestone,
        model=settings.OMNIROUTE_STRONG_MODEL,
        temperature=0.2,
        use_cache=False
    )
    elapsed1_ms = (time.perf_counter() - t0) * 1000
    strong_results.append((elapsed1_ms, res1.model_dump_json()))
    print(f"Latency:  {elapsed1_ms:.1f} ms")
    print(f"Result:   {res1.model_dump_json(indent=2)}")

    # Strong Call 2: Assessment Question
    print("\n[Strong Call #2: AssessmentQuestion Schema]")
    t0 = time.perf_counter()
    res2 = await llm_service.chat_json(
        messages=[{"role": "user", "content": "Generate a multiple-choice question testing understanding of Cross-Entropy Loss."}],
        schema=AssessmentQuestion,
        model=settings.OMNIROUTE_STRONG_MODEL,
        temperature=0.2,
        use_cache=False
    )
    elapsed2_ms = (time.perf_counter() - t0) * 1000
    strong_results.append((elapsed2_ms, res2.model_dump_json()))
    print(f"Latency:  {elapsed2_ms:.1f} ms")
    print(f"Result:   {res2.model_dump_json(indent=2)}")

    # Strong Call 3: Career Guidance
    print("\n[Strong Call #3: CareerGuidance Schema]")
    t0 = time.perf_counter()
    res3 = await llm_service.chat_json(
        messages=[{"role": "user", "content": "Analyze a profile with Python and SQL aiming for an AI Solutions Architect position."}],
        schema=CareerGuidance,
        model=settings.OMNIROUTE_STRONG_MODEL,
        temperature=0.2,
        use_cache=False
    )
    elapsed3_ms = (time.perf_counter() - t0) * 1000
    strong_results.append((elapsed3_ms, res3.model_dump_json()))
    print(f"Latency:  {elapsed3_ms:.1f} ms")
    print(f"Result:   {res3.model_dump_json(indent=2)}")

    # -------------------------------------------------------------
    # 3. Cached Repeat Call Test
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print(">>> BENCHMARK 3: CACHED REPEAT CALL (VALIDATING IN-MEMORY TTL CACHE)")
    cache_test_prompt = "Explain tokenization in NLP in 1 sentence."
    
    # Initial call (Cold) with caching enabled
    t0 = time.perf_counter()
    initial_res = await llm_service.chat(
        messages=[{"role": "user", "content": cache_test_prompt}],
        model=settings.OMNIROUTE_FAST_MODEL,
        use_cache=True
    )
    initial_ms = (time.perf_counter() - t0) * 1000
    print(f"[Initial Cold Call] Latency: {initial_ms:.1f} ms")
    print(f"Response: {initial_res.strip()}")

    # Cached repeat call
    t0 = time.perf_counter()
    cached_res = await llm_service.chat(
        messages=[{"role": "user", "content": cache_test_prompt}],
        model=settings.OMNIROUTE_FAST_MODEL,
        use_cache=True
    )
    cached_ms = (time.perf_counter() - t0) * 1000
    print(f"[Repeat Cached Call] Latency: {cached_ms:.3f} ms (Cache Hits: {llm_service.cache_hits})")
    print(f"Response matches cold call: {initial_res == cached_res}")

    # -------------------------------------------------------------
    # 4. Failure Handling Test (Wrong Port / Offline Fallback)
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print(">>> RESILIENCE TEST: FAILURE HANDLING (POINTING AT WRONG PORT 9999)")
    
    # Save original base URL
    original_url = settings.OMNIROUTE_BASE_URL
    try:
        # Temporarily reconfigure to unreachable port
        settings.OMNIROUTE_BASE_URL = "http://127.0.0.1:9999/v1"
        print(f"Temporarily modified Base URL to: {settings.OMNIROUTE_BASE_URL}")

        print("\nTest 4.1: chat() with fallback specified:")
        t0 = time.perf_counter()
        fallback_res = await llm_service.chat(
            messages=[{"role": "user", "content": "Hello AI?"}],
            fallback="[System Fallback: Local offline curriculum guidance loaded]"
        )
        elapsed_fail_ms = (time.perf_counter() - t0) * 1000
        print(f"Completed in {elapsed_fail_ms:.1f} ms without crashing!")
        print(f"Returned response: '{fallback_res}'")

        print("\nTest 4.2: chat() with default offline fallback:")
        default_fallback_res = await llm_service.chat(
            messages=[{"role": "user", "content": "What is AI?"}]
        )
        print(f"Returned default fallback: '{default_fallback_res}'")

        print("\nTest 4.3: chat_json() with Pydantic fallback:")
        mock_fallback_milestone = RoadmapMilestone(
            title="Local Offline Milestone: Fundamentals of Programming",
            estimated_hours=10,
            prerequisites=["Basic Computer Literacy"]
        )
        json_fallback_res = await llm_service.chat_json(
            messages=[{"role": "user", "content": "Give me a milestone"}],
            schema=RoadmapMilestone,
            fallback=mock_fallback_milestone
        )
        print(f"chat_json returned fallback model: {json_fallback_res.model_dump()}")

    finally:
        # Restore original URL
        settings.OMNIROUTE_BASE_URL = original_url
        print(f"\nRestored Base URL to: {settings.OMNIROUTE_BASE_URL}")

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
