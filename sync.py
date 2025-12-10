# 主程序
# 可自动安装依赖
import sys
import subprocess

def check_and_install_dependencies():
    """检查并自动安装所需依赖"""
    required_packages = {
        'requests': 'requests',
        'dotenv': 'python-dotenv'
    }
    
    missing_packages = []
    
    # 检查每个包是否已安装
    for import_name, package_name in required_packages.items():
        try:
            if import_name == 'dotenv':
                __import__('dotenv')
            else:
                __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    # 如果有缺失的包，自动安装
    if missing_packages:
        print(f"[INFO] 检测到缺失的依赖包: {', '.join(missing_packages)}")
        print("[INFO] 正在自动安装依赖...")
        
        for package in missing_packages:
            try:
                print(f"[INFO] 安装 {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--break-system-packages"])
                print(f"[SUCCESS] {package} 安装成功!")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] 安装 {package} 失败: {e}")
                sys.exit(1)
        
        print("[SUCCESS] 所有依赖安装完成!")
        print()

# 首先检查并安装依赖
check_and_install_dependencies()

# 导入其他必需的模块
import os
import requests
import json
from collections import defaultdict
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from urllib.parse import quote

# 修改点 1
EUDIC_API_KEY = "NIS /xxxxxxx =="

def fetch_word_list():
    """获取欧路词典生词本"""
    load_dotenv()
    
    headers = {
        "Authorization": EUDIC_API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    
    # 修改点 2（可不修改）
    url = "https://api.frdic.com/api/open/v1/studylist/words?category_id=0"
    # 上边的链接的0代表欧陆词典的生词本编号，默认是0

    try:
        response = requests.get(url, headers=headers, params={"language": "en"})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] 获取单词列表失败: {e}")
        return None

def generate_word_output(word_data):
    """生成按日期分组的单词字符串，并将UTC时间转换为中国时间"""
    if not word_data or 'data' not in word_data:
        return ""

    # 中国时区 (UTC+8)
    china_tz = timezone(timedelta(hours=8))
    
    grouped_words = defaultdict(list)
    for item in word_data['data']:
        # 解析UTC时间
        utc_time = datetime.fromisoformat(item["add_time"].replace('Z', '+00:00'))
        # 转换为中国时间
        china_time = utc_time.astimezone(china_tz)
        # 获取中国时区的日期
        date = china_time.strftime("%Y-%m-%d")
        
        grouped_words[date].append(item["word"])

    output_string = ""
    for date in sorted(grouped_words.keys()):
        output_string += f"#{date}\n"
        output_string += "\n".join(grouped_words[date])
        output_string += "\n"

    return output_string

def update_maimemo_notepad(content):
    """同步到墨墨背单词"""
    # 加载环境变量
    load_dotenv()

    # 修改点 3
    # 获取 API 密钥和笔记本 ID
    api_key = "8acxxxxxxxxxxxxxxxxxxxxxxxxxx54"
    # 修改点 4
    notepad_id = "np-xxxx"
    # id 要去墨墨背单词API文档通过请求单词本去找
    
    # 请求 URL
    url = f"https://open.maimemo.com/open/api/v1/notepads/{notepad_id}"
    
    # 请求头
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # 请求数据
    # 修改点 5（可不修改）
    payload = {
        "notepad": {
            "status": "UNPUBLISHED",
            "content": content,
            "title": "云同步词库",
            "brief": "暂无简介",
            "tags": ["其他"]
        }
    }
    
    try:
        # 发送 POST 请求
        response = requests.post(url, json=payload, headers=headers)
        
        # 检查响应
        response.raise_for_status()
        
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] 更新墨墨生词本失败: {e}")
        return None

def send_qmsg_notification(message):
    """发送 Qmsg 推送通知"""
    load_dotenv()

    # Qmsg酱 key
    # 修改点 6
    qmsg_key = "xxxxxxxxxxxxxxxxxxx"
    
    if not qmsg_key:
        print("[WARNING] 未配置 QMSG_KEY，跳过消息推送")
        return None
    
    # 构建 URL
    url = f"https://qmsg.zendee.cn/send/{qmsg_key}"
    
    try:
        # 使用 POST 方式发送
        response = requests.post(
            url,
            data={"msg": message},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            print("[SUCCESS] Qmsg 消息推送成功!")
        else:
            print(f"[WARNING] Qmsg 推送返回: {result}")
        
        return result
    except requests.RequestException as e:
        print(f"[ERROR] Qmsg 消息推送失败: {e}")
        return None
        
# 修改点 7（保存路径）
def save_words_to_file(word_data, filename="/www/wwwroot/olu_to_momo/words_data.txt"):
    """将单词列表保存到文件中"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(generate_word_output(word_data))
        return True
    except Exception as e:
        print(f"[ERROR] 保存单词列表到文件失败: {e}")
        return False

def main():
    start_time = datetime.now()
    print(f"[INFO] 开始同步 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 用于收集同步结果的变量
    sync_status = {
        "success": False,
        "word_count": 0,
        "error_message": None
    }
    
    # 获取欧路单词
    print("[INFO] 正在获取欧路词典单词...")
    word_data = fetch_word_list()
    
    if word_data:
        # 保存单词列表到文件
        word_count = len(word_data.get('data', []))
        sync_status["word_count"] = word_count
        print(f"[INFO] 获取到 {word_count} 个单词，正在保存到本地文件...")
        save_words_to_file(word_data)
        
        # 生成输出并同步到墨墨
        output_string = generate_word_output(word_data)
        print("[INFO] 正在同步到墨墨背单词...")
        response = update_maimemo_notepad(output_string)
        
        if response and response.get('success'):
            print("[SUCCESS] 同步完成!")
            sync_status["success"] = True
        else:
            print("[ERROR] 同步失败!")
            sync_status["error_message"] = "墨墨背单词同步失败"
    else:
        print("[ERROR] 未获取到欧路词典单词，同步终止")
        sync_status["error_message"] = "未获取到欧路词典单词"
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"[INFO] 同步结束 - {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] 总耗时: {duration:.2f} 秒")
    
    # 构建推送消息
    if sync_status["success"]:
        message = f"""📚 欧路词典同步成功

✅ 状态：同步完成
📊 单词数量：{sync_status['word_count']} 个
🕐 时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}"""
    else:
        error_msg = sync_status.get("error_message", "未知错误")
        message = f"""📚 欧路词典同步失败

❌ 状态：同步失败
📊 单词数量：{sync_status['word_count']} 个
⚠️ 错误：{error_msg}
🕐 时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}"""
    
    # 发送 Qmsg 推送
    print("[INFO] 正在发送推送通知...")
    send_qmsg_notification(message)

if __name__ == "__main__":
    main()