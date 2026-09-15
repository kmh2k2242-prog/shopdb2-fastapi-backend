# SHOPDB2 FastAPI Backend

MySQL 기반 쇼핑몰 DB `shopdb2`와 FastAPI를 연동하여  
결제·환불·회사 정책·RAG/AI 및 관리자 운영 기능을 구현한 조별 프로젝트입니다.

## 1. 기술 스택

- Python
- FastAPI
- MySQL
- SQLAlchemy
- Uvicorn
- uv
- DBeaver
- Swagger UI
- Git / GitHub

## 2. 프로젝트 구조

```text
app/
├── main.py
├── database.py
├── routers/
│   ├── org_units.py
│   ├── payments.py
│   ├── refunds.py
│   ├── policies.py
│   ├── rag.py
│   ├── audit_logs.py
│   ├── error_logs.py
│   ├── admin_approval_requests.py
│   ├── user_notifications.py
│   └── maintenance_notices.py
└── schemas/
    └── refunds.py
```

## 3. 주요 구현 기능

### 결제 관리

- 결제 목록 조회
- 결제 상세 조회
- 결제 트랜잭션 및 Webhook 정보 연동

### 환불 관리

- 환불 신청
- 환불 목록 조회
- 환불 상세 조회
- 환불 정책 조회

### 회사 정책 관리

- 회사 정책 목록 조회
- 회사 정책 상세 조회
- 정책 첨부파일 정보 연동

### RAG / AI 관리

- AI Provider 조회
- RAG 문서 목록 및 상세 조회
- RAG Chunk / Embedding 정보 연동
- RAG 질의 로그 조회

### 관리자 운영 기능

담당 운영 테이블:

- `audit_logs`
- `error_logs`
- `admin_approval_requests`
- `user_notifications`
- `maintenance_notices`

각 테이블에 대해 관리자용 목록 및 상세 조회 API를 구현했습니다.

## 4. 관리자 운영 API

| 기능 | Method | Endpoint |
|---|---|---|
| 감사 로그 목록 | GET | `/api/admin/audit-logs` |
| 감사 로그 상세 | GET | `/api/admin/audit-logs/{audit_log_id}` |
| 오류 로그 목록 | GET | `/api/admin/error-logs` |
| 오류 로그 상세 | GET | `/api/admin/error-logs/{error_log_id}` |
| 승인 요청 목록 | GET | `/api/admin/approval-requests` |
| 승인 요청 상세 | GET | `/api/admin/approval-requests/{approval_request_id}` |
| 사용자 알림 목록 | GET | `/api/admin/user-notifications` |
| 사용자 알림 상세 | GET | `/api/admin/user-notifications/{notification_id}` |
| 점검 공지 목록 | GET | `/api/admin/maintenance-notices` |
| 점검 공지 상세 | GET | `/api/admin/maintenance-notices/{maintenance_notice_id}` |

## 5. 실행 방법

프로젝트 폴더에서 다음 명령을 실행합니다.

```powershell
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

서버 실행 후 Swagger UI에서 API를 테스트할 수 있습니다.

```text
http://127.0.0.1:8001/docs
```

DB 연결 상태 확인:

```text
http://127.0.0.1:8001/health/db
```

## 6. 환경변수

DB 접속정보는 `.env` 파일에서 관리합니다.

보안을 위해 `.env` 파일은 Git에 업로드하지 않습니다.

```text
.env
.venv/
__pycache__/
*.pyc
```

## 7. 테스트 결과

FastAPI 서버와 MySQL `shopdb2` 연결을 확인하고  
Swagger UI를 이용하여 담당 관리자 운영 API를 테스트했습니다.

관리자 운영 영역의 5개 테이블에 대해

- 목록 조회 API 5개
- 상세 조회 API 5개

총 10개의 GET API에서 정상적인 HTTP `200 OK` 응답을 확인했습니다.

## 8. GitHub 관리

개발 소스는 Git을 이용하여 버전 관리하며  
`main` 브랜치를 기준으로 GitHub Repository와 연동합니다.

수정 후 기본 반영 절차:

```powershell
git add .
git commit -m "작업 내용"
git push
```

---

SHOPDB2 FastAPI + MySQL 조별 프로젝트