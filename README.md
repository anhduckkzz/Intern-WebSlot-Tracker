# 🎓 CSE HCMUT Internship Monitor

**Giám sát website thực tập CSE HCMUT và thông báo khi có công ty mới!**

![Status](https://img.shields.io/badge/Status-Ready-green)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Cloud-lightgrey)

## ✨ Tính năng

- 🔍 **Monitoring 24/7** - Kiểm tra công ty mới mỗi 2 phút
- 📱 **Telegram Bot** - Thông báo real-time qua Telegram
- ☁️ **Cloud Ready** - Deploy miễn phí lên Railway/Render/GitHub Actions
- 🔗 **No Login Required** - Chỉ cần API công khai
- 📊 **Smart Detection** - Hiển thị slot còn trống/đã đầy

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

1. **Setup Telegram Bot:**
   - Mở Telegram → tìm @BotFather
   - Gửi `/newbot` → đặt tên → copy **BOT TOKEN**
   - Tìm @userinfobot → gửi `/start` → copy **CHAT ID**

2. **Deploy nhanh với Railway:**
   - Fork repo này
   - Vào [railway.app](https://railway.app) → New Project
   - Connect GitHub → chọn repo
   - Thêm Environment Variables:
     ```
     TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI...
     TELEGRAM_CHAT_ID=123456789
     ```
   - Deploy! ✅

3. **Kiểm tra:** Bot sẽ gửi tin nhắn "Monitor Started!" khi deploy thành công

## 📁 Project Structure

```
intern_web/
├── internship_monitor.py     # Script chạy local (Windows notification)
├── monitor_cloud.py          # Script chạy cloud (Telegram bot)
├── requirements.txt          # Dependencies cho local
├── requirements_cloud.txt    # Dependencies cho cloud
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
# Environment Variables
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 🎯 API Endpoints Discovered

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/home/company/all` | Danh sách tất cả công ty |
| `GET` | `/home/company/id/{id}` | Chi tiết công ty (slots) |
| `GET` | `/home/state` | Thông tin user & đăng ký |
| `PUT` | `/student/company/register` | Đăng ký công ty |
| `PUT` | `/student/company/cancel` | Hủy đăng ký |

## 📱 Telegram Bot Example

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

## ⚡ Deploy Options

| Platform | Cost | Setup Time | Reliability |
|----------|------|------------|-------------|
| **Railway** | Free | 5 min | ⭐⭐⭐⭐⭐ |
| **Render** | Free | 5 min | ⭐⭐⭐⭐ |
| **GitHub Actions** | Free | 10 min | ⭐⭐⭐ |
| **Local PC** | Free | 1 min | ⭐⭐ |

## 🐛 Troubleshooting

**Bot không gửi tin nhắn:**
- Kiểm tra `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID`
- Đảm bảo đã `/start` bot trên Telegram
- Check logs trong platform dashboard

**Không detect công ty mới:**
- API có thể thay đổi → check console logs
- Network timeout → platform sẽ tự restart

**Deploy lỗi:**
- Kiểm tra `requirements_cloud.txt`
- Ensure Python 3.7+ trong platform settings

## 📊 Statistics

- ✅ **27 công ty** đang active (tính đến 06/04/2026)
- ⏱️ **Kiểm tra mỗi 2 phút** = 720 lần/ngày
- 📱 **Real-time notification** qua Telegram
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