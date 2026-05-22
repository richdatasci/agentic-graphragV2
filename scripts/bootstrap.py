import os
import sys
from pathlib import Path

import httpx


def check_http(name: str, url: str) -> bool:
    try:
        response = httpx.get(url, timeout=5.0)
        print(f"[ok] {name}: {response.status_code}")
        return True
    except Exception as exc:
        print(f"[warn] {name}: {exc}")
        return False


def init_local_dirs() -> None:
    Path(".local_data").mkdir(exist_ok=True)
    Path(".object_store").mkdir(exist_ok=True)
    print("[ok] local data directories")


def init_qdrant() -> None:
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    collection = os.getenv("QDRANT_COLLECTION", "documents")
    vector_size = int(os.getenv("VECTOR_SIZE", "384"))
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams

        client = QdrantClient(url=url)
        existing = [c.name for c in client.get_collections().collections]
        if collection not in existing:
            client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            print(f"[ok] qdrant collection created: {collection}")
        else:
            print(f"[ok] qdrant collection exists: {collection}")
    except Exception as exc:
        print(f"[warn] qdrant init skipped: {exc}")


def init_minio() -> None:
    try:
        from minio import Minio

        endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        bucket = os.getenv("MINIO_BUCKET", "agentic-graphrag")
        client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            print(f"[ok] minio bucket created: {bucket}")
        else:
            print(f"[ok] minio bucket exists: {bucket}")
    except Exception as exc:
        print(f"[warn] minio init skipped: {exc}")


def init_neo4j() -> None:
    try:
        from neo4j import GraphDatabase

        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "agentic-graphrag-password")
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            session.run("CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE")
            session.run("CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE")
            session.run("CREATE CONSTRAINT triple_id IF NOT EXISTS FOR (t:Triple) REQUIRE t.id IS UNIQUE")
        driver.close()
        print("[ok] neo4j constraints")
    except Exception as exc:
        print(f"[warn] neo4j init skipped: {exc}")


def init_postgres() -> None:
    try:
        import psycopg2

        dsn = (
            f"dbname={os.getenv('POSTGRES_DB', 'agentic_graphrag')} "
            f"user={os.getenv('POSTGRES_USER', 'graphrag')} "
            f"password={os.getenv('POSTGRES_PASSWORD', 'graphrag')} "
            f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
            f"port={os.getenv('POSTGRES_PORT', '5432')}"
        )
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            source_type TEXT NOT NULL,
            status TEXT DEFAULT 'indexed',
            created_at TIMESTAMP DEFAULT NOW()
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            document_id TEXT NOT NULL,
            text TEXT NOT NULL,
            chunk_index INTEGER DEFAULT 0
        )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("[ok] postgres tables")
    except Exception as exc:
        print(f"[warn] postgres init skipped: {exc}")


def main() -> int:
    print("Bootstrapping Agentic GraphRAG local services...")
    init_local_dirs()
    check_http("qdrant", os.getenv("QDRANT_URL", "http://localhost:6333") + "/")
    check_http("ollama", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/api/tags")
    init_qdrant()
    init_minio()
    init_neo4j()
    init_postgres()
    print("Bootstrap complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
