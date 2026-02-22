#!/usr/bin/env python3
"""
NexIA AI Tool — Uses NVIDIA API for content generation
Saves Claude credits by offloading heavy tasks to free NVIDIA models
"""
import requests
import json
import sys

NVIDIA_API_KEY = "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"
BASE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Best models available
MODELS = {
    "fast": "meta/llama-3.3-70b-instruct",       # Fast, good quality
    "smart": "qwen/qwen3-235b-a22b",              # Very smart, large
    "code": "qwen/qwen2.5-coder-32b-instruct",    # Best for code
    "reason": "qwen/qwq-32b",                      # Best for reasoning
    "deepseek": "deepseek-ai/deepseek-v3.2",       # DeepSeek latest
    "mistral": "mistralai/mistral-large-3-675b-instruct-2512",  # Mistral largest
}

def ask(prompt, model="fast", system=None, max_tokens=2000):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    resp = requests.post(BASE_URL,
        headers={
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODELS.get(model, model),
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        },
        timeout=60
    )
    data = resp.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"ERROR: {data}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 nvidia-ai.py 'your prompt' [model]")
        print(f"Models: {', '.join(MODELS.keys())}")
        sys.exit(1)
    
    prompt = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "fast"
    print(ask(prompt, model))
