"""
Show candidate data stored in MongoDB for this project.

Usage examples (from the backend folder):

  # Show first 20 candidates, pretty-printed
  python scripts/show_mongo_data.py --limit 20 --pretty

  # Show all candidates (be careful if large)
  python scripts/show_mongo_data.py --limit 0 --pretty

Environment:
  - Reads DATABASE_URL from .env (defaults to mongodb://localhost:27017)
  - Connects to database 'talent_hiring' and collection 'candidates'
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

from dotenv import load_dotenv  # type: ignore
from pymongo import MongoClient  # type: ignore
from bson import ObjectId  # type: ignore


def to_serializable(obj: Any) -> Any:
    """JSON serializer for special types like ObjectId and datetime."""
    if isinstance(obj, ObjectId):
        return str(obj)
    # Let json handle datetime via default=str in dumps
    return str(obj)


def fetch_candidates(client: MongoClient, limit: int, skip: int) -> List[Dict[str, Any]]:
    db = client["talent_hiring"]
    col = db["candidates"]
    cursor = col.find({}).skip(skip)
    if limit and limit > 0:
        cursor = cursor.limit(limit)
    return list(cursor)


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Show/Manage MongoDB candidate data for Talent Hiring project")
    parser.add_argument("--limit", type=int, default=20, help="Max documents to show (0 = no limit). Default: 20")
    parser.add_argument("--skip", type=int, default=0, help="Number of documents to skip before showing")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--count", action="store_true", help="Only print total document count and exit")
    parser.add_argument("--clear", action="store_true", help="Delete ALL documents in the candidates collection (DANGEROUS)")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt when used with --clear")
    args = parser.parse_args()

    mongo_url = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    client = MongoClient(mongo_url)
    db = client["talent_hiring"]
    col = db["candidates"]

    if args.clear:
        total = col.count_documents({})
        if total == 0:
            print("Collection is already empty. Nothing to delete.")
            return
        print(
            f"WARNING: You are about to delete {total} documents from 'talent_hiring.candidates'\n"
            f"Mongo URL: {mongo_url}\n"
        )
        if not args.yes:
            confirm = input("Type DELETE to confirm: ").strip()
            if confirm != "DELETE":
                print("Aborted. No documents were deleted.")
                return
        result = col.delete_many({})
        print(f"Deleted {result.deleted_count} documents from talent_hiring.candidates")
        return

    if args.count:
        total = col.count_documents({})
        print(f"Total candidates: {total}")
        return

    docs = fetch_candidates(client, args.limit, args.skip)

    if args.pretty:
        print(json.dumps(docs, default=to_serializable, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(docs, default=to_serializable))


if __name__ == "__main__":
    main()
