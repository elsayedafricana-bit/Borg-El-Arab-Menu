import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="شركة برج العرب - نظام المنيوهات", layout="wide")

# دالة لقراءة الصورة وتحويلها لخلفية
def get_base64_img(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return ""

logo_path = "Picsart_25-11-20_15-08-39-076.png"
bin_str = get_base64_img(logo_path)

# 2. التنسيق المتقدم (CSS) - تحسين الوضوح 100%
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.96)),
                    url("data:image/png;base64,{bin_str}");
        background-size: 50%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* تنسيق الساعة والتاريخ */
    .time-date-box {{
        text-align: center;
        padding: 15px;
        background: #1d3557;
        color: white;
        border-radius: 15px;
        margin: 10px auto;
        width: fit-content;
        font-family: 'Cairo', sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}

    /* تنسيق الجدول ليكون فائق الوضوح */
    .main-table {{
        width: 100%;
        border-collapse: collapse;
        background-color: white !important;
        color: #000000 !important; /* لون أسود صريح */
        font-family: 'Cairo', sans-serif;
        margin-top: 20px;
    }}
    
    .main-table th {{
        background-color: #1d3557 !important;
        color: white !important;
        padding: 15px;
        font-size: 20px;
        border: 2px solid #457b9d;
    }}
    
    .main-table td {{
        padding: 12px;
        text-align: center;
        border: 2px solid #dee2e6;
        font-size: 18px;
        font-weight: 900 !important; /* خط سميك جداً */
        color: #000000 !important;
    }}

    /* الأزرار المجسمة */
    div.stButton > button {{
        height: 100px !important;
        width: 100% !important;
        border-radius: 20px !important;
        background: linear-gradient(145deg, #1d3557, #457b9d) !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2) !important;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# 3. الهيدر والساعة
st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
if os.path.exists(logo_path):
    st.image(logo_path, width=180)

st.markdown("<h1 style='color:#1d3557; font-family:Cairo; margin:0;'>منيو هات شركة برج العرب الجديدة</h1>", unsafe_allow_html=True)

# عرض الوقت والتاريخ
now = datetime.now()
st.markdown(f"""
    <div class="time-date-box">
        <span style="font-size: 20px;">📅 {now.strftime("%Y / %m / %d")}</span>
        <span style="margin: 0 20px; opacity: 0.5;">|</span>
        <span style="font-size: 20px;">⏰ {now.strftime("%I:%M %p")}</span>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. رفع الملف وعرض المنيو
with st.sidebar:
    st.markdown("### 📂 تحميل البيانات")
    uploaded_file = st.file_uploader("ارفع ملف الإكسيل المجمع", type=['xlsx'])

if uploaded_file:
    excel = pd.ExcelFile(uploaded_file)
    sheets = excel.sheet_names
    
    cols = st.columns(4)
    for i, name in enumerate(sheets):
        with cols[i % 4]:
            if st.button(name):
                st.session_state['active_menu'] = name

    if 'active_menu' in st.session_state:
        sel = st.session_state['active_menu']
        df = pd.read_excel(uploaded_file, sheet_name=sel)
        df.columns = [str(c) if "Unnamed" not in str(c) else "" for c in df.columns]
        df = df.fillna("-")

        st.markdown(f"<h2 style='text-align:right; color:#e76f51; border-right: 10px solid #1d3557; padding-right:15px;'>📋 منيو: {sel}</h2>", unsafe_allow_html=True)
        
        # عرض الجدول بالتنسيق الجديد فائق الوضوح
        st.markdown(df.to_html(classes='main-table', index=False), unsafe_allow_html=True)
        
        if st.button("🖨️ طباعة"):
            st.components.v1.html("<script>window.print();</script>", height=0)
else:
    st.info("👈 برجاء رفع ملف الإكسيل من القائمة الجانبية للبدء.")