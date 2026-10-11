from typing import List, Dict, Any, Optional
from ..models.schemas import AssessmentQuestion, AssessmentFeedback

# Question repository organized by skill_id and difficulty
QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
    "pytorch": [
        {
            "id": "q-torch-e1",
            "skill_id": "pytorch",
            "difficulty": "Easy",
            "question": "What is the primary role of `tensor.backward()` in PyTorch?",
            "code_snippet": "loss = criterion(output, target)\nloss.backward()\noptimizer.step()",
            "options": [
                "It automatically calculates and accumulates the gradients of the loss with respect to graph leaves",
                "It zeroes out the gradients stored in model parameters",
                "It updates parameter weights using the configured learning rate",
                "It moves the tensor memory from CPU RAM to GPU VRAM"
            ],
            "correct_index": 0,
            "explanation": "Calling `loss.backward()` triggers PyTorch's reverse-mode automatic differentiation engine (`autograd`), computing d(loss)/d(param) for all parameters with `requires_grad=True`.",
            "grounded_source": "PyTorch Autograd Mechanics (Blitz Section 2)",
            "hint": "Think about what needs to happen before optimizer.step() updates weights."
        },
        {
            "id": "q-torch-m1",
            "skill_id": "pytorch",
            "difficulty": "Medium",
            "question": "Why must you invoke `optimizer.zero_grad()` before computing gradients in a training iteration?",
            "code_snippet": "for x, y in dataloader:\n    optimizer.zero_grad() # Why is this essential?\n    out = model(x)\n    loss = criterion(out, y)\n    loss.backward()",
            "options": [
                "PyTorch default behavior accumulates gradients on successive backward passes instead of overwriting them",
                "To release GPU VRAM occupied by the activation caches from forward pass",
                "To reset the model's dropout layers and batch normalization running statistics",
                "It compiles the graph into a TorchScript C++ execution plan"
            ],
            "correct_index": 0,
            "explanation": "By design, PyTorch accumulates gradients in `.grad` buffers to facilitate training patterns like gradient accumulation across mini-batches. Failing to zero gradients causes values to blow up.",
            "grounded_source": "PyTorch Optimization Recipes, torch.optim.Optimizer docs",
            "hint": "Consider what happens if multiple backward() calls occur without clearing buffers."
        },
        {
            "id": "q-torch-h1",
            "skill_id": "pytorch",
            "difficulty": "Hard",
            "question": "When training with Mixed Precision (AMP), why is `torch.cuda.amp.GradScaler` required alongside `torch.autocast`?",
            "code_snippet": "scaler = torch.cuda.amp.GradScaler()\nwith torch.autocast(device_type='cuda', dtype=torch.float16):\n    out = model(x)\n    loss = criterion(out, y)\nscaler.scale(loss).backward()\nscaler.step(optimizer)\nscaler.update()",
            "options": [
                "Small gradient magnitudes in FP16 can underflow to zero; scaling multiplies loss by a scale factor to fit FP16 dynamic range",
                "It prevents CPU-GPU memory bottlenecks by batching asynchronous DMA transfers",
                "It transforms model weights into 8-bit quantized integer integers on the fly",
                "It prevents CUDA out-of-memory errors by flushing the L2 GPU cache"
            ],
            "correct_index": 0,
            "explanation": "In 16-bit floating point, very small gradient values underflow to zero. GradScaler scales the loss upward so gradients fit into the representable dynamic range of FP16, and un-scales them before the optimizer step.",
            "grounded_source": "NVIDIA & PyTorch Mixed Precision Training Whitepaper (Micikevicius et al.)",
            "hint": "Think about the dynamic exponent range of 16-bit floats compared to 32-bit."
        },
        {
            "id": "q-torch-x1",
            "skill_id": "pytorch",
            "difficulty": "Expert",
            "question": "Under Fully Sharded Data Parallel (FSDP), what is the primary communication difference between forward pass and backward pass all-gathers?",
            "code_snippet": "model = FSDP(model, sharding_strategy=ShardingStrategy.FULL_SHARD)",
            "options": [
                "Forward pass all-gathers full weights and drops them post-computation; backward pass all-gathers weights again and executes reduce-scatter on gradients",
                "Forward pass computes everything in FP8, backward pass executes exclusively on CPU host memory",
                "FSDP duplicates 100% of weights on every rank in backward pass without gradient scatter",
                "Backward pass requires peer-to-peer ring topology without collective primitives"
            ],
            "correct_index": 0,
            "explanation": "FSDP shards model parameters, gradients, and optimizer states across ranks. In forward, it all-gathers parameters per unit, computes, and frees them. In backward, it all-gathers parameters again, computes gradients, frees parameters, and executes a reduce-scatter on gradients.",
            "grounded_source": "PyTorch Distributed FSDP Architecture Paper (Zhao et al.)",
            "hint": "Consider memory savings when sharding both parameters and gradients."
        }
    ],
    "transformers": [
        {
            "id": "q-tf-e1",
            "skill_id": "transformers",
            "difficulty": "Easy",
            "question": "What is the core purpose of Positional Encodings in the original Transformer architecture?",
            "code_snippet": "input_embeddings = token_embed(x) + positional_encoding(seq_len)",
            "options": [
                "To inject token order information into the model since self-attention is permutation-invariant",
                "To compress vocabulary token IDs into dense numerical tensors",
                "To prevent the Softmax denominator from overflowing during dot-product attention",
                "To calculate semantic cosine similarity between sentences"
            ],
            "correct_index": 0,
            "explanation": "Self-attention operations compute dot products irrespective of sequence position. Positional encodings ensure the model can distinguish 'dog bites man' from 'man bites dog'.",
            "grounded_source": "'Attention Is All You Need' (Vaswani et al., 2017)",
            "hint": "Without this, changing the order of words yields the identical attention matrix."
        },
        {
            "id": "q-tf-m1",
            "skill_id": "transformers",
            "difficulty": "Medium",
            "question": "In QLoRA parameter-efficient fine-tuning, what innovation enables fine-tuning 65B parameter models on a single 48GB GPU?",
            "code_snippet": "bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4')",
            "options": [
                "4-bit NormalFloat (NF4) quantization with Double Quantization and Paged Optimizers",
                "Pruning 70% of transformer attention heads during the first 100 iterations",
                "Distilling the teacher model into an FP16 student network before backpropagation",
                "Executing the backward pass purely in system swap RAM"
            ],
            "correct_index": 0,
            "explanation": "QLoRA introduces 4-bit NormalFloat quantization (information-theoretically optimal for zero-mean normal distributions), Double Quantization to save memory on quantization constants, and Paged Optimizers to manage memory spikes.",
            "grounded_source": "QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., 2023)",
            "hint": "Check the BitsAndBytesConfig arguments shown in the snippet."
        }
    ]
}

class AssessmentService:
    def get_questions_for_skill(self, skill_id: str) -> List[AssessmentQuestion]:
        # Normalize skill name
        key = "pytorch"
        s_lower = skill_id.lower()
        if "transform" in s_lower or "llm" in s_lower or "attention" in s_lower:
            key = "transformers"
        elif "sql" in s_lower or "data" in s_lower:
            key = "sql_data"
        elif "sec" in s_lower or "cyber" in s_lower:
            key = "security"

        raw_items = QUESTION_BANK.get(key, QUESTION_BANK["pytorch"])

        import random
        # Randomize sample and shuffle options so questions vary on every assessment
        sampled = list(raw_items)
        random.shuffle(sampled)

        result = []
        for item in sampled:
            opts = list(item["options"])
            correct_val = opts[item["correct_index"]]
            random.shuffle(opts)
            new_idx = opts.index(correct_val)
            item["current_correct_index"] = new_idx

            result.append(
                AssessmentQuestion(
                    id=item["id"],
                    skill_id=skill_id,
                    question=item["question"],
                    code_snippet=item.get("code_snippet"),
                    options=opts,
                    difficulty=item["difficulty"],
                    type="multiple_choice",
                    hint=item.get("hint")
                )
            )
        return result

    def evaluate_answer(self, question_id: str, selected_index: int, current_consecutive_correct: int) -> AssessmentFeedback:
        # Search question across banks
        target_q = None
        for bank in QUESTION_BANK.values():
            for q in bank:
                if q["id"] == question_id:
                    target_q = q
                    break
            if target_q:
                break

        if not target_q:
            target_q = QUESTION_BANK["pytorch"][0]

        correct_idx = target_q.get("current_correct_index", target_q["correct_index"])
        is_correct = (selected_index == correct_idx)
        
        # Adaptive difficulty adjustment logic
        difficulties = ["Easy", "Medium", "Hard", "Expert"]
        curr_diff = target_q["difficulty"]
        curr_idx = difficulties.index(curr_diff) if curr_diff in difficulties else 0

        if is_correct:
            new_consecutive = current_consecutive_correct + 1
            if new_consecutive >= 2 and curr_idx < len(difficulties) - 1:
                new_difficulty = difficulties[curr_idx + 1]
            else:
                new_difficulty = curr_diff
            points = (curr_idx + 1) * 50
        else:
            new_difficulty = difficulties[max(0, curr_idx - 1)]
            points = 10

        return AssessmentFeedback(
            is_correct=is_correct,
            correct_option_index=correct_idx,
            explanation=target_q["explanation"],
            grounded_source=target_q["grounded_source"],
            new_difficulty=new_difficulty,
            points_earned=points,
            current_score=points
        )

assessment_service = AssessmentService()
