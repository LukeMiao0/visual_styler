import streamlit as st
import yaml

# 設定頁面配置
st.set_page_config(layout="wide", page_title="NotebookLM Visual Architect v2.1", page_icon="🎨")

# ==========================================
# 1. 數據庫定義 (Presets)
# ==========================================

# --- 投影片預設 (Slide Presets) ---
SLIDE_PRESETS = {
    "希伯來盟約 (Hebrew Covenant)": {
        "description": "史詩感、羊皮卷、金/藍/紅配色，適合歷史與宗教敘事。",
        "brand": {"name": "Covenant & Journey", "tone": "史詩、神聖", "voice": "先知性敘事"},
        "visual_prompts": {
            "art_direction": "Biblical epic, Rembrandt lighting, oil painting texture",
            "background": "Aged parchment texture with ancient maps",
            "elements": "Burning bush, desert dunes, stone tablets"
        },
        "layout_intent": {
            "logic_1": "revelation: descending-light (光從上方照下)",
            "logic_2": "journey: map-overlay (地圖路徑疊加)",
            "logic_3": "law: twin-tablets (石版左右並列)"
        },
        "typography": {"font": "Noto Serif TC", "style": "Calligraphic"},
        "palette": {"primary": "#F3E5AB (羊皮卷)", "accent": "#0038B8 (提吉勒藍)"}
    },
    "瑞士國際主義 (Swiss Style)": {
        "description": "極簡、網格、無襯線字體，適合數據報告與學術分析。",
        "brand": {"name": "Helvetica Standard", "tone": "理性、客觀", "voice": "資訊優先"},
        "visual_prompts": {
            "art_direction": "Minimalist photography, high contrast, neutral lighting",
            "background": "Solid white or pure black",
            "elements": "Abstract geometric shapes, clean lines"
        },
        "layout_intent": {
            "logic_1": "grid: modular-12-col (模組化網格)",
            "logic_2": "contrast: scale-typography (巨大字級對比)",
            "logic_3": "data: naked-charts (極簡圖表)"
        },
        "typography": {"font": "Noto Sans TC", "style": "Black/Heavy"},
        "palette": {"primary": "#FFFFFF (白)", "accent": "#FF3B30 (瑞士紅)"}
    },
    "現代商務 (Modern Tech)": {
        "description": "深色模式、霓虹點綴、玻璃擬態，適合科技與商業提案。",
        "brand": {"name": "Tech Core", "tone": "專業、前衛", "voice": "數據驅動"},
        "visual_prompts": {
            "art_direction": "Tech-noir, glassmorphism, 3D isometric",
            "background": "Dark blue gradients, data flow lines",
            "elements": "Floating interfaces, glowing nodes"
        },
        "layout_intent": {
            "logic_1": "focus: bento-box (便當盒式佈局)",
            "logic_2": "compare: split-screen (左右分割)",
            "logic_3": "highlight: neon-frame (霓虹邊框)"
        },
        "typography": {"font": "Taipei Sans TC", "style": "Bold"},
        "palette": {"primary": "#0A0E14 (深藍黑)", "accent": "#00F0FF (螢光青)"}
    }
}

# --- 資訊圖表預設 (Infographic Presets) ---
# [FIX] 這裡的 density 值必須與下方 st.select_slider 的 options 完全一致
INFO_PRESETS = {
    "長卷軸敘事 (Long-form Scroll)": {
        "description": "適合講述歷史演變、流程步驟或時間軸 (Timeline)。",
        "canvas": {
            "ratio": "1:4 (Vertical Long)",
            "flow": "Top-down (由上而下)",
            "density": "Medium (平衡)"  # [FIXED]
        },
        "structure": {
            "header": "Hero Title + Intro illustration",
            "body": "Zig-zag path or Central timeline line",
            "footer": "Call to action + Sources"
        },
        "viz_style": "Icon-heavy with connecting lines"
    },
    "數據儀表板 (Data Dashboard)": {
        "description": "單頁高密度數據展示，適合年度回顧、比較分析。",
        "canvas": {
            "ratio": "4:3 or 1:1 (Poster)",
            "flow": "Modular / Grid (模組化)",
            "density": "High (密集)"    # [FIXED]
        },
        "structure": {
            "header": "Big KPI Numbers",
            "body": "Bento-box grid with Charts (Bar, Pie, Map)",
            "footer": "Key Insights summary"
        },
        "viz_style": "Flat vectors, Clean charts"
    },
    "對照比較圖 (Comparison / Versus)": {
        "description": "左右對決，適合 A/B 測試、優缺點分析、古今對照。",
        "canvas": {
            "ratio": "16:9 or 1:1",
            "flow": "Split Center (中線分割)",
            "density": "Low (極簡)"      # [FIXED]
        },
        "structure": {
            "header": "Central Topic Title",
            "body": "Two distinct columns with contrasting background colors",
            "footer": "Verdict / Conclusion"
        },
        "viz_style": "Symmetrical layout, distinct color coding"
    }
}

# ==========================================
# 2. 介面邏輯 (UI Logic)
# ==========================================

# --- 側邊欄 ---
st.sidebar.title("🎨 Visual Architect")
mode = st.sidebar.radio("請選擇生成模式", ["📽️ 投影片 (Slides)", "📊 資訊圖表 (Infographics)"], index=1)

st.sidebar.divider()

# 根據模式載入不同的預設值
if mode == "📽️ 投影片 (Slides)":
    st.sidebar.subheader("投影片風格")
    preset_key = st.sidebar.selectbox("載入模板", list(SLIDE_PRESETS.keys()))
    current_preset = SLIDE_PRESETS[preset_key]
    is_infographic = False
else:
    st.sidebar.subheader("資訊圖表架構")
    # 資訊圖表需要先選「架構」，再選「視覺風格」
    info_struct_key = st.sidebar.selectbox("版面架構", list(INFO_PRESETS.keys()))
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("視覺風格 (沿用)")
    # 讓用戶可以使用投影片定義好的視覺風格 (如希伯來風) 套用到資訊圖表上
    style_key = st.sidebar.selectbox("視覺風格", list(SLIDE_PRESETS.keys()))
    
    info_preset = INFO_PRESETS[info_struct_key]
    style_preset = SLIDE_PRESETS[style_key]
    is_infographic = True

# ==========================================
# 3. 主畫面內容
# ==========================================

st.title(f"NotebookLM {mode.split(' ')[1]} 生成器")
st.caption(current_preset['description'] if not is_infographic else info_preset['description'])

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 🛠️ 參數設定")
    
    if not is_infographic:
        # === 投影片設定模式 ===
        tab_brand, tab_visual, tab_layout = st.tabs(["品牌語氣", "視覺與圖像", "版型意圖"])
        
        with tab_brand:
            brand_name = st.text_input("品牌名稱", value=current_preset['brand']['name'])
            brand_tone = st.text_input("語氣", value=current_preset['brand']['tone'])
        
        with tab_visual:
            art_dir = st.text_area("藝術指導", value=current_preset['visual_prompts']['art_direction'])
            bg_prompt = st.text_area("背景指令", value=current_preset['visual_prompts']['background'])
            
        with tab_layout:
            st.info("定義每一頁的版型選擇邏輯")
            l_intent = current_preset['layout_intent']
            logic_1 = st.text_input("邏輯 1", value=l_intent['logic_1'])
            logic_2 = st.text_input("邏輯 2", value=l_intent['logic_2'])
            logic_3 = st.text_input("邏輯 3", value=l_intent['logic_3'])
            
            # 建構 Slide YAML
            final_yaml = {
                "type": "Presentation Slides",
                "framework": preset_key,
                "brand": {"name": brand_name, "tone": brand_tone},
                "visual_prompts": {"art_direction": art_dir, "background": bg_prompt},
                "layout": {"selection_logic": [logic_1, logic_2, logic_3]},
                "typography": current_preset['typography'],
                "palette": current_preset['palette']
            }

    else:
        # === 資訊圖表設定模式 ===
        tab_canvas, tab_struct, tab_style = st.tabs(["畫布與動線", "結構模組", "視覺風格"])
        
        with tab_canvas:
            st.info("設定圖表的物理尺寸與閱讀方向")
            canvas_ratio = st.selectbox("長寬比", ["1:4 (Vertical Long)", "16:9 (Horizontal)", "1:1 (Square)", "A4 Vertical"], index=0)
            canvas_flow = st.text_input("閱讀動線", value=info_preset['canvas']['flow'])
            
            # [FIXED] 確保這裡的 options 與 INFO_PRESETS 中的 density 值完全一致
            canvas_density = st.select_slider(
                "資訊密度", 
                options=["Low (極簡)", "Medium (平衡)", "High (密集)"], 
                value=info_preset['canvas']['density']
            )

        with tab_struct:
            st.success("定義圖表的內容區塊")
            struct_head = st.text_input("頭部 (Header)", value=info_preset['structure']['header'])
            struct_body = st.text_input("主體 (Body)", value=info_preset['structure']['body'])
            struct_foot = st.text_input("尾部 (Footer)", value=info_preset['structure']['footer'])
            viz_style = st.text_input("圖表風格", value=info_preset['viz_style'])

        with tab_style:
            st.warning(f"當前套用風格：{style_key}")
            # 允許微調從 Slide Preset 繼承來的風格
            infographic_palette = st.text_input("配色方案", value=f"Primary: {style_preset['palette']['primary']} / Accent: {style_preset['palette']['accent']}")
            infographic_mood = st.text_area("氛圍描述", value=style_preset['visual_prompts']['art_direction'])

        # 建構 Infographic YAML
        final_yaml = {
            "type": "Infographic",
            "framework": f"{info_struct_key} + {style_key}",
            "canvas": {
                "dimensions": canvas_ratio,
                "visual_flow": canvas_flow,
                "information_density": canvas_density
            },
            "composition": {
                "header_section": struct_head,
                "body_section": struct_body,
                "footer_section": struct_foot
            },
            "visual_style": {
                "art_direction": infographic_mood,
                "palette_rules": infographic_palette,
                "chart_style": viz_style
            },
            "rules": [
                "確保字體大小能區分層級 (Title > Sub > Body)",
                "保持視覺動線流暢，不跳躍",
                "使用圖示 (Icons) 來輔助文字說明"
            ]
        }

# ==========================================
# 4. 輸出生成
# ==========================================

yaml_str = yaml.dump(final_yaml, allow_unicode=True, sort_keys=False)

with col2:
    st.markdown("#### 📝 YAML 指令 (Output)")
    st.caption("複製此代碼，貼入 NotebookLM")
    st.code(yaml_str, language='yaml')
    
    st.divider()
    
    st.markdown("#### 🚀 NotebookLM Prompt")
    user_topic = st.text_input("內容主題", placeholder="例如：以色列人出埃及路線圖、2024年Q4財報全覽")
    
    if is_infographic:
        prompt_text = f"""請依據以下的 YAML 設定檔，將我的筆記內容轉化為一張「{info_struct_key}」的資訊圖表 (Infographic) 設計企劃。

請詳細描述這張圖表的：
1. **版面構成 (Composition)**：從上到下（或由左至右）的具體區塊安排。
2. **視覺元素**：建議使用的圖標、插圖以及圖表類型（參考 visual_style）。
3. **數據視覺化**：如何將筆記中的關鍵數據轉化為視覺圖形（參考 composition）。
4. **AI 繪圖指令**：給 Midjourney/DALL-E 的詳細 Prompt，用於生成這張長圖的底圖或素材。

---
{yaml_str}
"""
    else:
        prompt_text = f"""請依據以下的 YAML 設定檔，將我的筆記內容轉化為一份投影片大綱。

請明確列出每一頁的：
1. 標題與內文。
2. 建議版型 (Layout)。
3. AI 繪圖指令 (Visual Prompts)。

---
{yaml_str}
"""

    with st.expander("查看完整指令", expanded=True):
        st.text_area("Prompt", value=prompt_text, height=250)
