import io, zipfile, sqlite3, os
from datetime import datetime
from garminconnect import Garmin
from fitparse import FitFile

# --- [公开版配置区] ---
# 自动获取当前脚本所在目录，避免暴露服务器路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "gym_data.db")

# 佳明账号配置：建议在本地运行时修改此处，或设置系统环境变量
G_USER = os.getenv("GARMIN_USER", "YOUR_EMAIL@example.com")
G_PASS = os.getenv("GARMIN_PASS", "YOUR_PASSWORD")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    # 力量训练表：存储动作、次数、心率
    conn.execute('''CREATE TABLE IF NOT EXISTS strength 
                   (time TEXT, exercise TEXT, reps INTEGER, max_hr INTEGER DEFAULT 0)''')
    # 健康指标表：存储静息心率、睡眠分数
    conn.execute('''CREATE TABLE IF NOT EXISTS health 
                   (date TEXT PRIMARY KEY, rhr INTEGER, sleep_score INTEGER)''')
    conn.commit()
    conn.close()

def parse_and_save(fit_stream, act_date, act_name):
    """解析 FIT 文件并存入数据库"""
    try:
        fit_file = FitFile(fit_stream)
        data_list = []
        
        # 自动精简名称逻辑：例如将 "力量训练-背部" 简化为 "背部"
        clean_name = act_name.replace("力量训练-", "").replace("力量训练", "").strip()
        if not clean_name: 
            clean_name = "未命名训练"

        for record in fit_file.get_messages('set'):
            d = record.get_values()
            reps = d.get('repetitions', 0)
            if reps and reps > 0:
                max_hr = d.get('max_heart_rate', 0)
                data_list.append((act_date, clean_name, int(reps), max_hr))
        
        if data_list:
            conn = sqlite3.connect(DB_FILE)
            conn.executemany("INSERT INTO strength VALUES (?,?,?,?)", data_list)
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"解析 FIT 文件出错: {e}")

def sync_health(api):
    """同步每日健康指标"""
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        sleep_data = api.get_sleep_data(today)
        sleep_score = sleep_data.get('dailySleepDTO', {}).get('sleepScore', 0)
        
        stats = api.get_stats(today)
        rhr = stats.get('restingHeartRate', 0)
        
        conn = sqlite3.connect(DB_FILE)
        conn.execute("INSERT OR REPLACE INTO health VALUES (?,?,
