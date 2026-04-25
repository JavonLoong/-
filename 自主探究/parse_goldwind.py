import sqlite3
import csv
import os

db_path = r'd:\虚拟C盘\自主探究\goldwind_temp\Program Files (x86)\goldwind\MySetup\tempdata\GW15000120180104.db'
output_dir = r'd:\虚拟C盘\自主探究'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 列出所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"共找到 {len(tables)} 个表：")

for t in tables:
    table_name = t[0]
    # 查看列信息
    cursor.execute(f"PRAGMA table_info([{table_name}])")
    cols = cursor.fetchall()
    col_names = [c[1] for c in cols]
    
    # 查看行数
    cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
    count = cursor.fetchone()[0]
    print(f"\n表: {table_name}")
    print(f"  列({len(col_names)}): {col_names}")
    print(f"  行数: {count}")
    
    # 预览前3行
    cursor.execute(f"SELECT * FROM [{table_name}] LIMIT 3")
    rows = cursor.fetchall()
    for row in rows:
        print(f"  预览: {row}")

conn.close()
