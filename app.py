import streamlit as st
from google import genai
from google.genai import types
import yt_dlp
import os
import time

# --- 頁面配置 ---
st.set_page_config(page_title="Music Insight AI", page_icon="🎧", layout="wide")
st.title("🎧 音樂深度導聆：音訊與意境全分析")

# --- API 設定 ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("輸入 Gemini API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)

    # --- 下載 YouTube 音訊與資訊欄 ---
    def process_youtube(url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info.get('description', ''), info.get('title', ''), "temp_audio.mp3"

    # --- UI 介面 ---
    yt_url = st.text_input("請輸入 YouTube 歌曲連結：", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("🚀 開始深度導聆分析"):
        if not yt_url:
            st.warning("請先輸入連結")
        else:
            try:
                with st.spinner("1. 正在從 YouTube 擷取音訊與資訊欄..."):
                    description, title, audio_path = process_youtube(yt_url)
                
                with st.spinner("2. 正在上傳音訊至 Gemini File API..."):
                    # 上傳音訊檔案
                    audio_file = client.files.upload(file=audio_path)
                    # 等待檔案處理（音訊檔案通常需要幾秒鐘讓系統準備）
                    while audio_file.state.name == "PROCESSING":
                        time.sleep(2)
                        audio_file = client.files.get(name=audio_file.name)

                with st.spinner("3. AI 正在聆聽並閱讀意境..."):
                    prompt = f"""
                    影片標題：{title}
                    資訊欄文字：{description}

                    請執行以下多重任務：
                    1. 【歌詞過濾】：從資訊欄中提取純歌詞，但不需要輸出給我，而是分析它。如果沒有歌詞，請註明「資訊欄未提供歌詞」。
                    2. 【音訊特徵分析】：你現在具備聽覺。請分析這首音軌的音樂風格、主導樂器（如：合成器、電吉他、鋼琴）以及節奏感。
                    3. 【意境與情感】：結合歌詞與旋律，深入解析這首歌傳達的情感意境。
                    4. 【視覺化建議】：如果這首歌要拍一段 MV，你會建議什麼樣的色調與視覺場景？
                    
                    請用繁體中文回答，並以精美的 Markdown 格式與標題呈現。輸出不超過750個字
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.0-flash-lite',
                        contents=[audio_file, prompt]
                    )

                # --- 顯示結果 ---
                st.success("分析完成！")
                st.subheader(f"🎵 歌曲分析報告：{title}")
                st.markdown(response.text)
                
                # 清理暫存檔
                os.remove(audio_path)
                client.files.delete(name=audio_file.name)

            except Exception as e:
                st.error(f"發生錯誤：{str(e)}")
else:
    st.info("請先輸入 API Key 以開始使用。")