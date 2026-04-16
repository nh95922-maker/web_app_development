import sqlite3
import os

# 資料庫連線預設位置
# 在 Flask App 環境中對應根目錄的 instance 資料夾
DATABASE_PATH = os.path.join("instance", "database.db")

def get_db_connection():
    """建立並取得 SQLite 資料庫連線"""
    # 確保 instance 資料夾存在，避免產生 Exception
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    # 設定 Row Factory 以便可以直接使用 dictionary 鍵值存取資料
    conn.row_factory = sqlite3.Row
    return conn

def create_task(title, due_date=None):
    """新增一筆任務"""
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, due_date, status) VALUES (?, ?, 0)",
        (title, due_date)
    )
    conn.commit()
    conn.close()

def get_all_tasks():
    """取得所有任務，自動將快要到期的項目往前排列，新任務優先看"""
    conn = get_db_connection()
    # ASC 排序字母愈前面愈早，未設定 due_date 的將會排至後面
    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY due_date ASC, created_at DESC"
    ).fetchall()
    conn.close()
    return tasks

def get_task_by_id(task_id):
    """取得特定單一筆任務資訊 (用於編輯頁面讀取)"""
    conn = get_db_connection()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    conn.close()
    return task

def update_task(task_id, title, due_date):
    """更新特定任務的名稱以及期限"""
    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET title = ?, due_date = ? WHERE id = ?",
        (title, due_date, task_id)
    )
    conn.commit()
    conn.close()

def delete_task(task_id):
    """刪除單筆任務"""
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()

def toggle_task_status(task_id):
    """切換資料庫內的任務完成與否的狀態"""
    conn = get_db_connection()
    task = conn.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task:
        # 切換：如果原先為 0 則改 1，若 1 理當變回 0
        new_status = 1 if task['status'] == 0 else 0
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        conn.commit()
    conn.close()
