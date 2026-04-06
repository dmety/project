import requests
from typing import Optional, Dict, Any
from app.core.config import settings


class ContentAuditSDK:
    def __init__(
        self,
        app_id: Optional[str] = None,
        api_secret: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        self.app_id = app_id or settings.XFYUN_CONTENT_AUDIT_APP_ID
        self.api_secret = api_secret or settings.XFYUN_CONTENT_AUDIT_API_SECRET
        self.api_key = api_key or settings.XFYUN_CONTENT_AUDIT_API_KEY

    def audit_text(
        self,
        text: str,
        audit_type: str = "all"
    ) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "text": text,
            "type": audit_type
        }
        
        try:
            response = requests.post(
                "https://api.xf-yun.com/v1/private/s9a87e3ec/text/check",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            is_compliant = True
            risk_level = "low"
            
            if result.get("code") == 0:
                data = result.get("data", {})
                if data.get("is_sensitive") == 1:
                    is_compliant = False
                    risk_level = "high"
                elif data.get("is_sensitive") == 2:
                    is_compliant = False
                    risk_level = "medium"
                
                return {
                    "success": True,
                    "is_compliant": is_compliant,
                    "risk_level": risk_level,
                    "details": data,
                    "raw_response": result
                }
            else:
                return {
                    "success": False,
                    "error": result.get("message", "审核失败"),
                    "raw_response": result
                }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"请求失败: {str(e)}",
                "is_compliant": False,
                "risk_level": "high"
            }
