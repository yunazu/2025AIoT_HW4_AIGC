import streamlit as st
from google import genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 影音摘要助手", page_icon="📝", layout="wide")
st.title("📝 智慧影音摘要與視覺化系統 (v2.0)")
st.markdown("本工具採用最新的 Gemini 2.0 Flash-Lite 模型，為您快速提取長文精華。")

# --- 2. 部署安全性：API Key 輸入 ---
# 提供兩種方式：優先讀取 Streamlit Secrets，若無則顯示輸入框
if "GEMINI_API_KEY" in st.secrets:
    api_key_input = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.header("🔑 API 設定")
        api_key_input = st.text_input("輸入 Google API Key:", type="password", help="請至 Google AI Studio 申請免費金鑰")
        st.info("提示：輸入的 Key 僅供本次連線使用，不會被儲存。")

# --- 3. 初始化 Client ---
if api_key_input:
    client = genai.Client(api_key=api_key_input)

# --- 4. UI 介面 ---
user_input = st.text_area("請貼上文章、逐字稿或新聞內容：", height=250, placeholder="在此輸入內容...")

# 功能選項
col_opt1, col_opt2 = st.columns(2)
with col_opt1:
    summary_style = st.selectbox("摘要風格", ["簡潔重點", "詳細分析", "專業評論"])
with col_opt2:
    output_language = st.selectbox("輸出語言", ["繁體中文", "English", "日本語"])

if st.button("🚀 開始執行 AI 分析"):
    if not api_key_input:
        st.error("❌ 請先在左側輸入 API Key 才能執行！")
    elif not user_input:
        st.warning("⚠️ 請輸入需要分析的內容。")
    else:
        try:
            with st.spinner('Gemini 2.5 正在分析中...'):
                # 任務 A: 生成摘要
                prompt_text = f"你是一個專業的內容摘要專家。請用{output_language}，以{summary_style}的風格，摘要以下內容：\n\n{user_input}"
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite', 
                    contents=prompt_text
                )
                
                # 任務 B: 生成視覺化建議 (延伸亮點)
                visual_prompt = f"根據這段摘要內容：'{response.text}'。請寫出一段適合給 AI 繪圖工具(如 DALL-E)使用的英文提示詞(Prompt)，描述一個能代表本文意境的場景。"
                response_visual = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=visual_prompt
                )

            # --- 5. 顯示結果 ---
            st.divider()
            res_col1, res_col2 = st.columns([2, 1])
            
            with res_col1:
                st.subheader("📌 AI 摘要結果")
                st.markdown(response.text)
            
            with res_col2:
                st.subheader("🎨 視覺化延伸描述")
                st.success(response_visual.text)
                st.caption("提示：您可以將上方英文複製到 Stable Diffusion 或 Midjourney 生成圖片。")

        except Exception as e:
            st.error(f"連線錯誤: {str(e)}")

# --- 6. 頁尾 ---
st.divider()
st.caption("Taica AIGC Course Project | Powered by Gemini 2.5 Flash-Lite")