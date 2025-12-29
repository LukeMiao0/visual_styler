import streamlit as st
import yaml

# 設定頁面配置
st.set_page_config(layout="wide", page_title="NotebookLM Architect v7.7.1", page_icon="🏛️")

# ==========================================
# 1. 預設風格資料庫
# ==========================================
PRESETS = {
    "自定義 (Custom)": {"theme": "", "context": "", "audience": "", "colors": "", "imagery": ""},
    
    "希伯來盟約 (Hebrew Covenant)": {
        "theme": "Biblical Epic & Historical",
        "context": "聖經歷史教學、神學研討會",
        "audience": "神學生、教會會眾",
        "colors": "羊皮紙米黃 (#F3E5AB), 提吉勒藍 (#0038B8), 精金 (#D4AF37), 森林綠 (#1A7B4A)",
        "imagery": "油畫質感、林布蘭光影 (Chiaroscuro)、古卷特寫、岩石板岩質感 (Slate Texture)"
    },
    "古埃及風格 (Ancient Egyptian)": {
        "theme": "Monumental & Mysterious",
        "context": "古文明歷史展覽、博物館導覽",
        "audience": "歷史愛好者、遊客",
        "colors": "黑曜石黑 (#0F0F0F), 黃金 (#D4AF37), 青金石藍 (#191970), 鮮豔黃 (#FECD43)",
        "imagery": "壁畫風格 (Frescoes)、金字塔幾何結構、斑駁的石灰岩質感"
    },
    "地中海希臘 (Mediterranean Greek)": {
        "theme": "Classical Rationalism",
        "context": "哲學研討會、藝術史",
        "audience": "人文學者",
        "colors": "愛琴海藍 (#0047AB), 大理石白 (#F2F0E6), 深靛紫 (#5A3F9B)",
        "imagery": "斑駁的馬賽克拼貼 (Mottled Mosaic)、大理石雕像光影、手寫書法質感"
    },
    "兩河流域 (Mesopotamian)": {
        "theme": "Cradle of Civilization",
        "context": "文明起源探討",
        "audience": "考古愛好者",
        "colors": "未燒泥土色 (#C19A6B), 燒磚紅 (#8B4513), 森林綠 (#1A7B4A)",
        "imagery": "楔形文字泥板 (Cuneiform Clay Tablet)、浮雕質感、河流航拍"
    },
    "商務辦公 (Corporate Pro)": {
        "theme": "Modern Professional",
        "context": "年度財報",
        "audience": "投資人",
        "colors": "深藍黑 (#0A0E14), 螢光青 (#00F0FF), 極致白, 鮮豔黃 (#FECD43)",
        "imagery": "玻璃擬態、抽象科技線條、高解析度數據儀表板"
    }
}

# ==========================================
# 2. 核心邏輯：Master Prompt 生成器
# ==========================================
def get_master_spec_text(theme, context, audience, colors, imagery):
    return f"""
# Role: Google NotebookLM Visual Director
你現在是 Google NotebookLM 的首席視覺總監。
你的任務是根據「設計需求簡報 (Design Brief)」，定義一份 YAML 設計規範，並依據此規範執行後續任務。

---
## PART 1: Design Brief (核心規範)
1. **[核心風格]**: {theme}
2. **[簡報用途]**: {context}
3. **[目標受眾]**: {audience}
4. **[色彩偏好]**: {colors}
5. **[圖像風格]**: {imagery}

請在內心建立一份包含 `global_settings`, `palette` (Hex Codes), `typography`, `visual_assets` (Midjourney Prompts), `layout_templates` 的完整設計規範。

**[創意轉化原則 (Creative Translation Logic)]**
請發揮設計專業，將抽象形容詞轉化為具體的視覺參數：
- 若提到「復古/歷史」，請在 `visual_assets` 加入「噪點 (Noise)、舊照片質感、斑駁紋理 (Distressed texture)」。
- 若提到「博物館/神聖」，請在 `palette` 加入「深靛紫 (#5A3F9B)、森林綠 (#1A7B4A)」等厚重色系，並強調光影氛圍。
- 若提到「科技/現代」，請在 `visual_identity` 加入「網格 (Grid)、光暈 (Glow)、玻璃擬態」。
- 若提到「引用/經文」，請定義字體為「書法體 (Calligraphic)」或「手寫體 (Handwritten)」。

接下來的所有產出，都必須嚴格遵守此規範。
---
"""

# ==========================================
# 3. UI 介面
# ==========================================

st.sidebar.title("🏛️ Visual Architect v7.7.1")
st.sidebar.caption("Bug Fix Edition")

selected_preset = st.sidebar.selectbox("快速載入預設", list(PRESETS.keys()))
preset_data = PRESETS[selected_preset]

st.sidebar.divider()
st.sidebar.header("1. 設計簡報 (Design Brief)")
in_theme = st.sidebar.text_input("1. 核心風格", value=preset_data['theme'])
in_context = st.sidebar.text_input("2. 使用情境", value=preset_data['context'])
in_audience = st.sidebar.text_input("3. 目標受眾", value=preset_data['audience'])
in_colors = st.sidebar.text_input("4. 色彩偏好", value=preset_data['colors'])
in_imagery = st.sidebar.text_area("5. 圖像風格", value=preset_data['imagery'], height=80)

st.sidebar.divider()
st.sidebar.header("2. 內容定義")
in_topic = st.sidebar.text_input("內容主題", placeholder="例如：以色列人出埃及路線")
in_keywords = st.sidebar.text_area("關鍵字", placeholder="例如：西奈山, 盟約, 40年曠野", height=80)

st.title("NotebookLM Generator")

if not in_theme:
    st.warning("👈 請先在左側填寫設計簡報。")

# Tabs
tab_slide, tab_video, tab_info, tab_spec = st.tabs(["📽️ Slide Deck", "🎬 Video Overview", "📊 Infographic", "🧬 Master Spec"])

# 準備 Master Spec 文本
master_spec_text = get_master_spec_text(in_theme, in_context, in_audience, in_colors, in_imagery)

# ----------------------------------------------------
# Tab 1: Slide Deck
# ----------------------------------------------------
with tab_slide:
    st.subheader("Slide Deck Generator")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("##### ⚙️ 原子化設計參數")
        
        # 1. 網格與佈局
        with st.expander("📐 1. 網格與佈局", expanded=True):
            grid_system = st.selectbox("Grid 系統", ["12-Column Modular", "Asymmetric", "Golden Ratio", "Single Column"])
            img_txt_ratio = st.select_slider("圖文比例", ["文字為主", "平衡", "圖像為主"], value="平衡")
            layout_hierarchy = st.text_input("版面層級", value="Visual > Headline > Data")

        # 2. 字體與層級
        with st.expander("🔠 2. 字體與層級", expanded=True):
            h1_style = st.text_input("標題 (H1/H2)", value="Serif, Bold" if "Hebrew" in selected_preset else "Sans-serif, Heavy")
            body_style = st.text_input("內文 (Body)", value="Serif, Readable" if "Hebrew" in selected_preset else "Sans-serif")
            list_style = st.selectbox("列表樣式", ["Icon List", "Bullet Points", "Numbered", "No Bullets"])
            quote_style = st.selectbox("引文樣式 (Quote)", 
                                     ["Handwritten Font (手寫體)", "Calligraphic Script (書法體)", "Oversized Quote Marks (巨型引號)", "Modern Blockquote"])
        
        # 3. 視覺與背景
        with st.expander("🎨 3. 視覺與背景", expanded=True):
            bg_style = st.text_input("背景風格", value="Textured Parchment/Slate" if "Hebrew" in selected_preset else "Solid/Gradient")
            color_usage = st.text_input("色彩策略", value="Accent: Vivid Yellow (#FECD43) & Forest Green (#1A7B4A)")
            decorations = st.text_input("裝飾元素", value="Ancient Border Patterns" if "Hebrew" in selected_preset else "Minimalist Lines")

        st.markdown("---")
        include_master_slide = st.checkbox("📥 包含 Master Design Specs", value=True, key="inc_master_slide")

        # Slide YAML
        slide_yaml_instruction = {
            "type": "Presentation Slides",
            "content_context": {"topic": in_topic, "keywords": in_keywords},
            "design_tokens": {
                "grid_system": grid_system,
                "composition_ratio": img_txt_ratio,
                "visual_hierarchy": layout_hierarchy
            },
            "typography_rules": {
                "headings": h1_style,
                "body_text": body_style,
                "list_format": list_style,
                "quote_format": quote_style
            },
            "visual_components": {
                "background": bg_style,
                "decorations": decorations,
                "color_application": color_usage
            }
        }

        # Prompt with Clean Output Rules
        slide_task_text = f"""
## PART 2: Execution Task (Slide Deck)
請依據 PART 1 設計規範，並嚴格遵守以下參數生成大綱。

**[原子化設計參數]**
{yaml.dump(slide_yaml_instruction, allow_unicode=True)}

**[輸出格式嚴格規範 (Clean Output Rules)]**
1. **標題去符號化**：標題 **嚴禁** 使用 Markdown 的 `#` 符號。請直接寫出標題文字，並確保它是該頁的第一行（可加粗）。
2. **去標籤化**：內容中 **勿** 出現「標題：」、「內文：」等提示詞。
3. **引文處理**：若有引文，請註明使用「{quote_style}」字體。
4. **裝飾指示**：請明確指出每頁的「裝飾元素」（如：{decorations}）。

**輸出要求**：
請列出每一頁的完整內容（純文字格式，不含 #）與 AI 繪圖指令。
"""
        final_slide_prompt = master_spec_text + slide_task_text if include_master_slide else slide_task_text

    with col2:
        st.text_area("🚀 複製此指令", value=final_slide_prompt, height=750)

# ----------------------------------------------------
# Tab 2: Video Overview (Bug Fix: Pacing Value)
# ----------------------------------------------------
with tab_video:
    st.subheader("Video Director")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("##### ⚙️ Video 參數設定")
        
        # [FIX] 這裡修正了 value 必須與 options 列表中的項目完全一致
        pacing = st.select_slider("剪輯節奏", 
                                options=["Slow (沉思)", "Medium (敘事)", "Fast (快閃)"], 
                                value="Medium (敘事)") 
                                
        narrator = st.radio("旁白風格", ["Invisible Narrator", "AI Virtual Host", "Kinetic Text Only"], index=0)
        
        is_historical = "歷史" in in_context or "史" in in_theme or "Bible" in in_theme or "Ancient" in selected_preset
        enhance_historical = st.checkbox("🏛️ 古物增強模式 (優先展示文物)", value=is_historical)
        
        st.markdown("---")
        include_master_video = st.checkbox("📥 包含 Master Design Specs", value=True, key="inc_master_video")

        video_task_text = f"""
## PART 2: Execution Task (Video Script)
請作為 Video Overview 的藝術總監。
請將 PART 1 定義的視覺風格應用於影片生成。

**[影片專屬設定]**
- **剪輯節奏**: {pacing}
- **旁白形式**: {narrator}
- **古物增強模式**: {'開啟 (請優先展示古卷、地圖、文物)' if enhance_historical else '關閉'}
- **內容策略**: 優先展示「{in_keywords}」相關素材。

請生成一份包含時間碼、畫面描述與 AI 生成指令的分鏡表。
"""
        final_video_prompt = master_spec_text + video_task_text if include_master_video else video_task_text

    with col2:
        st.text_area("🚀 複製此指令", value=final_video_prompt, height=550)

# ----------------------------------------------------
# Tab 3: Infographic
# ----------------------------------------------------
with tab_info:
    st.subheader("Infographic")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("##### ⚙️ Info 參數設定")
        struct = st.selectbox("圖表架構", ["長卷軸 (Long Scroll)", "儀表板 (Dashboard)", "比較圖 (Comparison)"])
        canvas_ratio = st.selectbox("畫布比例", ["1:4 (手機長圖)", "16:9 (寬螢幕)", "4:3 (海報)"])
        density = st.select_slider("資訊密度", ["Low", "Medium", "High"], value="Medium")

        st.markdown("---")
        include_master_info = st.checkbox("📥 包含 Master Design Specs", value=True, key="inc_master_info")

        info_task_text = f"""
## PART 2: Execution Task (Infographic)
請依據 PART 1 的設計規範，設計一張資訊圖表。

**[圖表專屬設定]**
- **架構類型**: {struct}
- **畫布比例**: {canvas_ratio}
- **資訊密度**: {density}
- **主題**: {in_topic}

請描述版面構成、數據視覺化方式與所需的插圖指令。
"""
        final_info_prompt = master_spec_text + info_task_text if include_master_info else info_task_text

    with col2:
        st.text_area("🚀 複製此指令", value=final_info_prompt, height=550)

# ----------------------------------------------------
# Tab 4: Master Spec Preview
# ----------------------------------------------------
with tab_spec:
    st.subheader("🧬 Master Design Spec")
    st.caption("這是隱藏在 Prompt 開頭的「核心大腦」，負責創意轉化。")
    st.code(master_spec_text, language='markdown')
