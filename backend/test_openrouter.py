import httpx

for name, key in [
    ("CHATBOX_API_KEY", "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"),
    ("OMNIROUTE_API_KEY", "sk-b97c5f1ed643d79e-56ae18-ecac5620"),
]:
    print("=" * 40)
    print("Testing:", name, "Key:", key)
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "NovaPath AI Mentor"
    }
    body = {
        "model": "meta-llama/llama-3.2-3b-instruct:free",
        "messages": [{"role": "user", "content": "Say hello in one word"}],
        "max_tokens": 10
    }
    r = httpx.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers, timeout=15.0)
    print("Status:", r.status_code)
    print("Response:", r.text)
