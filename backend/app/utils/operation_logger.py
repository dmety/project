import time
from typing import Optional
from sqlalchemy.orm import Session
from app.models import SysOperationLog


def log_operation(
    db: Session,
    user_id: Optional[int],
    role_code: Optional[str],
    module: Optional[str],
    operation_type: Optional[str],
    request_url: Optional[str],
    request_method: Optional[str],
    request_params: Optional[str],
    response_result: Optional[str],
    operation_ip: Optional[str],
    duration: int,
    status: int = 1,
    error_msg: Optional[str] = None
):
    log = SysOperationLog(
        user_id=user_id,
        role_code=role_code,
        module=module,
        operation_type=operation_type,
        request_url=request_url,
        request_method=request_method,
        request_params=request_params,
        response_result=response_result,
        operation_ip=operation_ip,
        duration=duration,
        status=status,
        error_msg=error_msg
    )
    db.add(log)
    db.commit()


class OperationLogger:
    def __init__(self, db: Session):
        self.db = db
        self.start_time = time.time()
    
    def log(
        self,
        user_id: Optional[int],
        role_code: Optional[str],
        module: Optional[str],
        operation_type: Optional[str],
        request_url: Optional[str],
        request_method: Optional[str],
        request_params: Optional[str] = None,
        response_result: Optional[str] = None,
        operation_ip: Optional[str] = None,
        status: int = 1,
        error_msg: Optional[str] = None
    ):
        duration = int((time.time() - self.start_time) * 1000)
        log_operation(
            self.db, user_id, role_code, module, operation_type,
            request_url, request_method, request_params, response_result,
            operation_ip, duration, status, error_msg
        )
