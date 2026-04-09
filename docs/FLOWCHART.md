# 流程圖 — 任務管理系統

## 1. 使用者流程圖（User Flow）

以下描述使用者在本系統中的操作路徑與選擇：

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 任務列表]
    
    %% 新增任務流程
    B -->|點擊新增任務| C[新增任務表單]
    C -->|填寫完畢送出| D[系統儲存任務]
    D --> B
    
    %% 編輯任務流程
    B -->|點閱特定任務編輯| E[編輯任務表單]
    E -->|修改完畢送出| F[系統更新任務]
    F --> B
    
    %% 刪除任務流程
    B -->|點擊刪除任務| G[系統刪除該任務]
    G --> B
    
    %% 切換狀態流程
    B -->|點選完成/未完成| H[系統更新狀態]
    H --> B
```

## 2. 系統序列圖（Sequence Diagram）

以下描述「使用者嘗試新增一筆任務」時，系統各個元件如何互動與傳遞資料：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 使用者瀏覽器
    participant Flask as Flask Route
    participant DB as SQLite

    User->>Browser: 填寫「新增任務」表單並送出
    Browser->>Flask: POST /tasks (附帶任務名稱、預期時間)
    Flask->>DB: INSERT INTO tasks (title, due_date, status)
    DB-->>Flask: 成功寫入資料
    Flask-->>Browser: 重導向 (HTTP 302 Redirect) 至列表頁
    Browser->>Flask: GET /
    Flask->>DB: SELECT * FROM tasks ORDER BY due_date ASC
    DB-->>Flask: 回傳按時間排序的任務列表
    Flask-->>Browser: 回傳渲染後的首頁 HTML 頁面
    Browser-->>User: 呈現最新任務列表
```

## 3. 功能清單對照表

本系統各核心功能所對應的 URL 路徑與 HTTP 方法如下，供後續 API 與 Flask 路由實作參考：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| 瀏覽首頁任務列表 | `/` | GET | 查詢資料庫，回傳按時間排序的任務清單 |
| 新增任務頁面 | `/tasks/new` | GET | 顯示用於填寫新任務內容的網頁表單 |
| 處理新增任務 | `/tasks` | POST | 接收來自表單的資料並存入資料庫 |
| 編輯單一任務頁面 | `/tasks/<id>/edit` | GET | 查詢特定 ID 任務，顯示編輯用表單 |
| 處理更新任務 | `/tasks/<id>` | POST | 接收變更後的資料，覆寫回該筆記錄 (網頁表單常以 POST 替代 PUT) |
| 處理刪除任務 | `/tasks/<id>/delete` | POST | 接收刪除請求並移除該筆記錄 |
| 切換完成狀態 | `/tasks/<id>/toggle` | POST | 翻轉指定筆數任務的「已完成/未完成」狀態 |
