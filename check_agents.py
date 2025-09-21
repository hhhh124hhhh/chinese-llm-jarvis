import sqlite3
import json

# 连接到SQLite数据库
conn = sqlite3.connect('C:/Users/17723/.letta/sqlite.db')
cursor = conn.cursor()

# 查询agents表
cursor.execute("SELECT id, name, llm_config FROM agents")
results = cursor.fetchall()

print('Agents:')
for row in results:
    print(f'ID: {row[0]}, Name: {row[1]}')
    # 尝试解析JSON
    try:
        llm_config = json.loads(row[2])
        print(f'  LLM Config: {llm_config}')
    except:
        print(f'  LLM Config: {row[2]}')
    print()

conn.close()