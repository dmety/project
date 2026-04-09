import json
import hmac
import hashlib
import base64
import ssl
import websocket
from datetime import datetime
from typing import Optional, List, Dict, Any
from urllib.parse import urlencode
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
        self.api_url = "wss://spark-api.xf-yun.com/v4.0/chat"  # 默认使用V4
        self.domain = "4.0Ultra"  # 对应V4版本的domain
        
        print(f"星火SDK初始化:")
        print(f"  APP_ID: {self.app_id}")
        print(f"  API_KEY: {self.api_key[:10] if self.api_key else ''}...")
        print(f"  API_URL: {self.api_url}")
        print(f"  DOMAIN: {self.domain}")

    def _generate_auth_url(self) -> str:
        """生成WebSocket鉴权URL"""
        # 生成RFC1123格式的时间戳
        date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        # 拼接signature_origin
        signature_origin = f"host: spark-api.xf-yun.com\ndate: {date}\nGET /v4.0/chat HTTP/1.1"
        
        # hmac-sha256加密
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # base64编码
        signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')
        
        # 拼接authorization_origin
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        
        # base64编码
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        
        # 构建URL参数
        params = {
            "authorization": authorization,
            "date": date,
            "host": "spark-api.xf-yun.com"
        }
        
        # 拼接URL
        auth_url = f"{self.api_url}?{urlencode(params)}"
        return auth_url

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 0.9
    ) -> Dict[str, Any]:
        """使用WebSocket调用讯飞星火大模型"""
        response_content = ""
        ws = None
        
        try:
            auth_url = self._generate_auth_url()
            print(f"鉴权URL: {auth_url[:100]}...")
            
            # 构建请求参数
            request_data = {
                "header": {
                    "app_id": self.app_id,
                    "uid": "user"
                },
                "parameter": {
                    "chat": {
                        "domain": self.domain,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "top_p": top_p
                    }
                },
                "payload": {
                    "message": {
                        "text": messages
                    }
                }
            }
            
            print(f"请求数据: {json.dumps(request_data, ensure_ascii=False)[:200]}...")
            
            # WebSocket回调
            def on_message(ws_app, message):
                nonlocal response_content
                try:
                    data = json.loads(message)
                    print(f"收到响应: {json.dumps(data, ensure_ascii=False)[:200]}...")
                    
                    code = data["header"]["code"]
                    if code != 0:
                        print(f"请求错误: {data['header']['message']}")
                        ws_app.close()
                        return
                    
                    choices = data["payload"]["choices"]
                    status = choices["status"]
                    content = choices["text"][0]["content"]
                    
                    response_content += content
                    
                    if status == 2:
                        print("响应完成")
                        ws_app.close()
                        
                except Exception as e:
                    print(f"处理响应错误: {e}")
            
            def on_error(ws_app, error):
                print(f"WebSocket错误: {error}")
            
            def on_close(ws_app, close_status_code, close_msg):
                print(f"WebSocket关闭: {close_status_code} - {close_msg}")
            
            def on_open(ws_app):
                print("WebSocket连接成功")
                ws_app.send(json.dumps(request_data))
            
            # 创建WebSocket连接
            ws = websocket.WebSocketApp(
                auth_url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.on_open = on_open
            
            # 运行WebSocket（阻塞直到完成）
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            
            if response_content:
                return {
                    "success": True,
                    "content": response_content,
                    "usage": {}
                }
            else:
                return {
                    "success": False,
                    "error": "未收到响应内容"
                }
                
        except Exception as e:
            print(f"调用异常: {e}")
            import traceback
            print(f"堆栈: {traceback.format_exc()}")
            return {
                "success": False,
                "error": f"调用异常: {str(e)}"
            }
        finally:
            if ws:
                try:
                    ws.close()
                except:
                    pass

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
