import httpx

from app.core.config import get_settings


class LLMClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        if self.settings.llm_provider == "ollama":
            return self._ollama_generate(prompt, max_tokens=max_tokens, temperature=temperature)
        return self._hf_generate(prompt, max_tokens=max_tokens, temperature=temperature)

    def _hf_generate(self, prompt: str, max_tokens: int, temperature: float) -> str:
        headers = {}
        if self.settings.hf_api_token:
            headers["Authorization"] = f"Bearer {self.settings.hf_api_token}"
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False,
            },
        }
        url = f"https://api-inference.huggingface.co/models/{self.settings.hf_model}"
        response = httpx.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return data[0].get("generated_text", "").strip()
        if isinstance(data, dict) and "generated_text" in data:
            return str(data["generated_text"]).strip()
        return str(data)

    def _ollama_generate(self, prompt: str, max_tokens: int, temperature: float) -> str:
        payload = {
            "model": self.settings.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": temperature},
        }
        url = f"{self.settings.ollama_base_url}/api/generate"
        response = httpx.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return str(data.get("response", "")).strip()
