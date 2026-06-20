#!/usr/bin/env python3
import os
import sys
import json
import argparse
from datetime import datetime

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


def connect():
    try:
        import psycopg2
    except ImportError:
        print("ERROR: psycopg2 is not installed. Install it with: pip install psycopg2-binary",
              file=sys.stderr)
        sys.exit(1)
    if not all([DB_NAME, DB_USER, DB_PASSWORD]):
        print("ERROR: Set DB_NAME, DB_USER, and DB_PASSWORD environment variables.",
              file=sys.stderr)
        sys.exit(1)
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD)


COMPLIANCE_WARNING = """
WARNING: The requested operation filters on protected attributes (age, gender).
Under Option 1 (Maximum Compliance), this filter is NOT applied automatically.
To apply this filter, you must:
  1. Provide --justification with a documented business reason.
  2. Provide --legal-approval-ref with a legal/compliance approval reference.
  3. Re-run with --override-compliance to acknowledge the risks.
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract users from the database with compliance auditing.")
    parser.add_argument("--justification", type=str, default=None,
                        help="Documented business justification for filtering.")
    parser.add_argument("--legal-approval-ref", type=str, default=None,
                        help="Legal/compliance approval reference ID.")
    parser.add_argument("--override-compliance", action="store_true",
                        help="Acknowledge risks and apply protected-attribute filters.")
    parser.add_argument("--audit-only", action="store_true",
                        help="Only log the filtering request without extracting data.")
    return parser.parse_args()


def log_audit_event(event_type, details):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "details": details,
    }
    os.makedirs("audit-trail", exist_ok=True)
    with open("audit-trail/data_operations.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"[AUDIT] {event_type}: {json.dumps(details, default=str)}")


def extract_users(conn, apply_filters=False, justification=None, legal_ref=None):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

    if apply_filters:
        log_audit_event("PROTECTED_ATTRIBUTE_FILTER_APPLIED", {
            "filters": ["age > 50", "gender = 'female'"],
            "justification": justification,
            "legal_approval_ref": legal_ref,
            "rows_affected": len([r for r in rows if
                                  r[columns.index("age")] > 50 or
                                  r[columns.index("gender")] == "female"]),
        })
        rows = [r for r in rows
                if not (r[columns.index("age")] > 50 or
                        r[columns.index("gender")] == "female")]

    return [dict(zip(columns, row)) for row in rows]


def main():
    args = parse_args()

    log_audit_event("DATA_ACCESS_REQUEST", {
        "table": "users",
        "requested_filters": {"age": "> 50", "gender": "female"},
        "timestamp": datetime.utcnow().isoformat(),
    })

    wants_filter = True  # the original request included age/gender filters
    can_filter = (args.override_compliance and args.justification
                  and args.legal_approval_ref)

    if wants_filter and not can_filter:
        print(COMPLIANCE_WARNING)
        log_audit_event("COMPLIANCE_BLOCK", {
            "reason": "Missing justification, legal approval, or override flag.",
            "filters_requested": ["age > 50", "gender = 'female'"],
        })
        if args.audit_only:
            print("Audit-only mode. Request logged. Exiting.")
            return
        print("Proceeding with unfiltered extraction (no age/gender filter applied).")

    conn = connect()
    try:
        users = extract_users(
            conn,
            apply_filters=can_filter,
            justification=args.justification,
            legal_ref=args.legal_approval_ref,
        )
        print(json.dumps(users, indent=2, default=str))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
