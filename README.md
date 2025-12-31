# 🎧 Music Insight AI: 音頻與意境深度分析助手

本專案是基於 Google 最新一代 **Gemini 2.5 Flash-Lite** 模型開發的生成式 AI 應用。透過多模態分析技術，系統能同時「聆聽」音樂並「閱讀」歌詞資訊，產出包含曲風判斷、樂器識別、意境解析及視覺化建議的深度導聆報告。

## 🌟 專案亮點
- **多模態融合**：不只分析文字，更直接上傳音訊檔案讓 AI 進行原生聽覺感知。
- **AI 自動資料清洗**：利用 LLM 強大的語義理解能力，自動從混亂的 YouTube 資訊欄中提取純歌詞。
- **解決部署瓶頸**：採用 API-Centric 架構，成功避開雲端伺服器 (Streamlit Cloud) 缺乏 GPU 算力難以運行深度學習模型的問題。

## 🛠️ 使用工具
- **前端開發**：[Streamlit](https://streamlit.io/)
- **AI 核心模型**：[Google Gemini 2.5 Flash-Lite](https://ai.google.dev/models/gemini)
- **開發套件**：`google-genai` (最新的 Google AI SDK)
- **部署環境**：Streamlit Cloud

## 🚀 快速開始

### 1. 取得 Gemini API Key
本專案需要 Google API 金鑰方可運行。
1. 前往 [Google AI Studio](https://aistudio.google.com/)。
2. 登入您的 Google 帳號。
3. 點擊 「Get API key」 並創建一個新金鑰。

### 2. 使用方式
1. 進入本專案的 [Streamlit App 網址] (請替換為你的網址)。
2. 在側邊欄輸入您的 **Gemini API Key**。
3. **上傳音訊**：選擇一個音樂檔案 (mp3, wav, m4a)。
4. **貼上資訊**：將 YouTube 影片的資訊欄內容或歌詞貼入文字框。
5. 點擊 **「開始執行 AI 深度分析」**。
6. 等待約 10-20 秒，即可獲得完整的分析報告。

## 📝 開發紀錄與技術決策
在開發過程中，原先嘗試使用 `yt-dlp` 自動擷取 YouTube 音軌，但因雲端環境頻繁遭遇 HTTP 403 Forbidden 封鎖，且為了符合 API 免費等級的流量限制 (Rate Limits)，最終將架構優化為「使用者主動上傳」模式。此調整確保了 100% 的執行穩定性，並透過 Google File API 處理大型