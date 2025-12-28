import streamlit as st
import yaml

# 設定頁面配置
st.set_page_config(layout="wide", page_title="NotebookLM Architect v6.0", page_icon="🧠")

# ==========================================
# 1. 全域風格數據庫 (Master Style Database)
# ==========================================

STYLE_LIBRARY = {
    # --- 古文明系列 ---
    "希伯來盟約 (Hebrew Covenant)": {
        "desc": "史詩感、羊皮卷、金/藍/紅配色，強調神聖與歷史厚度。",
        "mood": "莊嚴、神聖、溫暖 (Solemn, Divine, Warm)",
        "palette": "羊皮紙色 (#F3E5AB)、提吉勒藍 (#0038B8)、精金 (#D4AF37)",
        "visual_elements": "古卷 (Scrolls)、古代地圖、曠野地景、火焰與光",
        "font_style": "宋體 (Serif) - 帶有書法與歷史感",
        "video_focus": "強調經文引用的視覺化、地圖路徑的演變、歷史文物的特寫"
    },
    "古埃及風格 (Ancient Egyptian)": {
        "desc": "宏偉、神秘、黑金配色，強調永恆與權威。",
        "mood": "宏大、神秘、高對比 (Monumental, Mysterious)",
        "palette": "黑曜石 (#0F0F0F)、黃金 (#D4AF37)、青金石藍 (#191970)",
        "visual_elements": "象形文字、金字塔幾何、蓮花圖騰、星空",
        "font_style": "粗宋體/飾線體 - 模仿石刻銘文",
        "video_focus": "壁畫式的橫向移動、金碧輝煌的材質特寫、星象運行的縮時"
    },
    "兩河流域 (Mesopotamian)": {
        "desc": "泥板質感、楔形文字、厚重實用，文明的基石。",
        "mood": "原始、厚重、大地感 (Earthy, Primal, Solid)",
        "palette": "未燒泥土色 (#C19A6B)、燒磚紅 (#8B4513)、深岩灰 (#2F4F4F)",
        "visual_elements": "泥板刻痕、楔形文字、磚塊堆砌結構、河流",
        "font_style": "粗黑體 (Slab Serif) - 強調刻印力度",
        "video_focus": "強調材質的紋理 (Texture)、河流流動的空拍、層層堆疊的建築結構"
    },
    "希臘地中海 (Greek Mediterranean)": {
        "desc": "藍白對比、理性光輝、柱式結構，強調邏輯與哲學。",
        "mood": "明亮、理性、通透 (Bright, Rational, Airy)",
        "palette": "大理石白 (#FFFFFF)、愛琴海藍 (#0047AB)、月桂金 (#D4AF37)",
        "visual_elements": "大理石柱、幾何對稱、雕塑光影、海洋",
        "font_style": "羅馬體 (Classic Serif) - 優雅且結構嚴謹",
        "video_focus": "純白的背景與高對比藍色、對稱的構圖、幾何圖形的動態演示"
    },
    
    # --- 現代與設計系列 ---
    "現代極簡 (Modern Minimalist)": {
        "desc": "大量留白、無襯線字體，強調訊息純粹性。",
        "mood": "冷靜、乾淨、低調 (Calm, Clean, Understated)",
        "palette": "純白 (#FFFFFF)、炭黑 (#333333)、淺灰 (#F5F5F5)",
        "visual_elements": "細線條、負空間 (Negative Space)、高解析度攝影",
        "font_style": "細黑體 (Light Sans) - 通透呼吸感",
        "video_focus": "極簡的轉場、文字淡入淡出、去除一切裝飾性元素"
    },
    "商務辦公 (Corporate Professional)": {
        "desc": "深色模式、數據驅動、高效清晰，Luke ESL 經典風格。",
        "mood": "專業、信賴、高效 (Professional, Trustworthy)",
        "palette": "深藍黑 (#0A0E14)、螢光青 (#00F0FF)、白 (#FFFFFF)",
        "visual_elements": "玻璃擬態 (Glassmorphism)、數據儀表板、科技線條",
        "font_style": "粗黑體 (Bold Sans) - 權威且易讀",
        "video_focus": "數據圖表的動態生長、螢光線條的指引、關鍵字的高亮顯示"
    },
    "包豪斯 (Bauhaus Style)": {
        "desc": "幾何圖形、原色美學、形隨機能，前衛設計感。",
        "mood": "前衛、幾何、結構 (Avant-garde, Geometric)",
        "palette": "米白 (#F0F0F0)、紅 (#D92B2B)、藍 (#1E3D99)、黃 (#F2C94C)",
        "visual_elements": "圓形/方形/三角形、斜向排版、色塊重疊",
        "font_style": "幾何無襯線 (Geometric Sans) - 如 Futura",
        "video_focus": "幾何圖形的拼貼動畫、原色的強烈對比、節奏感強烈的切換"
    },
    "日式寂 (Japanese Wabi-Sabi)": {
        "desc": "質樸自然、不對稱之美、和紙質感，強調餘韻。",
        "mood": "寧靜、禪意、自然 (Zen, Peaceful, Organic)",
        "palette": "和紙白 (#EFECE8)、抹茶綠 (#5D6858)、陶土灰 (#8C837B)",
        "visual_elements": "自然紋理、墨跡、留白 (Ma)、植物剪影",
        "font_style": "宋體/明體 (Mincho) - 纖細優雅",
        "video_focus": "緩慢的鏡頭推移、自然光影的變化、強調「間」的留白"
    }
}

INFO_STRUCTURES = {
    "長卷軸敘事": {"canvas": {"ratio": "1:4", "flow": "Top-down", "density": "Medium"}},
    "數據儀表板": {"canvas": {"ratio": "4:3", "flow": "Modular Grid", "density": "High"}},
    "對照比較圖": {"canvas": {"ratio": "16:9", "flow": "Split Center", "density": "Low"}}
}

# ==========================================
# 2. 側邊欄：統一輸入中心 (Unified Input Center)
# ==========================================

st.sidebar.title("🧠 Visual Architect v6.0")
st.sidebar.caption("Unified Context Engine")

# --- A. 內容核心 (Content Core) ---
st.sidebar.header("1. 內容定義 (Context)")
st.sidebar.info("在此設定一次，自動應用於所有輸出格式。")

global_topic = st.sidebar.text_input("主題 (Topic)", placeholder="例如：以色列人出埃及路線")
global_keywords = st.sidebar.text_area("關鍵字 (Keywords)", placeholder="例如：西奈山, 盟約, 40年曠野, 嗎哪 (以逗號分隔)", height=100)
global_audience = st.sidebar.text_input("目標受眾 (Audience)", placeholder="例如：神學生、歷史愛好者")

# --- B. 風格核心 (Style Core) ---
st.sidebar.divider()
st.sidebar.header("2. 風格定義 (Style)")

selected_style_name = st.sidebar.selectbox("視覺框架", list(STYLE_LIBRARY.keys()))
style_data = STYLE_LIBRARY[selected_style_name]

# 風格預覽
st.sidebar.markdown(f"**{selected_style_name}**")
st.sidebar.caption(style_data['desc'])
with st.sidebar.expander("查看風格參數"):
    st.write(f"🎨 配色: {style_data['palette']}")
    st.write(f"🖼️ 元素: {style_data['visual_elements']}")
    st.write(f"🎞️ 影片重點: {style_data['video_focus']}")

# ==========================================
# 3. 主畫面：多模態輸出 (Multi-modal Output)
# ==========================================

st.title(f"NotebookLM 多模態生成指令")
if global_topic:
    st.success(f"當前專案：{global_topic} | 風格：{selected_style_name}")
else:
    st.warning("請先在左側輸入「主題」與「關鍵字」以開始生成。")

# 使用 Tabs 來切換不同的輸出格式
tab_slide, tab_video, tab_info = st.tabs(["📽️ Slide Deck (投影片)", "🎬 Video Overview (導演模式)", "📊 Infographic (資訊圖表)"])

# ----------------------------------------------------
# Tab 1: Slide Deck
# ----------------------------------------------------
with tab_slide:
    st.subheader("Slide Deck Generation")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        # 繼承全域變數
        layout_logic = st.text_area("Slide 版型邏輯", value="Title: impactful-center\nData: chart-focus\nQuote: typographic-poster", height=100)
        
        slide_yaml = {
            "type": "Presentation Slides",
            "meta": {"topic": global_topic, "audience": global_audience},
            "content_context": {
                "keywords": [k.strip() for k in global_keywords.split(",")] if global_keywords else [],
                "instruction": "Highlight these keywords visually."
            },
            "framework": selected_style_name,
            "brand": {"tone": style_data['mood']},
            "visual_prompts": {"instruction": f"Use {style_data['visual_elements']} with {style_data['palette']} palette."},
            "layout_intent": layout_logic.split('\n'),
            "typography": style_data['font_style']
        }
    
    with col2:
        st.caption("複製此 YAML 給 NotebookLM")
        st.code(yaml.dump(slide_yaml, allow_unicode=True), language='yaml')
        
        prompt_text = f"""請將筆記轉化為投影片大綱。
主題：{global_topic}
關鍵字：{global_keywords}
風格：{selected_style_name}

---
{yaml.dump(slide_yaml, allow_unicode=True)}
"""
        st.text_area("Slide Prompt", value=prompt_text, height=200)

# ----------------------------------------------------
# Tab 2: Video Overview (Pro)
# ----------------------------------------------------
with tab_video:
    st.subheader("Native Video Director's Monitor")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        # Video 專屬的微調參數
        st.markdown("###### 導演微調")
        pacing = st.select_slider("剪輯節奏", options=["Slow", "Medium", "Fast"], value="Slow" if "莊嚴" in style_data['mood'] else "Medium")
        
        # 自動判斷是否開啟古物模式
        is_historical = "希伯來" in selected_style_name or "埃及" in selected_style_name or "兩河" in selected_style_name
        enhance_historical = st.checkbox("古物增強模式 (優先展示文物)", value=is_historical)

        video_yaml = {
            "type": "Native Video Directive",
            "meta": {"topic": global_topic, "keywords": global_keywords},
            "style_framework": selected_style_name,
            "art_direction": {
                "theme": f"{selected_style_name} - {style_data['visual_elements']}",
                "mood": style_data['mood'],
                "historical_mode": enhance_historical
            },
            "content_strategy": {
                "visual_priority": style_data['video_focus'],
                "highlight_keywords": global_keywords
            },
            "production": {"pacing": pacing}
        }

    with col2:
        st.caption("複製此 YAML 給 NotebookLM Video Overview")
        st.code(yaml.dump(video_yaml, allow_unicode=True), language='yaml')
        
        prompt_text = f"""請作為 Video Overview 的藝術總監。
主題：{global_topic}
風格：{selected_style_name}

請依照 YAML 指令，優先展示與「{global_keywords}」相關的素材。
---
{yaml.dump(video_yaml, allow_unicode=True)}
"""
        st.text_area("Video Prompt", value=prompt_text, height=200)

# ----------------------------------------------------
# Tab 3: Infographic
# ----------------------------------------------------
with tab_info:
    st.subheader("Infographic Generation")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        # Info 專屬參數
        struct_name = st.selectbox("圖表架構", list(INFO_STRUCTURES.keys()))
        struct_data = INFO_STRUCTURES[struct_name]
        
        info_yaml = {
            "type": "Infographic",
            "meta": {"topic": global_topic, "keywords": global_keywords},
            "framework": f"{struct_name} ({selected_style_name})",
            "canvas": struct_data['canvas'],
            "visual_style": {
                "palette": style_data['palette'],
                "elements": style_data['visual_elements'],
                "mood": style_data['mood']
            }
        }

    with col2:
        st.caption("複製此 YAML 給 NotebookLM")
        st.code(yaml.dump(info_yaml, allow_unicode=True), language='yaml')
        
        prompt_text = f"""請將筆記轉化為資訊圖表企劃。
主題：{global_topic}
架構：{struct_name}
風格：{selected_style_name}

---
{yaml.dump(info_yaml, allow_unicode=True)}
"""
        st.text_area("Infographic Prompt", value=prompt_text, height=200)
