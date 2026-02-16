import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="برج العرب - Borg El Arab Catering", layout="wide")

# دالة لقراءة الصورة وتحويلها لخلفية
def get_base64_img(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

logo_path = "Picsart_25-11-20_15-08-39-076.png"

# 2. حقن التنسيقات (CSS)
css_content = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.95)),
                    url("data:image/png;base64,{get_base64_img(logo_path)}");
        background-size: 45%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* تصميم الساعة والتاريخ */
    .datetime-container {{
        text-align: center;
        font-family: 'Cairo', sans-serif;
        color: #1d3557;
        background: rgba(255, 255, 255, 0.8);
        padding: 10px;
        border-radius: 15px;
        border: 1px solid #e76f51;
        display: inline-block;
        margin-top: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}

    /* تنسيق الأزرار */
    div.stButton > button {{
        height: 120px !important;
        width: 100% !important;
        border-radius: 20px !important;
        background: linear-gradient(145deg, #1d3557, #2a4d7d) !important;
        color: white !important;
        font-family: 'Cairo', sans-serif !important;
        font-size: 24px !important;
        font-weight: bold !important;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2) !important;
        border: none !important;
    }}
    
    div.stButton > button:hover {{
        background: #e76f51 !important;
        transform: scale(1.03) !important;
    }}

    .menu-table {{ width: 100%; border-collapse: collapse; background: white; }}
    .menu-table th {{ background: #1d3557; color: white; padding: 12px; border: 1px solid #ddd; }}
    .menu-table td {{ padding: 10px; text-align: center; border: 1px solid #ddd; font-weight: bold; }}

    #MainMenu, footer, header {{visibility: hidden;}}
</style>
"""
st.markdown(css_content, unsafe_allow_html=True)

# 3. الهيدر (اللوجو والعناوين)
st.markdown('<div style="text-align: center; padding: 10px; border-bottom: 5px solid #e76f51;">', unsafe_allow_html=True)
if os.path.exists(logo_path):
    st.image(logo_path, width=180)
st.markdown("<h1 style='color:#1d3557; font-family:Cairo; margin:0;'>منيو هات شركة برج العرب الجديدة</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#e76f51; font-family:Cairo; font-size:20px; font-weight:bold; margin:0;'>إدارة التكاليف  - السيد عبد الرحمن </p>", unsafe_allow_html=True)

# إضافة الساعة والتاريخ
now = datetime.now()
date_str = now.strftime("%Y / %m / %d")
time_str = now.strftime("%I:%M %p")
st.markdown(f"""
    <div class="datetime-container">
        <span style="font-size: 22px; margin-left: 15px;">📅 {date_str}</span>
        <span style="font-size: 22px; color: #e76f51; font-weight: 900;">⏰ {time_str}</span>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. رفع الملف والتشغيل
with st.sidebar:
    st.markdown("### 📂 تحميل البيانات")
    uploaded_file = st.file_uploader("ارفع ملف الإكسيل هنا", type=['xlsx'])

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
        df = df.fillna("")

        st.markdown(f"<h2 style='text-align:right; color:#1d3557; border-right: 10px solid #e76f51; padding-right:15px;'>📋 عرض منيو: {sel}</h2>", unsafe_allow_html=True)
        st.markdown(df.to_html(classes='menu-table', index=False), unsafe_allow_html=True)
        
        if st.button("🖨️ طباعة المنيو"):
            st.components.v1.html("<script>window.print();</script>", height=0)
else:
    st.info("👈 برجاء رفع ملف الإكسيل من القائمة الجانبية.")