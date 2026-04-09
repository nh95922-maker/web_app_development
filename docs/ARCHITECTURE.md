# 系統架構設計 — 任務管理系統

## 1. 技術架構說明

本專案採用輕量級的後端渲染架構（Server-Side Rendering），透過單一伺服器處理業務邏輯、資料存取與網頁渲染，適合快速開發與驗證產品核心功能。

- **選用技術與原因**：
  - **後端框架：Python + Flask**。Flask 是一個輕量、靈活的 Web 微框架，適合中小型應用，沒有繁瑣的預設立場，能提供極佳的開發彈性。
  - **模板引擎：Jinja2**。Flask 原生支援 Jinja2，能直接在後端將變數與 HTML 結合成靜態頁面並回傳給瀏覽器，省去建置獨立前端框架（如 React/Vue）及跨域連線的溝通成本。
  - **資料庫：SQLite**。SQLite 是一套輕量級關聯式資料庫，資料直接儲存於本地檔案中，開發零配置（免安裝伺服器）。十分適合功能單純、無需高併發寫入的任務管理系統。

- **MVC 模式實作 (Model / View / Controller)**：
  - **Model (模型)**：負責與 SQLite 檔案互動，集中管理任務系統中所有的查詢、新增、更新與刪除（CRUD）指令。
  - **View (視圖)**：利用 Jinja2 HTML 模板，負責把拿到的資料轉換成使用者看得懂的網頁。
  - **Controller (控制器)**：在 Flask 中由「路由 (Routes)」擔任此角色。負責接收自瀏覽器傳來的參數、呼叫適當的 Model 取得資料，最後選擇並回傳正確的 View 給使用者。

## 2. 專案資料夾結構

建議採用中本型的資料夾分配，避免檔案全塞在一起。將關注點分離有助於未來的維護支援：

```text
web_app_development/
├── app/                  # 主要應用程式與邏輯目錄
│   ├── __init__.py       # 初始化 Flask 應用程式、載入專案設定
│   ├── models/           # (Model) 資料庫模型層
│   │   ├── __init__.py
│   │   └── task.py       # 包含 Task 資料庫連線及指令整合邏輯
│   ├── routes/           # (Controller) 接收請求的 API 路由層
│   │   ├── __init__.py
│   │   └── task_routes.py # 負責處理各項任務清單與狀態更新的請求
│   ├── templates/        # (View) Jinja2 HTML 畫面渲染層
│   │   ├── base.html     # 共用的頁面佈局 (含 Header/Footer)
│   │   ├── index.html    # 顯示任務列表的首頁
│   │   └── form.html     # 用於新增或編輯任務的表單分頁
│   └── static/           # CSS/Javascript 等靜態資源
│       ├── style.css     # 全域樣式，控制畫面排版與顏色
│       └── script.js     # 負責簡單的前端互動 (例如刪除再次確認彈窗)
├── instance/             # 特定環境設置或機密存儲區 (建議加入 .gitignore)
│   └── database.db       # SQLite 實體資料檔案
├── docs/                 # 設計文件存放區
│   ├── PRD.md            # 產品需求文件
│   ├── FLOWCHART.md      # 流程圖
│   └── ARCHITECTURE.md   # 架構文件 (本文)
├── app.py                # 專案主入口，用以啟動 Web Server
└── requirements.txt      # 記錄套件相依性版本 (如 flask)
```

## 3. 元件關係圖

以下展示從使用者送出請求（如點擊保存更新或查看列表），到資料庫更新處理最後回傳畫面的關聯：

```mermaid
graph TD
    %% 定義節點與樣式
    User([瀏覽器 / 使用者])
    Route[Flask Route (Controller)]
    TaskModel[Model 層 (task.py)]
    DB[(SQLite 資料庫)]
    JinjaView[Jinja2 模板 (View 本體)]

    %% 關聯流程表示
    User -- "1. 觸發 GET / POST 網路請求" --> Route
    
    Route -- "2. 要求操作/查詢資料" --> TaskModel
    TaskModel -- "3. 執行對應 SQL 語句" --> DB
    DB -. "4. 回報寫入狀態/回傳查詢結果" .-> TaskModel
    TaskModel -. "5. 將資料打包傳回 Controller" .-> Route
    
    Route -- "6. 傳遞 Python 資料結構 (變數)" --> JinjaView
    JinjaView -. "7. 將資料渲染組合至 HTML 架構" .-> Route
    
    Route -- "8. HTTP Response 回傳編譯後畫面" --> User
```

## 4. 關鍵設計決策

1. **不採用前後端分離架構**
   - **原因**：為了在最短時間內提供符合 MVP (Minimal Viable Product) 的專案版本，將前後端合併於 Flask 中可大幅降低建置與溝通的成本，也能降低入門者維護時遭遇跨域（CORS）問題的門檻。
2. **採用 SQLite 減輕資料儲存負擔**
   - **原因**：任務系統目前主要在個人追蹤的範疇，因此選擇無伺服器配置的 SQLite 能最快速運轉，同時資料也容易以實體檔案 `.db` 形式備份。一旦有擴充多人服務的需求，只需調整連線字串即可替換為 Postgres / MySQL。
3. **把邏輯切分出 Routes 與 Models**
   - **原因**：如果將所有的路由和資料庫處理都寫進 `app.py` 裡，專案會迅速變得笨重且難以除錯。我們將路由拆分至 `routes/task_routes.py`，專門處理參數傳遞；並把所有資料庫溝通封裝在 `models/task.py`，未來只要 Model 層沒有錯誤，Controller 就無須擔心會有錯誤查詢。
4. **共用 Jinja2 的 `base.html` 基礎模板**
   - **原因**：利用 Jinja 模板繼承（`{% block content %}`），能將所有頁面的共用元素像是導覽列、CSS 統一管理。未來如果想更改介面樣式，只需修改這個基底檔案，所有頁面就都會一起更新。
