import requests
import base64
from typing import Optional, Dict, Any
from app.core.config import settings


class MultimodalSDK:
    def __init__(
        self,
        app_id: Optional[str] = None,
        api_secret: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        self.app_id = app_id or settings.XFYUN_MULTIMODAL_APP_ID
        self.api_secret = api_secret or settings.XFYUN_MULTIMODAL_API_SECRET
        self.api_key = api_key or settings.XFYUN_MULTIMODAL_API_KEY

    def image_to_text(
        self,
        image_path: Optional[str] = None,
        image_base64: Optional[str] = None,
        prompt: str = "描述这张图片的内容"
    ) -> Dict[str, Any]:
        if image_path:
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode()
        
        if not image_base64:
            return {
                "success": False,
                "error": "需要提供图片路径或base64编码"
            }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "spark-v4.0",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(
                "https://spark-openai.xf-yun.com/v4/chat/completions",
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
