import requests
import json
from typing import Optional, Dict, Any
from app.core.config import settings


class IFlyCodeSDK:
    def __init__(
        self,
        app_id: Optional[str] = None,
        api_secret: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        self.app_id = app_id or settings.XFYUN_IFLYCODE_APP_ID
        self.api_secret = api_secret or settings.XFYUN_IFLYCODE_API_SECRET
        self.api_key = api_key or settings.XFYUN_IFLYCODE_API_KEY
        self.api_url = "https://iflycode.xf-yun.com/v1/code/generate"

    def generate_code(
        self,
        prompt: str,
        language: str = "python",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "iflycode-v1",
            "prompt": prompt,
            "language": language,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            
            if "code" in result:
                return {
                    "success": True,
                    "code": result["code"],
                    "explanation": result.get("explanation", ""),
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

    def generate_python_code(
        self,
        prompt: str,
        with_comments: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        full_prompt = prompt
        if with_comments:
            full_prompt = f"{prompt}\n请生成带有详细中文注释的Python代码。"
        
        return self.generate_code(full_prompt, language="python", **kwargs)

    def debug_code(
        self,
        code: str,
        error_message: Optional[str] = None,
        language: str = "python"
    ) -> Dict[str, Any]:
        prompt = f"请帮我调试以下{language}代码：\n\n{code}"
        if error_message:
            prompt += f"\n\n错误信息：{error_message}"
        prompt += "\n\n请提供：1. 错误原因分析 2. 修复后的代码 3. 优化建议"
        
        return self.generate_code(prompt, language=language)
