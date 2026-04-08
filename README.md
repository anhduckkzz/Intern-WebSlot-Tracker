# 🎓 CSE HCMUT Internship Monitor

**Giám sát website thực tập CSE HCMUT và thông báo khi có công ty mới!**

![Status](https://img.shields.io/badge/Status-Ready-green)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Cloud-lightgrey)

## ✨ Tính năng

- 🔍 **Monitoring 24/7** - Kiểm tra công ty mới mỗi 2 phút
- 📱 **Telegram Bot** - Thông báo real-time qua Telegram
- 💬 **Discord Webhook** - Thông báo rich embed qua Discord
- ☁️ **Cloud Ready** - Deploy miễn phí lên Railway/Render/GitHub Actions
- 🔗 **No Login Required** - Chỉ cần API công khai
- 📊 **Smart Detection** - Hiển thị slot còn trống/đã đầy
- 🎨 **Rich Embeds** - Discord notifications với màu sắc và format đẹp

## 🚀 Quick Start

### Chạy Local (Windows)

1. **Cài đặt:**
   ```bash
   git clone <repo>
   cd intern_web
   pip install -r requirements.txt
   ```

2. **Chạy:**
   ```bash
   python internship_monitor.py          # Chạy liên tục với Windows notification
   python internship_monitor.py --list   # Xem danh sách công ty hiện tại
   ```

### Deploy Cloud 24/7 (Miễn phí)

#### Setup Notification Channels (chọn ít nhất 1)

**Option A: Telegram Bot**
1. Mở Telegram → tìm @BotFather
2. Gửi `/newbot` → đặt tên → copy **BOT TOKEN**
3. Tìm @userinfobot → gửi `/start` → copy **CHAT ID**

**Option B: Discord Webhook**
1. Mở Discord → vào server của bạn
2. Click chuột phải vào channel → Settings → Integrations → Webhooks
3. Click "New Webhook" → Copy **WEBHOOK URL**

**Option C: Cả hai (Recommended)** 🌟
- Setup cả Telegram và Discord để không bỏ lỡ thông báo!

#### Deploy với Railway (Recommended)

1. Fork repo này
2. Vào [railway.app](https://railway.app) → New Project
3. Connect GitHub → chọn repo
4. Thêm Environment Variables:
   ```bash
   # Telegram (optional)
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI...
   TELEGRAM_CHAT_ID=123456789
   
   # Discord (optional)
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
   ```
5. Deploy! ✅

6. **Kiểm tra:** Bot sẽ gửi tin nhắn "Monitor Started!" khi deploy thành công

## 📁 Project Structure

```
intern_web/
├── internship_monitor.py     # Script chạy local (Windows notification)
├── monitor_cloud.py          # Script chạy cloud (Telegram + Discord)
├── requirements.txt          # Dependencies cho local
├── requirements_cloud.txt    # Dependencies cho cloud
├── .env.example              # Template cho environment variables
├── Procfile                  # Config cho Railway/Heroku
├── DEPLOY.md                 # Hướng dẫn deploy chi tiết
└── README.md                 # File này
```

## 🔧 Configuration

### Local Version (`internship_monitor.py`)
```python
CHECK_INTERVAL = 120           # Kiểm tra mỗi 2 phút
ENABLE_NOTIFICATION = True     # Thông báo Windows
ENABLE_SOUND = True           # Âm thanh cảnh báo
AUTO_OPEN_BROWSER = True      # Tự mở browser
```

### Cloud Version (`monitor_cloud.py`)
```bash
# Environment Variables - chọn ít nhất 1 notification method

# Telegram
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id

# Discord
DISCORD_WEBHOOK_URL=your_webhook_url
```

## 🎯 API Endpoints Discovered

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/home/company/all` | Danh sách tất cả công ty |
| `GET` | `/home/company/id/{id}` | Chi tiết công ty (slots) |
| `GET` | `/home/state` | Thông tin user & đăng ký |
| `PUT` | `/student/company/register` | Đăng ký công ty |
| `PUT` | `/student/company/cancel` | Hủy đăng ký |

## 📱 Notification Examples

### Telegram Bot
```
🔔 CÔNG TY MỚI! 🔔

✅ CÔNG TY TNHH ABC TECHNOLOGY
📝 Viết tắt: ABC

📊 Thông tin đăng ký:
• Slot: 5/20
• Nhận tối đa: 10 SV

🔗 Vào đăng ký ngay!

⏰ 14:30:25 06/04/2026
```

### Discord Webhook (Rich Embed)
- ✅ **Màu xanh lá**: Còn slot trống
- 🟠 **Màu cam**: Đã đầy hoặc cần kiểm tra
- 🔵 **Màu xanh dương**: Chưa rõ trạng thái
- Logo BKU thumbnail
- Các field hiển thị thông tin chi tiết
- Link trực tiếp đến website
- Timestamp tự động

## ⚡ Deploy Options

| Platform | Cost | Setup Time | Reliability | Notification Support |
|----------|------|------------|-------------|---------------------|
| **Railway** | Free | 5 min | ⭐⭐⭐⭐⭐ | Telegram + Discord |
| **Render** | Free | 5 min | ⭐⭐⭐⭐ | Telegram + Discord |
| **GitHub Actions** | Free | 10 min | ⭐⭐⭐ | Telegram + Discord |
| **Local PC** | Free | 1 min | ⭐⭐ | Windows Toast |

## 🐛 Troubleshooting

**Bot không gửi tin nhắn:**
- Kiểm tra `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID`
- Đảm bảo đã `/start` bot trên Telegram
- Check logs trong platform dashboard

**Discord webhook không hoạt động:**
- Kiểm tra `DISCORD_WEBHOOK_URL` có đúng format không
- Webhook có bị xóa trong Discord settings không?
- Test webhook bằng cách gửi POST request thủ công

**Không detect công ty mới:**
- API có thể thay đổi → check console logs
- Network timeout → platform sẽ tự restart

**Deploy lỗi:**
- Kiểm tra `requirements_cloud.txt`
- Ensure Python 3.7+ trong platform settings

## 📊 Statistics

- ✅ **27 công ty** đang active (tính đến 06/04/2026)
- ⏱️ **Kiểm tra mỗi 2 phút** = 720 lần/ngày
- 📱 **Real-time notification** qua Telegram & Discord
- 🔋 **Chạy 24/7** không cần laptop bật

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Create Pull Request

## 📄 License

MIT License - tự do sử dụng và chỉnh sửa!

---

**🎯 Made for CSE HCMUT students to never miss internship opportunities!**

*"Bồ ơi có công ty mới này!" - Bot, 2026*