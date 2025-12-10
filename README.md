# 欧路词典 → 墨墨背单词 同步工具 / Eudic to Maimemo Sync Tool

[English](#english) | [中文](#chinese)

---

<a name="chinese"></a>

## 📖 中文说明

### 功能特性

✅ **自动依赖安装** - 首次运行自动检测并安装 `requests` 和 `python-dotenv`  
✅ **欧路词典同步** - 自动获取欧路词典生词本  
✅ **墨墨背单词同步** - 将单词同步到墨墨背单词词库  
✅ **QQ 消息推送** - 同步结果通过 Qmsg 推送到 QQ  
✅ **本地文件保存** - 自动保存单词列表到本地文件  
✅ **时区自动转换** - UTC 时间自动转换为中国时间（UTC+8）  
✅ **日期分组** - 按添加日期自动分组单词  

### 快速开始

#### 1. 下载脚本

将 `sync_words.py` 下载到本地任意目录。

#### 2. 修改配置

打开 `sync_words.py`，找到以下**7个修改点**并填入你的配置：

```python
# 修改点 1: 欧路词典 API Key
EUDIC_API_KEY = "NIS /xxx=="

# 修改点 2: 欧路词典生词本ID（可选，默认为 0）
url = "https://api.frdic.com/api/open/v1/studylist/words?category_id=0"

# 修改点 3: 墨墨背单词 API Key (APP内获取)
api_key = "你的墨墨API密钥"

# 修改点 4: 墨墨背单词笔记本ID
notepad_id = "np-xxxxx"

# 修改点 5: 墨墨词库信息（可选）
payload = {
    "notepad": {
        "title": "云同步词库",  # 自定义标题
        "brief": "暂无简介",    # 自定义简介
        "tags": ["其他"]       # 自定义标签
    }
}

# 修改点 6: Qmsg 推送 Key
qmsg_key = "你的Qmsg密钥"

# 修改点 7: 本地保存路径（可选）
filename = "/www/wwwroot/olu_to_momo/words_data.txt"
```

#### 3. 运行脚本

```bash
python sync_words.py
```

首次运行时会自动安装依赖：

```
[INFO] 检测到缺失的依赖包: requests, python-dotenv
[INFO] 正在自动安装依赖...
[INFO] 安装 requests...
[SUCCESS] requests 安装成功!
[INFO] 安装 python-dotenv...
[SUCCESS] python-dotenv 安装成功!
[SUCCESS] 所有依赖安装完成!
```

### 获取配置信息

#### 📱 欧路词典 API Key

1. 登录 [欧路词典开放平台](https://my.eudic.net/OpenAPI/Doc_Index)
2. 进入「我的应用」创建应用
3. 复制 API Key（格式：`NIS /xxxxx==`）
4. 生词本 ID 默认为 `0`，如需使用其他生词本，查看 API 文档获取 ID

#### 📚 墨墨背单词 API

1. 访问 [墨墨开放平台](https://open.maimemo.com/)
2. 登录并创建应用，获取 API Key
3. **获取笔记本 ID**：
   ```bash
   # 使用以下 API 查询你的笔记本列表
   curl -X GET "https://open.maimemo.com/open/api/v1/notepads" \
     -H "Authorization: Bearer 你的API_Key"
   ```
4. 从返回结果中找到目标笔记本的 ID（格式：`np-xxxx`）

#### 💬 Qmsg 推送 Key

1. 访问 [Qmsg 酱官网](https://qmsg.zendee.cn/)
2. 注册并登录账号
3. 在「我的」页面绑定 QQ 号
4. 复制你的 Key

**测试推送：**
```bash
# 浏览器访问以下地址测试
https://qmsg.zendee.cn/send/你的Key?msg=测试消息
```

### 推送消息示例

#### ✅ 同步成功

```
📚 欧路词典同步成功

✅ 状态：同步完成
📊 单词数量：125 个
🕐 时间：2025-12-10 15:30:00
```

#### ❌ 同步失败

```
📚 欧路词典同步失败

❌ 状态：同步失败
📊 单词数量：0 个
⚠️ 错误：未获取到欧路词典单词
🕐 时间：2025-12-10 15:30:00
```

### 设置定时任务

#### Linux/Mac (crontab)

```bash
# 编辑定时任务
crontab -e

# 每天早上 8 点自动同步
0 8 * * * cd /path/to/script && /usr/bin/python3 sync_words.py >> /path/to/sync.log 2>&1

# 每 2 小时同步一次
0 */2 * * * cd /path/to/script && /usr/bin/python3 sync_words.py >> /path/to/sync.log 2>&1
```

#### Windows (任务计划程序)

1. 打开「任务计划程序」
2. 创建基本任务
3. 触发器：选择「每天」或其他周期
4. 操作：
   - 程序：`C:\Python\python.exe`
   - 参数：`C:\path\to\sync_words.py`
   - 起始于：`C:\path\to\`

### 输出文件格式

`words_data.txt` 按日期分组保存：

```
#2025-12-08
adventure
challenge
opportunity

#2025-12-09
achievement
benefit
capability

#2025-12-10
dedication
efficiency
```

### 常见问题

**Q: 如何查看同步日志？**  
A: 脚本运行时会在控制台输出详细日志，建议使用 `>> log.txt 2>&1` 重定向到文件。

**Q: 推送消息显示乱码？**  
A: 确保脚本文件使用 UTF-8 编码保存。

**Q: 墨墨同步失败怎么办？**  
A: 检查：
1. API Key 是否正确
2. Notepad ID 是否存在（通过 API 查询确认）
3. 网络连接是否正常

**Q: 可以不使用 Qmsg 推送吗？**  
A: 可以，将 `qmsg_key` 留空或注释掉 `send_qmsg_notification(message)` 这行代码即可。

**Q: 如何修改推送消息格式？**  
A: 在 `main()` 函数中找到 `message` 变量的赋值部分，自定义你想要的格式。

### 依赖说明

- **Python**: >= 3.6
- **requests**: HTTP 请求库
- **python-dotenv**: 环境变量管理（本脚本中未强制使用）

### 更新日志

- **v1.0** (2025-12-10)
  - 首次发布
  - 支持欧路→墨墨同步
  - 支持 Qmsg 推送
  - 自动依赖安装

### 开源协议

MPL-2.0 license

---

<a name="english"></a>

## 📖 English Documentation

### Features

✅ **Auto Dependency Installation** - Automatically installs `requests` and `python-dotenv` on first run  
✅ **Eudic Sync** - Fetch vocabulary from Eudic dictionary  
✅ **Maimemo Sync** - Sync words to Maimemo vocabulary  
✅ **QQ Notification** - Push sync results to QQ via Qmsg  
✅ **Local File Save** - Automatically save word list to local file  
✅ **Timezone Conversion** - Auto convert UTC to China Time (UTC+8)  
✅ **Date Grouping** - Automatically group words by date added  

### Quick Start

#### 1. Download Script

Download `sync_words.py` to any local directory.

#### 2. Configure Settings

Open `sync_words.py` and modify these **7 configuration points**:

```python
# Point 1: Eudic API Key
EUDIC_API_KEY = "NIS /xxxxxxxx=="

# Point 2: Eudic Category ID (optional, default is 0)
url = "https://api.frdic.com/api/open/v1/studylist/words?category_id=0"

# Point 3: Maimemo API Key
api_key = "your_maimemo_api_key"

# Point 4: Maimemo Notepad ID (from APP)
notepad_id = "np-xxxx"

# Point 5: Maimemo Notepad Info (optional)
payload = {
    "notepad": {
        "title": "Cloud Sync Vocab",  # Custom title
        "brief": "No description",    # Custom description
        "tags": ["Others"]            # Custom tags
    }
}

# Point 6: Qmsg Push Key
qmsg_key = "your_qmsg_key"

# Point 7: Local Save Path (optional)
filename = "/www/wwwroot/olu_to_momo/words_data.txt"
```

#### 3. Run Script

```bash
python sync_words.py
```

First run will auto-install dependencies:

```
[INFO] Detected missing packages: requests, python-dotenv
[INFO] Installing dependencies...
[INFO] Installing requests...
[SUCCESS] requests installed successfully!
[INFO] Installing python-dotenv...
[SUCCESS] python-dotenv installed successfully!
[SUCCESS] All dependencies installed!
```

### Get Configuration Info

#### 📱 Eudic API Key

1. Login to [Eudic Open Platform](https://my.eudic.net/OpenAPI/Doc_Index)
2. Go to "My Apps" and create an application
3. Copy API Key (format: `NIS /xxxxx==`)
4. Default category ID is `0`, check API docs for other IDs

#### 📚 Maimemo API

1. Visit [Maimemo Open Platform](https://open.maimemo.com/)
2. Login and create app to get API Key
3. **Get Notepad ID**:
   ```bash
   # Query your notepad list
   curl -X GET "https://open.maimemo.com/open/api/v1/notepads" \
     -H "Authorization: Bearer your_api_key"
   ```
4. Find target notepad ID from response (format: `np-xxxx`)

#### 💬 Qmsg Push Key

1. Visit [Qmsg Official Site](https://qmsg.zendee.cn/)
2. Register and login
3. Bind QQ number in "My Profile"
4. Copy your Key

**Test Push:**
```bash
# Visit this URL in browser
https://qmsg.zendee.cn/send/your_key?msg=Test Message
```

### Push Message Examples

#### ✅ Sync Success

```
📚 Eudic Sync Success

✅ Status: Completed
📊 Word Count: 125 words
🕐 Time: 2025-12-10 15:30:00
```

#### ❌ Sync Failed

```
📚 Eudic Sync Failed

❌ Status: Failed
📊 Word Count: 0 words
⚠️ Error: Failed to fetch Eudic words
🕐 Time: 2025-12-10 15:30:00
```

### Setup Scheduled Tasks

#### Linux/Mac (crontab)

```bash
# Edit crontab
crontab -e

# Auto sync at 8:00 AM daily
0 8 * * * cd /path/to/script && /usr/bin/python3 sync_words.py >> /path/to/sync.log 2>&1

# Sync every 2 hours
0 */2 * * * cd /path/to/script && /usr/bin/python3 sync_words.py >> /path/to/sync.log 2>&1
```

#### Windows (Task Scheduler)

1. Open "Task Scheduler"
2. Create Basic Task
3. Trigger: Choose "Daily" or other period
4. Action:
   - Program: `C:\Python\python.exe`
   - Arguments: `C:\path\to\sync_words.py`
   - Start in: `C:\path\to\`

### Output File Format

`words_data.txt` saves words grouped by date:

```
#2025-12-08
adventure
challenge
opportunity

#2025-12-09
achievement
benefit
capability

#2025-12-10
dedication
efficiency
```

### FAQ

**Q: How to view sync logs?**  
A: The script outputs detailed logs to console. Recommend redirecting to file with `>> log.txt 2>&1`.

**Q: Push messages showing garbled text?**  
A: Ensure script file is saved with UTF-8 encoding.

**Q: Maimemo sync failed?**  
A: Check:
1. Is API Key correct
2. Does Notepad ID exist (verify via API query)
3. Is network connection normal

**Q: Can I disable Qmsg push?**  
A: Yes, leave `qmsg_key` empty or comment out the `send_qmsg_notification(message)` line.

**Q: How to modify push message format?**  
A: Find the `message` variable assignment in `main()` function and customize as needed.

### Dependencies

- **Python**: >= 3.6
- **requests**: HTTP library
- **python-dotenv**: Environment variable management (not mandatory in this script)

### Changelog

- **v1.0** (2025-12-10)
  - Initial release
  - Eudic → Maimemo sync
  - Qmsg push support
  - Auto dependency installation

### License

MPL-2.0 license

---

## 💡 Tips

- Keep your API keys secure and don't share them publicly
- Test the script manually before setting up scheduled tasks
- Check logs regularly to ensure sync is working properly
- Backup your configuration before updating

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📧 Contact

If you have any questions or suggestions, feel free to open an issue.

---

**Star ⭐ this project if it helps you!**
