import requests
import json
from typing import Optional, List, Dict, Any
from app.core.config import settings


class SparkSDK:
    def __init__(
        self,
        app_id: Optional[str] = None,
        api_secret: Optional[str] = None,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None
    ):
        self.app_id = app_id or settings.XFYUN_SPARK_APP_ID
        self.api_secret = api_secret or settings.XFYUN_SPARK_API_SECRET
        self.api_key = api_key or settings.XFYUN_SPARK_API_KEY
        self.api_url = api_url or settings.XFYUN_SPARK_V4_URL

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 0.9
    ) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "spark-v4.0",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return {
                    "success": True,
                    "content": result["choices"][0]["message"]["content"],
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "error": "响应格式错误",
                    "raw_response": result
                }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"请求失败: {str(e)}"
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"JSON解析失败: {str(e)}"
            }

    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages, **kwargs)
