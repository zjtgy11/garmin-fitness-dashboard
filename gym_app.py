import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import subprocess

# --- 1. 彻底解决半截抬头的纯净 UI ---
st.set_page_config(page_title="Fitness Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/sf-pro-display-2');
    header[data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; margin-top: -20px !important; }
    html, body, [data-testid="stSidebar"] * { font-family: 'SF Pro Display', sans-serif !important; font-size: 14px !important; }
    
    /* 深浅色模式自适应卡片 */
    :root { --card-bg: rgba(255, 255, 255, 0.9); --text-color: #1d1d1f; }
    @media (prefers-color-scheme: dark) { :root { --card-bg: rgba(30, 30, 30, 0.8); --text-color: #f5f5f7; } }
    
    div[data-testid="stMetric"] {
        background-color: var(--card-bg) !important;
        border: 1px solid rgba(128,128,128,0.2) !important;
        border-radius: 12px; padding: 12px !important;
    }
    div[data-testid="stMetricValue"] { font-size: 20px !important; color: var(--text-color) !important; }
    #MainMenu, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 自动化路径配置 (隐去绝对路径) ---
# 获取当前脚本所在目录，确保项目在任何目录下都能运行
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "gym_data.db")

# 同步脚本配置：建议在公开 README 中说明虚拟环境结构
# 这里使用通用调用方式，用户可根据实际环境修改
SYNC_COMMAND = f"python3 {os.path.join(BASE_DIR, 'sync_data.py')}"

def load_all_data():
    if not os.path.exists(DB_PATH): 
        return pd.DataFrame(), pd.DataFrame()
    
    conn = sqlite3.connect(DB_PATH)
    try:
        df_g = pd.read_sql_query("SELECT * FROM strength", conn)
        df_h = pd.read_sql_query("SELECT * FROM health", conn)
    except Exception:
        return pd.DataFrame(), pd.DataFrame()
    finally:
        conn.close()
    
    if not df_g.empty:
        df_g['dt'] = pd.to_datetime(df_g['time'])
        df_g['日期'] = df_g['dt'].dt.strftime('%Y-%m-%d')
        df_
