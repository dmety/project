from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
import subprocess
import tempfile
import os
import time
import uuid

from app.core.database import get_db
from app.core.response import ApiResponse, success_response
from app.core.security import get_current_user
from app.schemas.tutor import (
    TutorDialogRequest,
    TutorDialogResponse,
    CodeRunRequest,
    CodeRunResponse,
    ErrorAnalysisRequest,
    ErrorAnalysisResponse,
    TutorAgentInterface
)

router = APIRouter(prefix="/tutor", tags=["智能辅导"])


def generate_tutor_answer(question: str) -> Dict[str, Any]:
    answer = f"感谢您的提问！关于 '{question}'，以下是我的解答：\n\n"
    answer += "这是一个示例回答。在实际使用中，将通过智能体或大模型生成准确的解答。\n\n"
    answer += "建议您：\n"
    answer += "1. 先理解相关知识点\n"
    answer += "2. 查看配套的学习资源\n"
    answer += "3. 完成相关练习题\n"
    answer += "4. 如有疑问，继续提问\n"
    
    return {
        "answer": answer,
        "answer_type": "text",
        "code_suggestion": None,
        "diagram_url": None,
        "related_exercises": [1, 2, 3]
    }


def run_python_code(code: str) -> Dict[str, Any]:
    start_time = time.time()
    success = False
    output = ""
    errors = ""
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file_name = f.name
        
        result = subprocess.run(
            ['python', temp_file_name],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8'
        )
        
        output = result.stdout
        errors = result.stderr
        success = result.returncode == 0
        
    except subprocess.TimeoutExpired:
        errors = "执行超时（超过10秒）"
    except Exception as e:
        errors = f"执行错误: {str(e)}"
    finally:
        try:
            os.unlink(temp_file_name)
        except:
            pass
    
    execution_time = time.time() - start_time
    
    return {
        "success": success,
        "output": output,
        "errors": errors,
        "execution_time": execution_time
    }


@router.post("/dialog", response_model=ApiResponse[TutorDialogResponse])
def tutor_dialog(
    request: TutorDialogRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    conversation_id = request.conversation_id or str(uuid.uuid4())
    answer_data = generate_tutor_answer(request.question)
    
    return success_response(
        data=TutorDialogResponse(
            conversation_id=conversation_id,
            answer=answer_data["answer"],
            answer_type=answer_data["answer_type"],
            code_suggestion=answer_data["code_suggestion"],
            diagram_url=answer_data["diagram_url"],
            related_exercises=answer_data["related_exercises"]
        )
    )


@router.post("/code/run", response_model=ApiResponse[CodeRunResponse])
def run_code(
    request: CodeRunRequest,
    current_user = Depends(get_current_user)
):
    result = run_python_code(request.code_content)
    
    return success_response(
        data=CodeRunResponse(
            success=result["success"],
            output=result["output"],
            errors=result["errors"],
            execution_time=result["execution_time"]
        )
    )


@router.post("/error/analysis", response_model=ApiResponse[ErrorAnalysisResponse])
def analyze_error(
    request: ErrorAnalysisRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return success_response(
        data=ErrorAnalysisResponse(
            error_type="概念理解错误",
            knowledge_point="知识点ID: 1",
            correct_answer="正确答案示例",
            explanation="这是错误解析示例。在实际使用中，将通过智能体分析您的错误原因。",
            similar_exercises=[4, 5, 6]
        )
    )


@router.post("/agent/call", response_model=ApiResponse[Dict[str, Any]])
def call_tutor_agent(
    request: TutorAgentInterface,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if request.enable_agent:
        return success_response(
            data={
                "message": "智能辅导智能体调用入口已预留",
                "agent_type": request.agent_type,
                "status": "pending_implementation"
            }
        )
    else:
        return success_response(
            data={
                "message": "智能体未启用，使用基础答疑逻辑",
                "status": "using_basic_logic"
            }
        )
