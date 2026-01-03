# NotebookLM Visual Architect v8.4 (Global Civilizations & Design Icons)
# Updated: 2026-01-04

import streamlit as st
import yaml

# 設定頁面配置
st.set_page_config(layout="wide", page_title="NotebookLM Architect v8.4", page_icon="🏛️")

# ==========================================
# 1. 預設風格資料庫 (全方位擴充版)
# ==========================================
STANDARD_PRESETS = {
    "自定義 (Custom)": {
        "theme": "", "context": "", "audience": "", "colors": "", "imagery": "",
        "preview_image": "https://placehold.co/600x400/EEE/31343C?text=Custom+Style"
    },

    # -------------------------------
    # [Series A] 古文明與歷史
    # -------------------------------
    "古埃及尼羅河 (Egypt & Nile)": {
        "theme": "Monumental Stone & Life-giving River",
        "context": "古文明展覽、歷史講座、神話解析",
        "audience": "歷史愛好者、博物館遊客",
        "colors": "黑曜石黑 (#0F0F0F), 尼羅河藍 (#4F759B), 黃金 (#D4AF37), 莎草綠 (#6B8C42)",
        "imagery": "石碑刻字 (Stele), 紙莎草紋理, 蓮花邊框, 側面人像壁畫 (Frescoes), 太陽船",
        "preview_image": "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?auto=format&fit=crop&w=600&q=80"
    },
    "兩河流域風情 (Mesopotamia & Babylon)": {
        "theme": "Cuneiform Clay & Ishtar Gate",
        "context": "文明起源、法律史、聖經背景",
        "audience": "考古迷、神學生",
        "colors": "未燒泥土色 (#C19A6B), 琉璃磚藍 (#26619C), 燒磚紅 (#8B4513), 獅子金 (#C5A059)",
        "imagery": "泥板壓印質感 (Imprinted Clay), 楔形文字, 伊什塔爾門琉璃磚 (Glazed Brick), 神塔階梯",
        "preview_image": "https://images.unsplash.com/photo-1599707367072-cd6ad66acc40?auto=format&fit=crop&w=600&q=80"
    },
    "地中海希臘 (Mediterranean Greek)": {
        "theme": "Classical Rationalism & Aegean Sea",
        "context": "哲學研討、藝術史、建築賞析",
        "audience": "人文學者、大學生",
        "colors": "愛琴海藍 (#0047AB), 大理石白 (#F2F0E6), 橄欖綠 (#708238), 陶土紅 (#CC4E5C)",
        "imagery": "多立克柱式 (Doric Columns), 斑駁馬賽克拼貼, 白色大理石光影, 幾何迴紋 (Meander)",
        "preview_image": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=600&q=80"
    },
    "希伯來盟約 (Hebrew Covenant)": {
        "theme": "Biblical Epic & Sacred History",
        "context": "聖經教學、教會聚會",
        "audience": "信徒、神學研究者",
        "colors": "羊皮紙米黃 (#F3E5AB), 提吉勒藍 (#0038B8), 精金 (#D4AF37), 聖約紅 (#8B0000)",
        "imagery": "油畫質感 (Chiaroscuro), 羊皮古卷, 岩石刻字, 猶太印章",
        "preview_image": "https://images.unsplash.com/photo-1473177104440-ffee2f376098?auto=format&fit=crop&w=600&q=80"
    },

    # -------------------------------
    # [Series B] 東方美學
    # -------------------------------
    "東方瓷器韻味 (Oriental Porcelain)": {
        "theme": "Imperial Craft & Glazed Aesthetics",
        "context": "藝術策展、高端品牌發布、文化沙龍",
        "audience": "收藏家、設計師",
        "colors": "骨瓷白 (#F8F6F5), 青花藍 (#0047AB), 胭脂紅 (#E91E63), 豆青釉 (#93C0A4)",
        "imagery": "高光釉面質感 (Glossy Glaze), 冰裂紋 (Ice Crackle), 朱紅印章 (Seals), 極致細膩的留白",
        "preview_image": "https://images.unsplash.com/photo-1615456942691-230b77742d65?auto=format&fit=crop&w=600&q=80"
    },
    "園林與寫意山水 (Garden & Ink Wash)": {
        "theme": "Literati Garden & Poetic Void",
        "context": "文學講座、茶道、東方建築",
        "audience": "文人雅士、文化學者",
        "colors": "宣紙白 (#F5F5F5), 濃墨黑 (#1A1A1A), 竹青 (#5F7A61), 朱砂紅 (#C83C23)",
        "imagery": "水墨暈染 (Ink Diffusion), 月洞門構圖, 太湖石紋理, 雲霧繚繞, 毛筆筆觸",
        "preview_image": "https://images.unsplash.com/photo-1547619292-240402b5ae5d?auto=format&fit=crop&w=600&q=80"
    },

    # -------------------------------
    # [Series C] 現代設計經典
    # -------------------------------
    "瑞士極簡 (Swiss International)": {
        "theme": "International Typographic Style",
        "context": "設計展覽、建築匯報、學術發表",
        "audience": "設計師、極簡主義者",
        "colors": "純白 (#FFFFFF), 極致黑 (#000000), 瑞士紅 (#FF3B30)",
        "imagery": "嚴謹網格 (Grid Systems), Helvetica 字體排版, 非對稱佈局, 客觀攝影",
        "preview_image": "https://images.unsplash.com/photo-1509343256512-d77a5cb3791b?auto=format&fit=crop&w=600&q=80"
    },
    "包豪斯工業風 (Bauhaus Industrial)": {
        "theme": "Form Follows Function",
        "context": "工業設計、藝術史、創意提案",
        "audience": "建築師、藝術學生",
        "colors": "原色紅 (#D92B2B), 原色藍 (#1E3D99), 原色黃 (#F2C94C), 水泥灰 (#F0F0F0)",
        "imagery": "幾何圖形 (圓/方/三角), 鋼管與混凝土質感, 結構主義拼貼, 斜向排版",
        "preview_image": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?auto=format&fit=crop&w=600&q=80"
    },
    "美式諮詢風格 (MBB Consulting)": {
        "theme": "Elite Strategy & Data Logic",
        "context": "戰略規劃、董事會匯報 (C-Suite)",
        "audience": "CEO、高階主管、投資人",
        "colors": "海軍深藍 (#051C2C), 專業灰 (#F2F2F2), 活力紅 (#CC0000) 或 諮詢綠 (#2D6943)",
        "imagery": "瀑布圖 (Waterfall Charts), 簡潔邊框 (Clean Borders), 行動標題 (Action Titles), 高密度資訊圖表",
        "preview_image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=600&q=80"
    }
}

# ==========================================
# 2. Session State 管理
# ==========================================
if 'custom_presets' not in st.session_state:
    st.session_state['custom_presets'] = {}

def get_all_presets():
    return {**STANDARD_PRESETS, **st.session_state['custom_presets']}

all_presets = get_all_presets()

if 'theme' not in st.session_state:
    default_key = list(STANDARD_PRESETS.keys())[1] 
    data = STANDARD_PRESETS[default_key]
    st.session_state.update({
        'theme': data.get('theme', ''),
        'context': data.get('context', ''),
        'audience': data.get('audience', ''),
        'colors': data.get('colors', ''),
        'imagery': data.get('imagery', ''),
        'topic': '',
        'keywords': ''
    })

def on_preset_change():
    selected_key = st.session_state.selected_preset_key
    if selected_key in all_presets:
        data = all_presets[selected_key]
        st.session_state.update({
            'theme': data.get('theme', ''),
            'context': data.get('context', ''),
            'audience': data.get('audience', ''),
            'colors': data.get('colors', ''),
            'imagery': data.get('imagery', ''),
            'topic': data.get('topic', st.session_state.topic),
            'keywords': data.get('keywords', st.session_state.keywords)
        })

# ==========================================
# 3. 核心邏輯：Master Prompt 生成器
# ==========================================

def get_master_spec_text(theme, context, audience, colors, imagery):
    return f"""
# Role: Google NotebookLM Visual Director (v8.4 Universal Framework)
你現在是 Google NotebookLM 的首席視覺總監。
你的任務是根據「設計需求簡報 (Design Brief)」，定義一份 YAML 設計規範，並依據此規範執行後續任務。

---
## PART 1: Design Brief (核心規範)
1. **[核心風格]**: {theme}
2. **[簡報用途]**: {context}
3. **[目標受眾]**: {audience}
4. **[色彩偏好]**: {colors}
5. **[圖像風格]**: {imagery}

請在內心建立一份包含 `global_settings`, `palette` (Hex Codes), `typography`, `visual_assets` 的完整設計規範。

**[v8.4 質感與邏輯增強 (Texture & Logic Enforcement)]**
請嚴格遵守以下針對不同風格體系的特殊規定：

1.  **材質化 (Materiality)**：
    - 若是 **古文明 (Ancient)**：標題必須呈現「石刻 (Chiselled)」、「泥板壓印」或「手寫古卷」質感。
    - 若是 **東方美學 (Eastern)**：強調「宣紙暈染」、「釉面光澤」或「朱紅印章」。
    - 若是 **現代設計 (Modern)**：強調「玻璃擬態」、「網格線」或「混凝土質感」。

2.  **容器與邊框 (Container & Border)**：
    - **經文/引言**：必須放置在符合時代背景的容器中（如：羊皮卷、竹簡、現代對話框）。
    - **重要結論**：必須使用風格化的邊框（如：蓮花紋飾、迴紋、粗黑線框）來強調。

3.  **數量感知佈局 (Count-Aware Layout)**：
    - **動態卡片生成**：請分析內容中的「項目數量」。
    - 例如：若內容有 3 個重點，版型自動設定為 **「3-Column Grid」**；若有 4 個階段，設定為 **「2x2 Grid」**。

接下來的所有產出，都必須嚴格遵守此規範。
---
"""

# ==========================================
# 4. UI 介面
# ==========================================

st.sidebar.title("🏛️ Visual Architect v8.4")
st.sidebar.caption("Global Civilizations & Design Icons")

# --- 載入區 ---
st.sidebar.header("1. 風格選擇 (Style Selection)")
selected_preset_key = st.sidebar.selectbox(
    "選擇預設風格", 
    list(all_presets.keys()), 
    key="selected_preset_key",
    on_change=on_preset_change,
    index=list(all_presets.keys()).index("希伯來盟約 (Hebrew Covenant)") if "希伯來盟約 (Hebrew Covenant)" in all_presets else 0
)
current_preset_data = all_presets[selected_preset_key]

# 顯示預覽圖
if 'preview_image' in current_preset_data:
    with st.sidebar.container():
        st.markdown(
            f"""
            <style>
            .style-preview img {{
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0;
                margin-bottom: 10px;
            }}
            </style>
            <div class="style-preview"></div>
            """, 
            unsafe_allow_html=True
        )
        st.image(current_preset_data['preview_image'], caption=f"Style: {selected_preset_key}", use_column_width=True)

st.sidebar.divider()

# --- 編輯區 ---
st.sidebar.header("2. 設計簡報 (Design Brief)")
in_theme = st.sidebar.text_input("核心風格", key="theme")
in_context = st.sidebar.text_input("使用情境", key="context")
in_audience = st.sidebar.text_input("目標受眾", key="audience")
in_colors = st.sidebar.text_input("色彩偏好", key="colors")
in_imagery = st.sidebar.text_area("圖像風格", key="imagery", height=80)

st.sidebar.header("3. 內容定義")
in_topic = st.sidebar.text_input("內容主題", key="topic", placeholder="例如：漢摩拉比法典的現代意義")
in_keywords = st.sidebar.text_area("關鍵字", key="keywords", placeholder="例如：以眼還眼, 社會正義, 泥板文獻", height=80)

st.sidebar.divider()

# --- 保存區 ---
st.sidebar.header("4. 保存配置")
if st.sidebar.button("💾 保存當前配置"):
    if in_topic and in_theme:
        style_name = selected_preset_key.split(' (')[0] if '(' in selected_preset_key else "Custom"
        safe_topic = in_topic[:10].replace(" ", "_")
        save_name = f"★ {style_name} - {safe_topic}"
        
        st.session_state['custom_presets'][save_name] = {
            "theme": in_theme, "context": in_context, "audience": in_audience,
            "colors": in_colors, "imagery": in_imagery, "topic": in_topic,
            "keywords": in_keywords,
            "preview_image": "https://placehold.co/600x400/EEE/31343C?text=User+Saved+Config"
        }
        st.sidebar.success(f"已保存：{save_name}")
        st.rerun()
    else:
        st.sidebar.error("請輸入風格與主題。")

# --- 主畫面 ---
st.title("NotebookLM Generator")

if not in_theme:
    st.warning("👈 請先在左側填寫設計簡報。")

# Tabs
tab_slide, tab_video, tab_info, tab_spec = st.tabs(["📽️ Slide Deck", "🎬 Video Overview", "📊 Infographic", "🧬 Master Spec"])

master_spec_text = get_master_spec_text(in_theme, in_context, in_audience, in_colors, in_imagery)

# ----------------------------------------------------
# Tab 1: Slide Deck
# ----------------------------------------------------
with tab_slide:
    st.subheader("Slide Deck Generator")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("##### ⚙️ 參數設定")
        
        # 智能預設值
        is_mbb = "MBB" in selected_preset_key or "Consulting" in in_theme
        is_ancient = "Ancient" in selected_preset_key or "Hebrew" in selected_preset_key or "Nile" in selected_preset_key
        
        default_grid = "Data-Heavy Grid (高密度)" if is_mbb else "Auto-Detect (根據項目數量)"
        default_hierarchy = "Action Title > Data > Conclusion" if is_mbb else "Visual > Headline > Data"
        default_quote = "Boxed Quote" if is_mbb else ("Ancient Scroll" if is_ancient else "Calligraphic")

        with st.expander("📐 佈局與字體", expanded=True):
            grid_system = st.selectbox("Grid 系統", ["Auto-Detect (根據項目數量)", "Bento Grid", "12-Column Modular", "Data-Heavy Grid"], index=3 if is_mbb else 0)
            layout_hierarchy = st.text_input("版面層級", value=default_hierarchy)
            quote_style = st.selectbox("引文/經文樣式", ["Ancient Scroll (古卷)", "Stone Tablet (石板)", "Calligraphic (書法)", "Handwritten (手寫)", "Professional Box (方框)"], index=4 if is_mbb else 0)
        
        with st.expander("🎨 視覺與裝飾", expanded=True):
            bg_style = st.text_input("背景風格", value="Textured (紋理)" if is_ancient else "Clean/Gradient")
            decorations = st.text_input("裝飾元素", value="Seals & Borders (印章與邊框)" if is_ancient else "Minimal Lines")

        st.markdown("---")
        include_master_slide = st.checkbox("📥 包含 Master Design Specs", value=True, key="inc_master_slide")

        slide_yaml_instruction = {
            "type": "Presentation Slides",
            "content_context": {"topic": in_topic, "keywords": in_keywords},
            "design_tokens": {
                "grid_logic": "Count-Aware (e.g., 4 points = 2x2 Grid)",
                "visual_hierarchy": layout_hierarchy
            },
            "typography_rules": {
                "quote_container": quote_style
            },
            "visual_components": {
                "background": bg_style,
                "decorations": decorations
            }
        }

        slide_task_text = f"""
## PART 2: Execution Task (Slide Deck)
請依據 PART 1 設計規範，生成投影片大綱。

**[原子化設計參數]**
{yaml.dump(slide_yaml_instruction, allow_unicode=True)}

**[輸出格式嚴格規範 (Clean Output Rules)]**
1. **去標籤化**：不要寫「標題：」、「Title:」等。直接輸出內容。
2. **標題格式**：標題請使用純文字（勿用 #）。{ '請使用 Action Title (完整的觀點句)' if is_mbb else '' }
3. **動態版型**：若內容有多個並列項目，請明確指示使用 **[X-Card Grid]** 版型。
4. **容器指令**：請為引言或重要結論標註 **[Container: {quote_style}]**。

請列出每一頁的完整內容與詳細的視覺/容器指令。
"""
        final_slide_prompt = master_spec_text + slide_task_text if include_master_slide else slide_task_text

    with col2:
        st.text_area("🚀 複製此指令", value=final_slide_prompt, height=750)

# ----------------------------------------------------
# Tab 2: Video Overview
# ----------------------------------------------------
with tab_video:
    st.subheader("Video Director")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("##### ⚙️ Video 設定")
        pacing = st.select_slider("剪輯節奏", ["Slow (沉思)", "Medium (敘事)", "Fast (快閃)"], value="Medium")
        # 智能判斷歷史模式
        is_historical = "Historical" in in_theme or "Ancient" in selected_preset_key or "Clay" in selected_preset_key or "Egypt" in selected_preset_key
        enhance_historical = st.checkbox("🏛️ 古物增強模式", value=is_historical)
        include_master_video = st.checkbox("📥 包含 Master Specs", value=True, key="inc_master_video")

        video_task_text = f"""
## PART 2: Execution Task (Video Script)
請作為 Video Overview 的藝術總監。

**[影片專屬設定]**
- **風格**: {in_theme}
- **節奏**: {pacing}
- **古物模式**: {'開啟 (優先展示古卷、文物、地圖)' if enhance_historical else '關閉'}
- **內容策略**: 優先展示 {in_keywords}。
- **文字質感**: 標題請呈現{ '石刻/金屬' if is_historical else '現代無襯線' }質感。

請生成包含時間碼、畫面描述與 AI 生成指令的分鏡表。
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
        st.markdown("##### ⚙️ Info 設定")
        default_struct_idx = 1 if is_mbb else 0
        struct = st.selectbox("架構", ["長卷軸 (Long Scroll)", "儀表板 (Dashboard)", "比較圖 (Comparison)"], index=default_struct_idx)
        include_master_info = st.checkbox("📥 包含 Master Specs", value=True, key="inc_master_info")

        info_task_text = f"""
## PART 2: Execution Task (Infographic)
請設計一張「{struct}」資訊圖表。

**[內容]**
- **主題**: {in_topic}
- **風格**: {in_theme}
- **裝飾**: 使用 {in_imagery.split(',')[0] if in_imagery else '標準'} 相關元素。

請描述版面構成與數據視覺化方式。
"""
        final_info_prompt = master_spec_text + info_task_text if include_master_info else info_task_text

    with col2:
        st.text_area("🚀 複製此指令", value=final_info_prompt, height=550)

# ----------------------------------------------------
# Tab 4: Master Spec Preview
# ----------------------------------------------------
with tab_spec:
    st.subheader("🧬 Master Design Spec")
    st.code(master_spec_text, language='markdown')
