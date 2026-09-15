from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.database import engine


router = APIRouter(
    prefix="/api/admin/policies",
    tags=["admin - policies"]
)


# =========================================================
# 1. 회사 정책 목록
# GET /api/admin/policies
# =========================================================
@router.get("")
def get_policies():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM company_policies
                ORDER BY policy_id
            """)
        )

        rows = result.mappings().all()

    return {
        "count": len(rows),
        "data": [dict(row) for row in rows]
    }


# =========================================================
# 2. 회사 정책 상세
# GET /api/admin/policies/{policy_id}
#
# company_policies
#       ↓
# policy_files
#       ↓ LEFT JOIN
# file_assets
# =========================================================
@router.get("/{policy_id}")
def get_policy(policy_id: int):

    with engine.connect() as connection:

        # -------------------------------------------------
        # 회사 정책 기본 정보 조회
        # -------------------------------------------------
        policy_result = connection.execute(
            text("""
                SELECT *
                FROM company_policies
                WHERE policy_id = :policy_id
            """),
            {
                "policy_id": policy_id
            }
        )

        policy = policy_result.mappings().first()

        if policy is None:
            raise HTTPException(
                status_code=404,
                detail="해당 회사 정책을 찾을 수 없습니다."
            )


        # -------------------------------------------------
        # 정책 첨부파일 조회
        #
        # policy_files
        #      ↓
        # file_assets
        # -------------------------------------------------
        file_result = connection.execute(
            text("""
                SELECT
                    pf.policy_file_id,
                    pf.policy_id,
                    pf.file_id,
                    pf.display_order,

                    fa.original_file_name,
                    fa.public_url,
                    fa.thumbnail_url

                FROM policy_files pf

                LEFT JOIN file_assets fa
                    ON pf.file_id = fa.file_id

                WHERE pf.policy_id = :policy_id

                ORDER BY
                    pf.display_order,
                    pf.policy_file_id
            """),
            {
                "policy_id": policy_id
            }
        )

        files = file_result.mappings().all()


    return {
        "policy": dict(policy),
        "files": [
            dict(row)
            for row in files
        ]
    }