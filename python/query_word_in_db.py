# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pymysql",
# ]
# ///

"""
Scan MySQL tables for a substring in text-like columns.

Only searches varchar/char/text/json/enum/set style columns; skips ``id`` and
columns whose names end with ``_id``. Writes one CSV row per column as it runs.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

import pymysql

_IDENT = re.compile(r"^[A-Za-z0-9_]+$")

TEXT_COLUMN_TYPES = frozenset(
    {
        "varchar",
        "char",
        "text",
        "mediumtext",
        "longtext",
        "tinytext",
        "enum",
        "set",
        "json",
    }
)


def _require_ident(name: str, label: str) -> str:
    if not name or not _IDENT.fullmatch(name):
        raise ValueError(f"Invalid {label} (allowed: letters, digits, underscore): {name!r}")
    return name


def _row_get(row: dict, key: str) -> str:
    for k, v in row.items():
        if k.lower() == key.lower():
            return str(v)
    raise KeyError(key)


@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str
    connect_timeout: int
    ssl_ca_none: bool


def load_table_names(*, tables: Sequence[str], tables_files: Iterable[Path]) -> list[str]:
    names: list[str] = []
    for raw in tables:
        t = raw.strip()
        if t:
            names.append(t)
    for path in tables_files:
        p = Path(path).expanduser()
        if not p.is_file():
            raise FileNotFoundError(
                "Tables file not found or not a regular file.\n"
                f"  Argument: {path!s}\n"
                f"  Resolved: {p.resolve()}\n"
                f"  Current directory: {Path.cwd()}\n"
                "Tip: create the file (one table name per line), cd to its directory, "
                "or pass a full path: -f /path/to/tables.txt"
            )
        text = p.read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            names.append(line)
    # stable unique order
    seen: dict[str, None] = {}
    for n in names:
        seen.setdefault(n, None)
    return list(seen.keys())


def mysql_connect(cfg: DBConfig) -> pymysql.connections.Connection:
    ssl_kw: dict | None
    if cfg.ssl_ca_none:
        ssl_kw = {"ca": None}
    else:
        ssl_kw = None
    return pymysql.connect(
        host=cfg.host,
        port=cfg.port,
        user=cfg.user,
        password=cfg.password,
        database=cfg.database,
        charset="utf8mb4",
        ssl=ssl_kw,
        connect_timeout=cfg.connect_timeout,
        cursorclass=pymysql.cursors.DictCursor,
    )


def fetch_all_base_tables(cursor: pymysql.cursors.Cursor, database: str) -> list[str]:
    _require_ident(database, "database name")
    cursor.execute(
        """
        SELECT TABLE_NAME
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """,
        (database,),
    )
    rows = cursor.fetchall()
    out: list[str] = []
    for row in rows:
        t = _row_get(row, "TABLE_NAME")
        if _IDENT.fullmatch(t):
            out.append(t)
    return out


class DBTextSearcher:
    def __init__(self, cfg: DBConfig, search_text: str, output_dir: Path):
        self.cfg = cfg
        self.search_text = search_text
        self.output_dir = output_dir
        self.conn: pymysql.connections.Connection | None = None
        self.cursor: pymysql.cursors.Cursor | None = None
        self.csv_file_path = self._new_csv_path()

    def _new_csv_path(self) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.output_dir / f"field_search_result_{stamp}.csv"

    def connect(self) -> None:
        self.conn = mysql_connect(self.cfg)
        self.cursor = self.conn.cursor()

    def close(self) -> None:
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None

    def _write_csv_header(self) -> None:
        fieldnames = [
            "database",
            "table",
            "column",
            "column_type",
            "status",
            "match_count",
            "query_time",
            "elapsed_seconds",
            "search_text",
        ]
        with self.csv_file_path.open("w", encoding="utf-8-sig", newline="") as f:
            csv.DictWriter(f, fieldnames=fieldnames).writeheader()

    def _save_row(self, row: dict) -> None:
        with self.csv_file_path.open("a", encoding="utf-8-sig", newline="") as f:
            csv.DictWriter(f, fieldnames=list(row.keys())).writerow(row)

    def get_table_columns(self, table_name: str) -> list[dict]:
        db = _require_ident(self.cfg.database, "database name")
        tbl = _require_ident(table_name, "table name")
        assert self.cursor is not None
        self.cursor.execute(f"DESC `{db}`.`{tbl}`")
        return list(self.cursor.fetchall())

    @staticmethod
    def is_skip_id_field(col_name: str) -> bool:
        c = col_name.lower()
        return c == "id" or col_name.endswith("_id")

    def search_field(self, table_name: str, col_name: str) -> tuple[int, float]:
        db = _require_ident(self.cfg.database, "database name")
        tbl = _require_ident(table_name, "table name")
        col = _require_ident(col_name, "column name")
        assert self.cursor is not None
        start = time.time()
        sql = (
            f"SELECT COUNT(1) AS cnt FROM `{db}`.`{tbl}` "
            f"WHERE LOCATE(%s, CAST(`{col}` AS CHAR)) > 0"
        )
        self.cursor.execute(sql, (self.search_text,))
        row = self.cursor.fetchone()
        if not row:
            cnt = 0
        else:
            cnt = int(_row_get(row, "cnt"))
        cost = round(time.time() - start, 4)
        return cnt, cost

    def scan_table(self, table_name: str) -> None:
        print(f"\n===== table: {table_name} =====")
        columns = self.get_table_columns(table_name)

        for col in columns:
            col_name = _row_get(col, "Field")
            col_type_raw = _row_get(col, "Type").lower()
            col_type_simple = col_type_raw.split("(", 1)[0]
            query_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if self.is_skip_id_field(col_name):
                status = "skipped: id / _id suffix"
                match_count = 0
                cost = 0.0
                print(f"skip {col_name} -> {status}")

            elif col_type_simple not in TEXT_COLUMN_TYPES:
                status = "skipped: non-text type"
                match_count = 0
                cost = 0.0
                print(f"skip {col_name} -> {status}")

            else:
                match_count, cost = self.search_field(table_name, col_name)
                status = "searched"
                print(f"search {col_name} -> matches {match_count}")

            self._save_row(
                {
                    "database": self.cfg.database,
                    "table": table_name,
                    "column": col_name,
                    "column_type": col_type_simple,
                    "status": status,
                    "match_count": match_count,
                    "query_time": query_time,
                    "elapsed_seconds": cost,
                    "search_text": self.search_text,
                }
            )

    def run(self, table_names: list[str]) -> int:
        if not table_names:
            print("No tables to scan.", file=sys.stderr)
            return 1
        try:
            self.connect()
            print("Connected.")
            self._write_csv_header()
            for tbl in table_names:
                _require_ident(tbl, "table name")
                self.scan_table(tbl)
            print(f"\nDone. CSV: {self.csv_file_path}")
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        finally:
            self.close()
            print("Connection closed.")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Search MySQL text columns for a substring; write per-column results to CSV."
    )
    p.add_argument(
        "-s",
        "--search",
        required=True,
        help="Substring to find (LOCATE / contains).",
    )
    p.add_argument("--host", default=os.environ.get("MYSQL_HOST", "127.0.0.1"))
    p.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("MYSQL_PORT", "3306")),
    )
    p.add_argument("--user", default=os.environ.get("MYSQL_USER", ""))
    p.add_argument(
        "--password",
        default=os.environ.get("MYSQL_PASSWORD", ""),
        help="Also read from MYSQL_PASSWORD env var.",
    )
    p.add_argument("--database", default=os.environ.get("MYSQL_DATABASE", ""))
    p.add_argument(
        "-T",
        "--table",
        action="append",
        default=[],
        metavar="NAME",
        help="Table to scan (repeatable).",
    )
    p.add_argument(
        "-f",
        "--tables-file",
        type=Path,
        action="append",
        default=[],
        metavar="PATH",
        help="File with one table name per line (# comments allowed). Repeatable.",
    )
    p.add_argument(
        "--all-tables",
        action="store_true",
        help="Scan every BASE TABLE in --database (use with care on large schemas).",
    )
    p.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("db_search_results"),
        help="Directory for CSV output (default: db_search_results).",
    )
    p.add_argument(
        "--connect-timeout",
        type=int,
        default=15,
        help="Connect timeout in seconds (default: 15).",
    )
    p.add_argument(
        "--no-ssl-ca-none",
        action="store_true",
        help="Do not pass ssl={'ca': None} (try this for local MySQL if SSL errors occur). "
        "Default matches Azure-style MySQL (ssl with ca=None).",
    )
    return p


def main() -> int:
    args = build_arg_parser().parse_args()
    if not args.user or not args.database:
        print(
            "Error: --user and --database are required (or MYSQL_USER / MYSQL_DATABASE).",
            file=sys.stderr,
        )
        return 1
    password = args.password
    cfg = DBConfig(
        host=args.host,
        port=args.port,
        user=args.user,
        password=password,
        database=args.database,
        connect_timeout=args.connect_timeout,
        ssl_ca_none=not args.no_ssl_ca_none,
    )

    table_names: list[str] = []
    if args.all_tables:
        if args.table or args.tables_file:
            print(
                "Warning: --all-tables used; ignoring --table / --tables-file.",
                file=sys.stderr,
            )
        conn = mysql_connect(cfg)
        try:
            cur = conn.cursor()
            table_names = fetch_all_base_tables(cur, args.database)
        finally:
            conn.close()
    else:
        try:
            table_names = load_table_names(
                tables=args.table, tables_files=args.tables_file
            )
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if not table_names:
        print(
            "Error: no tables to scan. Use --table, --tables-file, or --all-tables.",
            file=sys.stderr,
        )
        return 1

    searcher = DBTextSearcher(cfg, args.search, args.output_dir)
    return searcher.run(table_names)


if __name__ == "__main__":
    raise SystemExit(main())
