from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.database import engine


router = APIRouter(
    prefix="/api/admin/rag",
    tags=["admin - RAG / AI"]
)


# =========================================================
# 1. AI Provider 목록
# GET /api/admin/rag/providers
# =========================================================
@router.get("/providers")
def get_ai_providers():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM ai_providers
                ORDER BY provider_id
            """)
        )

        rows = result.mappings().all()

    return {
        "count": len(rows),
        "data": [dict(row) for row in rows]
    }


# =========================================================
# 2. RAG 문서 목록
# GET /api/admin/rag/documents
# =========================================================
@router.get("/documents")
def get_rag_documents():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM rag_documents
                ORDER BY document_id DESC
            """)
        )

        rows = result.mappings().all()

    return {
        "count": len(rows),
        "data": [dict(row) for row in rows]
    }


# =========================================================
# 3. RAG 문서 상세
# GET /api/admin/rag/documents/{document_id}
#
# 조회 범위
# rag_documents
#   ├─ rag_document_files → file_assets
#   ├─ rag_chunks
#   └─ rag_chunks → rag_embeddings
# =========================================================
@router.get("/documents/{document_id}")
def get_rag_document(document_id: int):

    with engine.connect() as connection:

        # -------------------------------------------------
        # RAG 문서 기본 정보
        # -------------------------------------------------
        document_result = connection.execute(
            text("""
                SELECT *
                FROM rag_documents
                WHERE document_id = :document_id
            """),
            {
                "document_id": document_id
            }
        )

        document = document_result.mappings().first()

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="해당 RAG 문서를 찾을 수 없습니다."
            )


        # -------------------------------------------------
        # RAG Chunk 조회
        # -------------------------------------------------
        chunk_result = connection.execute(
            text("""
                SELECT *
                FROM rag_chunks
                WHERE document_id = :document_id
                ORDER BY chunk_no
            """),
            {
                "document_id": document_id
            }
        )

        chunks = chunk_result.mappings().all()


        # -------------------------------------------------
        # RAG 문서 첨부파일 조회
        #
        # rag_document_files
        #        ↓ JOIN
        # file_assets
        # -------------------------------------------------
        file_result = connection.execute(
            text("""
                SELECT
                    rdf.rag_document_file_id,
                    rdf.document_id,
                    rdf.file_id,

                    fa.original_file_name,
                    fa.public_url,
                    fa.thumbnail_url

                FROM rag_document_files rdf

                LEFT JOIN file_assets fa
                    ON rdf.file_id = fa.file_id

                WHERE rdf.document_id = :document_id

                ORDER BY rdf.rag_document_file_id
            """),
            {
                "document_id": document_id
            }
        )

        files = file_result.mappings().all()


        # -------------------------------------------------
        # RAG Embedding 조회
        #
        # rag_chunks
        #      ↓
        # rag_embeddings
        # -------------------------------------------------
        embedding_result = connection.execute(
            text("""
                SELECT
                    re.embedding_id,
                    re.chunk_id,
                    rc.document_id,
                    rc.chunk_no,

                    re.embedding_provider,
                    re.embedding_model,
                    re.embedding_dimension,
                    re.embedding_json,

                    re.vector_db_type,
                    re.vector_collection,
                    re.vector_external_id,

                    re.created_at

                FROM rag_embeddings re

                INNER JOIN rag_chunks rc
                    ON re.chunk_id = rc.chunk_id

                WHERE rc.document_id = :document_id

                ORDER BY
                    rc.chunk_no,
                    re.embedding_id
            """),
            {
                "document_id": document_id
            }
        )

        embeddings = embedding_result.mappings().all()


    return {
        "document": dict(document),

        "files": [
            dict(row)
            for row in files
        ],

        "chunks": [
            dict(row)
            for row in chunks
        ],

        "embeddings": [
            dict(row)
            for row in embeddings
        ]
    }


# =========================================================
# 4. RAG 검색 기록 목록
# GET /api/admin/rag/query-logs
# =========================================================
@router.get("/query-logs")
def get_rag_query_logs():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM rag_query_logs
                ORDER BY query_log_id DESC
            """)
        )

        rows = result.mappings().all()

    return {
        "count": len(rows),
        "data": [dict(row) for row in rows]
    }


# =========================================================
# 5. RAG 검색 기록 상세
# GET /api/admin/rag/query-logs/{query_log_id}
# =========================================================
@router.get("/query-logs/{query_log_id}")
def get_rag_query_log(query_log_id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT *
                FROM rag_query_logs
                WHERE query_log_id = :query_log_id
            """),
            {
                "query_log_id": query_log_id
            }
        )

        row = result.mappings().first()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="해당 RAG 검색 기록을 찾을 수 없습니다."
        )

    return dict(row)