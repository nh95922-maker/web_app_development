# 路由設計 — 任務管理系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 任務列表 | GET | `/` | `index.html` | 顯示首頁，並從資料庫讀取所有任務列出 |
| 新增任務頁面 | GET | `/tasks/new` | `form.html` | 顯示建立新任務的空白表單 |
| 建立任務 | POST | `/tasks` | — | 接收來自表單的資料寫入資料庫，完成後重導向至 `/` |
| 編輯任務頁面 | GET | `/tasks/<id>/edit` | `form.html` | 查詢特定 id 之任務，將既有內容帶入表單顯示以供修改 |
| 更新任務 | POST | `/tasks/<id>` | — | 接收已修改任務資料，更新相對應庫存紀錄後重導向至 `/` |
| 刪除任務 | POST | `/tasks/<id>/delete` | — | 刪除單筆特定任務資料，完成重導向至 `/` |
| 切換狀態 | POST | `/tasks/<id>/toggle` | — | 翻轉特定任務的已完成/未完成狀態，完成重導向至 `/` |

## 2. 每個路由的詳細說明

### `GET /`
- **輸入**: 無
- **處理邏輯**: 呼叫 Model 的 `get_all_tasks()` 方法取得任務陣列。
- **輸出**: 渲染 `index.html`，並將任務串列傳入模板的 `tasks` 變數。

### `GET /tasks/new`
- **輸入**: 無
- **處理邏輯**: 無須呼叫 Model。
- **輸出**: 渲染 `form.html`，並傳入目標 action 給 HTML 表單運用。

### `POST /tasks`
- **輸入**: 來自表單的 `title` 與 `due_date` 欄位值。
- **處理邏輯**: 驗證 `title` 是否空白；通過則呼叫 Model `create_task(title, due_date)`。
- **輸出**: 處理完畢後，透過 302 Redirect 重新導至 `/` 首頁。

### `GET /tasks/<id>/edit`
- **輸入**: 網址中的任務 `<id>`。
- **處理邏輯**: 呼叫 Model `get_task_by_id(id)` 取出本筆任務資訊，若不存在則使用 `abort(404)` 到 404 處理區。
- **輸出**: 渲染 `form.html`，將取得的任務物件傳入，作為給 value 的預帶變數。

### `POST /tasks/<id>`
- **輸入**: 來自表單的更新值 `title`, `due_date`。
- **處理邏輯**: 呼叫 Model `update_task(id, title, due_date)`。
- **輸出**: 寫入成功後重導向回 `/` 首頁。

### `POST /tasks/<id>/delete`
- **輸入**: 提供目標 URL 內的 `<id>`。
- **處理邏輯**: 呼叫 Model `delete_task(id)`。
- **輸出**: 刪除後重導向回首頁 `/`。

### `POST /tasks/<id>/toggle`
- **輸入**: 提供目標 `<id>`。
- **處理邏輯**: 呼叫 Model `toggle_task_status(id)` 進行變更。
- **輸出**: 變更完成後重新導往 `/`。

## 3. Jinja2 模板清單

這三個檔案將會存放於接下來會建立的 `app/templates/` 之中，以支援上述所有路由的畫面呈現：

1. **`base.html`**
   - 主要入口，含網站共同外層框架、並負責引入共同的 CSS / JS 靜態資源。
2. **`index.html`**
   - 負責渲染迴圈清單。
   - 使用 `{% extends "base.html" %}` 與基底合併。
3. **`form.html`**
   - 作為「新增」與「編輯」共用的畫面，能接受帶預設數值或全空白狀況；如果 `task` 存在就判斷為進入修改模式。
   - 使用 `{% extends "base.html" %}` 與基底合併。
