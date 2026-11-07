"""
SwitchMesh Universal LLM Engine.
Provides real Generative AI inference across Google Gemini, OpenAI, Anthropic, and Groq.
Allows agents to perform live dynamic reasoning, code synthesis, and problem solving.
Falls back to deterministic expert templates when no API key is configured.
"""

from __future__ import annotations
import os
import json
from typing import Optional, List, Dict
import httpx


class LLMEngine:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    def has_live_llm(self) -> bool:
        """Returns True if any real LLM API key is configured."""
        return bool(self.gemini_key or self.openai_key or self.groq_key or self.anthropic_key)

    def get_provider_name(self) -> str:
        if self.gemini_key:
            return "Google Gemini (gemini-2.0-flash)"
        if self.openai_key:
            return "OpenAI (gpt-4o-mini)"
        if self.groq_key:
            return "Groq (llama-3.3-70b-versatile)"
        if self.anthropic_key:
            return "Anthropic (claude-3-5-sonnet)"
        return "Deterministic Expert Engine (No API key set)"

    async def generate(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """
        Executes a real LLM generation call across available providers.
        """
        # 1. Google Gemini
        if self.gemini_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_key}"
                payload = {
                    "system_instruction": {"parts": [{"text": system_prompt}]},
                    "contents": [{"parts": [{"text": user_prompt}]}],
                    "generationConfig": {"temperature": 0.4, "maxOutputTokens": 1024}
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.post(url, json=payload)
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text = candidates[0]["content"]["parts"][0]["text"]
                        return text.strip()
            except Exception as e:
                print(f"⚠️ Gemini API error: {e}")

        # 2. Groq (Ultra-fast Llama 3)
        if self.groq_key:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.groq_key}"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.4,
                    "max_tokens": 1024
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.post(url, headers=headers, json=payload)
                    data = resp.json()
                    return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                print(f"⚠️ Groq API error: {e}")

        # 3. OpenAI
        if self.openai_key:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_key}"}
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.4,
                    "max_tokens": 1024
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.post(url, headers=headers, json=payload)
                    data = resp.json()
                    return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                print(f"⚠️ OpenAI API error: {e}")

        # 4. Anthropic
        if self.anthropic_key:
            try:
                url = "https://api.anthropic.com/v1/messages"
                headers = {
                    "x-api-key": self.anthropic_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                payload = {
                    "model": "claude-3-5-sonnet-20241022",
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": user_prompt}],
                    "max_tokens": 1024
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.post(url, headers=headers, json=payload)
                    data = resp.json()
                    return data["content"][0]["text"].strip()
            except Exception as e:
                print(f"⚠️ Anthropic API error: {e}")

        return None


llm_engine = LLMEngine()
