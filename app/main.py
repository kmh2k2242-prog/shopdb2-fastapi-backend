from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

# =========================================================
# Router Import
# =========================================================

# 기존 Router
from app.routers.org_units import router as org_units_router
from app.routers.payments import router as payments_router

from app.routers.refunds import (
    router as refunds_router,
    admin_router as admin_refunds_router,
    policy_router as refund_policy_router
)

from app.routers.policies import router as policies_router
from app.routers.rag import router as rag_router

# 신규 협업 Router
from app.routers.audit_logs import router as audit_logs_router
from app.routers.error_logs import router as error_logs_router
from app.routers.admin_approval_requests import router as admin_approval_requests_router
from app.routers.user_notifications import router as user_notifications_router
from app.routers.maintenance_notices import router as maintenance_notices_router


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="SHOPDB2 조별 프로젝트 API",
    version="1.0.0"
)


# =========================================================
# Router 등록
# =========================================================

# 조직
app.include_router(org_units_router)

# 결제
app.include_router(payments_router)

# 환불 신청
app.include_router(refunds_router)

# 관리자 환불 조회
app.include_router(admin_refunds_router)

# 관리자 환불 정책 조회
app.include_router(refund_policy_router)

# 회사 정책
app.include_router(policies_router)

# RAG / AI
app.include_router(rag_router)


# ---------------------------------------------------------
# 신규 협업 기능
# ---------------------------------------------------------

# 감사 로그
app.include_router(audit_logs_router)

# 오류 로그
app.include_router(error_logs_router)

# 관리자 승인 요청
app.include_router(admin_approval_requests_router)

# 사용자 알림
app.include_router(user_notifications_router)

# 서비스 점검 공지
app.include_router(maintenance_notices_router)


# =========================================================
# 기본 API
# =========================================================

@app.get("/")
def root():

    return {
        "status": "success",
        "message": "SHOPDB2 FastAPI 서버 정상 실행"
    }


# =========================================================
# DB 연결 확인
# =========================================================

@app.get("/health/db")
def health_db():

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT DATABASE()")
            )

            database_name = result.scalar()

        return {
            "status": "success",
            "database": database_name,
            "message": "DB 연결 성공"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }