import streamlit as st
import yaml

# 設定頁面配置
st.set_page_config(layout="wide", page_title="NotebookLM Visual Architect v3.1", page_icon="🎬")

# ==========================================
# 1. 數據庫定義 (Presets)
# ==========================================

# --- Video 腳本風格預設 ---
VIDEO_PRESETS = {
    "希伯來盟約史詩 (Hebrew Epic)": {
        "description": "電影質感、宏大敘事，適合歷史重現與願景影片。",
        "vision": {
            "style": "Cinematic Realism (Dune Style)",
            "mood": "神聖、滄桑、震撼 (Awe-inspiring)",
            "pacing": "緩慢鋪陳 -> 震撼高潮 (Slow burn to Climax)"
        },
        "audio": {
            "vo": "深沉的先知性旁白 (Prophetic Narrator)",
            "music": "管弦樂、Duduk 笛聲、戰鼓",
            "sfx": "曠野風聲、火焰燃燒聲、雷鳴"
        },
        "visuals": {
            "lighting": "林布蘭光 (Chiaroscuro), 耶穌光 (God rays)",
            "camera": "史詩航拍 (Drone), 緩慢推軌 (Slow Dolly)",
            "palette": "金色、深藍、赤紅、沙色"
        }
    },
    "現代科技解說 (Tech Explainer)": {
        "description": "快節奏、幾何圖形、UI 演示，適合產品發布與教學。",
        "vision": {
            "style": "Motion Graphics & Mixed Media",
            "mood": "專業、前衛、高能量 (High Energy)",
            "pacing": "快速剪輯 (Snappy cuts)"
        },
        "audio": {
            "vo": "親切、聰明、對話感 (Conversational)",
            "music": "Lo-fi Beats, Upbeat Electronic",
            "sfx": "鍵盤聲、數位轉場音效 (Whoosh, Glitch)"
        },
        "visuals": {
            "lighting": "高對比霓虹光 (Neon), 柔光箱 (Softbox)",
            "camera": "動態運鏡 (Whip pans), 螢幕錄製縮放",
            "palette": "深色模式黑、螢光青、白"
        }
    },
    "社群短影音 (Viral Short)": {
        "description": "9:16 垂直構圖、強調鉤子 (Hook)、高互動性。",
        "vision": {
            "style": "UGC (User Generated Content) Style",
            "mood": "真實、有趣、直接",
            "pacing": "極快 (Fast-paced), 每 3 秒一個切換"
        },
        "audio": {
            "vo": "充滿活力、第一人稱 (Vlogger)",
            "music": "Trending TikTok Sounds",
            "sfx": "強調音效 (Pop, Ding)"
        },
        "visuals": {
            "lighting": "自然光、環形燈",
            "camera": "手持感 (Handheld), 第一人稱視角 (POV)",
            "palette": "鮮豔、高飽和度"
        }
    }
}

# (為了代碼完整性，保留 Slide/Info/Audio 的簡化佔位符，實際使用請保留您之前的完整定義)
SLIDE_PRESETS = {"希伯來盟約": {}, "瑞士國際主義": {}}
INFO_PRESETS = {"長卷軸敘事": {}}
AUDIO_PRESETS = {"希伯來盟約": {}}

# ==========================================
# 2. 介面邏輯
# ==========================================

st.sidebar.title("🎬 NotebookLM Director")
mode = st.sidebar.radio(
    "請選擇生成目標", 
    ["🎬 Video Script (影音分鏡)", "🎙️ Audio Overview (語音導覽)", "📽️ 投影片 (Slides)", "📊 資訊圖表 (Infographics)"],
    index=0
)
st.sidebar.divider()

if mode == "🎬 Video Script (影音分鏡)":
    st.sidebar.subheader("影片風格")
    video_key = st.sidebar.selectbox("載入預設", list(VIDEO_PRESETS.keys()))
    preset = VIDEO_PRESETS[video_key]

    st.title("NotebookLM Video Script Generator")
    st.caption("將您的筆記轉換為詳細的「分鏡腳本」與「AI 影片生成指令」。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 🎥 導演板 (Director's Slate)")
        
        tab_vision, tab_audio, tab_tech = st.tabs(["視覺風格", "聲音設計", "技術規格"])

        with tab_vision:
            st.info("定義畫面看起來的樣子")
            v_style = st.text_input("影像風格", value=preset['vision']['style'])
            v_mood = st.text_input("情緒氛圍", value=preset['vision']['mood'])
            v_cam = st.text_area("運鏡語言", value=preset['visuals']['camera'])
            v_light = st.text_area("光影設定", value=preset['visuals']['lighting'])

        with tab_audio:
            st.success("定義聽起來的樣子")
            a_vo = st.text_input("旁白人設", value=preset['audio']['vo'])
            a_music = st.text_input("配樂風格", value=preset['audio']['music'])
            a_sfx = st.text_input("關鍵音效", value=preset['audio']['sfx'])

        with tab_tech:
            st.warning("格式設定")
            duration = st.selectbox("目標時長", ["60秒 (Short)", "3分鐘 (Overview)", "10分鐘 (Deep Dive)"])
            format_ratio = st.selectbox("畫面比例", ["16:9 (橫式電影/YouTube)", "9:16 (垂直 IG/TikTok)", "2.35:1 (寬銀幕史詩)"])
            prompt_engine = st.selectbox("目標 AI 生成器", ["Runway Gen-2", "Sora", "Kling AI", "Midjourney (Static)"])

        # 建構 Video YAML
        video_yaml = {
            "type": "Video Script Directive",
            "meta": {"title": "Generated from NotebookLM", "duration": duration, "ratio": format_ratio},
            "director_vision": {
                "style": v_style,
                "mood": v_mood,
                "pacing": preset['vision']['pacing']
            },
            "audio_design": {
                "voice_over": a_vo,
                "music_cues": a_music,
                "sfx_focus": a_sfx
            },
            "visual_language": {
                "camera": v_cam,
                "lighting": v_light,
                "target_engine": prompt_engine
            },
            "output_requirement": "Markdown Table with detailed Prompt engineering columns."
        }

    with col2:
        st.markdown("#### 🚀 生成指令 (Prompt Generation)")
        st.caption("複製此指令，貼入 NotebookLM 的 **對話框 (Chat)**。")

        prompt_text = f"""
請扮演一位專業的紀錄片導演與編劇。請依照這份 YAML 設定檔，將我的筆記內容改寫成一份詳細的 **「影片分鏡腳本 (Video Script)」**。

---
**[ 核心指令 ]**
1. **格式要求**：請務必輸出為一個 **Markdown 表格**，包含以下欄位：
   - **時間 (Time)**：例如 00:00-00:10
   - **畫面描述 (Scene Description)**：詳細描述場景、動作與氛圍。
   - **旁白/對白 (Audio/VO)**：逐字稿內容，請符合「{a_vo}」的語氣。
   - **聲音提示 (SFX/Music)**：標註何時進音樂或音效（如：{a_sfx}）。
   - **AI 生成指令 ({prompt_engine} Prompt)**：這是最重要的一欄。請將該場景轉換為英文的 AI 繪圖/影片生成 Prompt，需包含「{v_style}」、「{v_light}」等關鍵詞。

2. **內容轉譯**：
   - 不要只是朗讀筆記。請將抽象的概念轉化為具體的視覺隱喻。
   - 節奏控制：{preset['vision']['pacing']}。

3. **視覺風格 (Visual Language)**：
   - 整體風格：{v_style}
   - 光影氛圍：{v_mood}
   - 運鏡方式：{v_cam}

---
{yaml.dump(video_yaml, allow_unicode=True)}
"""
        st.text_area("複製此指令", value=prompt_text, height=450)
        
        st.divider()
        st.markdown("#### 📝 YAML 預覽")
        st.code(yaml.dump(video_yaml, allow_unicode=True), language='yaml')

else:
    # 這裡顯示 Audio/Slide/Info 的介面 (為節省篇幅省略，請保留原代碼)
    st.info("請從側邊欄選擇其他模式。")
