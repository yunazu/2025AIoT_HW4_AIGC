import streamlit as st
from google import genai
import os
import time

# --- 頁面配置 ---
st.set_page_config(page_title="Music Insight AI", page_icon="🎧", layout="wide")
st.title("🎧 音樂深度導聆：音訊與歌詞全分析")
st.markdown("請上傳您的音樂檔案並貼上相關資訊，讓 Gemini 2.0 為您導讀。")

# --- API 設定 ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("1. 輸入 Gemini API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)

    # --- UI 介面 ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📁 上傳音樂")
        uploaded_file = st.file_uploader("選擇音訊檔案 (mp3, wav, m4a)", type=['mp3', 'wav', 'm4a'])
        
    with col2:
        st.subheader("📝 歌詞或資訊欄內容")
        raw_text = st.text_area("請貼上 YouTube 資訊欄或歌詞內容：", height=200, placeholder="在此貼上文字...")

    if st.button("🚀 開始執行 AI 深度分析"):
        if not uploaded_file or not raw_text:
            st.warning("請確保已上傳音訊且已貼上文字內容。")
        else:
            try:
                # 1. 儲存暫存檔
                with open("temp_audio.mp3", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                with st.spinner("AI 正在聆聽音樂並閱讀文字中..."):
                    # 2. 上傳至 Google File API
                    audio_file = client.files.upload(file="temp_audio.mp3")
                    while audio_file.state.name == "PROCESSING":
                        time.sleep(2)
                        audio_file = client.files.get(name=audio_file.name)

                    # 3. 執行多模態分析
                    prompt = f"""
                    以下是這首歌的相關文字資訊：
                    {raw_text}

                    任務：
                    1. 【歌詞過濾】：從文字內容中提取純歌詞，過濾掉無關資訊。
                    2. 【聽感分析】：根據音軌分析音樂風格、主導樂器、節奏情緒。
                    3. 【深度導讀】：結合歌詞意境與旋律，撰寫一段 300 字的深度賞析。
                    4. 【視覺描述】：為這首歌設計一個 MV 視覺場景描述。
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.0-flash-lite',
                        contents=[audio_file, prompt]
                    )

                # --- 顯示結果 ---
                st.success("分析完成！")
                st.markdown(response.text)
                
                # 清理
                client.files.delete(name=audio_file.name)
                os.remove("temp_audio.mp3")

            except Exception as e:
                st.error(f"發生錯誤：{str(e)}")
else:
    st.info("請在側邊欄輸入 API Key 以開始。")