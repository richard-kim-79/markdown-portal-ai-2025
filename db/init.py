# db/init.py

"""
DB 초기화를 위한 실행 스크립트입니다.
터미널에서 직접 실행하여 summary_documents 및 collection_logs 테이블을 생성합니다.
"""

from db.models import init_db

if __name__ == "__main__":
    print("📦 DB 초기화 시작...")
    init_db()
    print("✅ DB 초기화 완료.")