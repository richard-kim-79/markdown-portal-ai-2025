import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple, Any
from pathlib import Path

# 프로젝트 루트 기준 DB 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "summary.db"

# 폴더 자동 생성
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_db():
    """
    summary_documents 및 collection_logs 테이블을 생성 (존재하지 않을 경우).
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # 문서 저장 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS summary_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                summary TEXT,
                tags TEXT,
                category TEXT,
                url TEXT,
                saved_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 수집 로그 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collection_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                keyword TEXT,
                status TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
    print(f"✅ SQLite DB 초기화 완료: {DB_PATH}")


def insert_document(
    title: str,
    content: str,
    summary: str,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    url: Optional[str] = None,
    saved_path: Optional[str] = None
):
    """
    새 문서를 summary_documents 테이블에 삽입합니다.
    """
    tag_string = ",".join(tags) if tags else ""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO summary_documents (title, content, summary, tags, category, url, saved_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, content, summary, tag_string, category, url, saved_path))
        conn.commit()


def get_all_documents() -> List[Tuple[Any]]:
    """
    저장된 모든 문서를 최신순으로 반환합니다.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM summary_documents
            ORDER BY created_at DESC
        """)
        return cursor.fetchall()


def log_collection(source: str, keyword: str, status: str, message: str):
    """
    수집 결과를 collection_logs 테이블에 저장합니다.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO collection_logs (source, keyword, status, message)
            VALUES (?, ?, ?, ?)
        """, (source, keyword, status, message))
        conn.commit()


def get_recent_logs(limit: int = 50) -> List[Tuple[Any]]:
    """
    최근 수집 로그를 반환합니다.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM collection_logs
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()