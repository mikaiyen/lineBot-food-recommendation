
---

# 掌中美食推薦家 (LINE ChatGPT Food Recommender)

「掌中美食推薦家」透過 LINE 聊天機器人介面，串接 OpenAI 的 ChatGPT，根據使用者在 LINE 對話中輸入的一系列偏好(用餐時間、主食選擇、預算、辣度、冷暖體感)，智慧地生成具有說服力的餐點推薦短文。使用者可以透過簡易的互動式按鈕，一步步選擇屬於自己風格的美食體驗。

---

## 專案介紹

1. **核心理念**  
   - 提供一個 **便利、友善** 的 LINE 機器人介面，幫助忙碌的現代人在「該吃什麼？」的日常難題中，快速給出個性化的美食建議。  
   - 利用 **ChatGPT** 模型生成文情並茂的推薦文案，增添用餐動機與樂趣。  

2. **主要功能**  
   - **多階段選單**：使用者依序回答機器人提出的 **用餐時段 / 主食類型 / 預算範圍 / 辣度 / 體感冷暖** 等選項。  
   - **ChatGPT 生成**：收集完使用者回答後，系統將組裝 prompt 發送至 OpenAI API，並回傳深度學習生成的推薦短文與理由。  
   - **簡單且友善**：整個流程透過 LINE Bot 的 Template Message（按鈕樣板）互動，無需自行輸入複雜文字。

---

## 系統架構與流程

1. **使用者端**：  
   - 於 **LINE** 上與機器人進行聊天，點擊按鈕選擇餐點偏好。
2. **伺服器端 (Flask)**：  
   - 接收 LINE Webhook 傳入的事件與使用者選項。  
   - 組裝問題 (prompt)，傳送至 OpenAI ChatGPT API，取得建議文字。  
   - 將 ChatGPT 回覆包裝為 LINE 回應訊息 (TextSendMessage) 回傳給使用者。  
3. **OpenAI ChatGPT**：  
   - 基於使用者提供的偏好，生成貼合情境且引人食慾的短文與理由。

---

## 程式結構

```
.
├── main.py               # 含LINE Bot與OpenAI串接邏輯
├── README.md             # 專案說明
```

- **main.py**：  
  - 使用 `Flask` 作為 Web Framework，監聽 /callback 路徑。  
  - 透過 `line-bot-sdk` 處理 LINE Bot 的 webhook 事件 (MessageEvent、PostbackEvent)。  
  - 收集使用者在 Template Message 中選擇的內容，組裝 ChatGPT prompt，呼叫 OpenAI API，並回傳推薦結果。

---

## 快速開始 (Setup & Run)

1. **設定環境變數** (建議方式)  
   - `LINE_CHANNEL_ACCESS_TOKEN`：您的 LINE Bot Access Token  
   - `LINE_CHANNEL_SECRET`：您的 LINE Bot Channel Secret  
   - `OPENAI_API_KEY`：您的 OpenAI API 金鑰

   或直接在 `main.py` 中填寫(不建議，需注意隱私與安全)。

2. **執行程式**  
   ```bash
   python main.py
   ```
   - 預設會在本地 `http://127.0.0.1:5000` 執行 Flask 伺服器。
   - 執行.py和ngrok.exe後cmd輸入 ngrok http 5000 ，複製 Forwarding網址/callback 到 Messaging API 的 Webhook URL選擇use即上線

3. **Ngrok / 伺服器佈署**  
   - 若在本地測試，需使用 [ngrok](https://ngrok.com/) 或其他工具將 5000 port 對外公開，取得 HTTPS URL，如 `https://xxxx.ngrok.io`  
   - 將該 URL + `/callback` 填入 [LINE Developers Messaging API](https://developers.line.biz/console/) 的 Webhook URL 區域，即可上線測試。

---

## 使用方式

1. **在 LINE 上與機器人對話**：  
   - 輸入關鍵字 `@吃啥` (或依您在 `main.py` 中定義的觸發條件)，機器人會回覆「ButtonsTemplate」，引導使用者選擇 `早餐 / 午餐 / 晚餐 / 點心`。  
   - 之後依序選擇 **飯/麵/其他 → 預算範圍 → 能接受的辣度 → 體感冷暖**。  
2. **ChatGPT 推薦**：  
   - 當所有選項都確認完畢，機器人會將這些條件組裝成 prompt 送至 ChatGPT，並回傳一段結合美味描述、原因解釋的文字訊息給使用者。  

---

## 系統特色

1. **聊天式串接**：以 **LINE Bot** 為前端，不須自行撰打繁瑣訊息；只需點選按鈕完成。  
2. **個性化體驗**：透過多個步驟蒐集使用者偏好 (時間、主食、預算、辣度、冷暖)，大幅提升推薦內容的精準度。  
3. **文情並茂的推薦**：ChatGPT 生成優美富有說服力的短文，激起對該道美食的興趣。  

---

## 後續可擴充方向

- **更細緻的問題**：加入口味喜好 (甜 / 鹹 / 酸 / 苦)、餐廳類型 (中式 / 西式 / 日式…)。  
- **地理位置串接**：串接 Google Maps API 或自建 POI 資料庫，推薦附近實際可去的餐廳。  
- **資料庫使用者行為分析**：記錄使用者歷史選擇、回饋評分，不斷優化模型。  
- **多語言支援**：讓機器人與 ChatGPT 支援英文、日文等多國語系。

---
