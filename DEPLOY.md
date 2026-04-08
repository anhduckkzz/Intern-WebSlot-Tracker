# Internship Monitor - Cloud Deployment

Monitor website thực tập CSE HCMUT và thông báo qua Telegram hoặc Discord khi có công ty mới.

## 🚀 Quick Deploy

### Option 1: Railway (Recommended - Free)

1. Fork/Push code lên GitHub
2. Vào [railway.app](https://railway.app)
3. New Project → Deploy from GitHub repo
4. Thêm Environment Variables (chọn ít nhất một):
   - **Telegram**: `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`
   - **Discord**: `DISCORD_WEBHOOK_URL`
5. Deploy!

### Option 2: Render (Free)

1. Push code lên GitHub
2. Vào [render.com](https://render.com)
3. New → Background Worker
4. Connect GitHub repo
5. Thêm Environment Variables
6. Deploy!

### Option 3: GitHub Actions (Free - mỗi 5 phút)

1. Tạo file `.github/workflows/monitor.yml` (xem bên dưới)
2. Thêm Secrets trong repo settings
3. Push!

## 📱 Setup Telegram Bot (Optional)

### Bước 1: Tạo Bot
1. Mở Telegram, tìm @BotFather
2. Gửi `/newbot`
3. Đặt tên bot (vd: `CSE Internship Monitor`)
4. Đặt username (vd: `cse_intern_monitor_bot`)
5. **Copy TOKEN** được cung cấp

### Bước 2: Lấy Chat ID
1. Mở Telegram, tìm @userinfobot hoặc @getmyid_bot
2. Gửi `/start`
3. **Copy số Chat ID** (vd: `123456789`)

### Bước 3: Start Bot
1. Tìm bot bạn vừa tạo trên Telegram
2. Gửi `/start` để activate

## 💬 Setup Discord Webhook (Optional)

### Bước 1: Tạo Webhook
1. Mở Discord → vào server của bạn
2. Click chuột phải vào channel muốn nhận thông báo
3. Settings → Integrations → Webhooks
4. Click "New Webhook"

### Bước 2: Cấu hình Webhook
1. Đặt tên webhook (vd: `Internship Monitor`)
2. Chọn avatar (optional)
3. Click "Copy Webhook URL"
4. **Lưu URL này** để dùng làm biến môi trường

### Bước 3: Test
Webhook URL có dạng:
```
https://discord.com/api/webhooks/123456789/abcdefghijklmnop
```

## 🔧 Environment Variables

### Telegram + Discord (Recommended - nhận thông báo ở cả 2 nơi)
```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
```

### Chỉ Telegram
```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

### Chỉ Discord
```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
```

## 📁 Files

- `monitor_cloud.py` - Script chính cho cloud (hỗ trợ Telegram + Discord)
- `requirements_cloud.txt` - Dependencies
- `Procfile` - Cho Railway/Heroku
- `internship_monitor.py` - Script local (có notification Windows)
- `.env.example` - Template cho environment variables

## 🧪 Test Local

### Windows
```cmd
# Copy .env.example to .env
copy .env.example .env

# Edit .env và điền thông tin
notepad .env

# Run
python monitor_cloud.py
```

### Linux/Mac
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env và điền thông tin
nano .env

# Set environment variables
export TELEGRAM_BOT_TOKEN=your_token
export TELEGRAM_CHAT_ID=your_chat_id
export DISCORD_WEBHOOK_URL=your_webhook_url

# Run
python monitor_cloud.py
```

## 📋 GitHub Actions Workflow

Tạo file `.github/workflows/monitor.yml`:

```yaml
name: Internship Monitor

on:
  schedule:
    - cron: '*/5 * * * *'  # Mỗi 5 phút
  workflow_dispatch:  # Cho phép chạy manual

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install requests
      
      - name: Download known companies
        continue-on-error: true
        run: |
          curl -H "Authorization: token ${{ secrets.GIST_TOKEN }}" \
            https://gist.githubusercontent.com/${{ github.actor }}/${{ secrets.GIST_ID }}/raw/known_companies.json \
            -o known_companies.json
      
      - name: Run monitor
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: python -c "
          import monitor_cloud as m
          m.check_for_new_companies()
          "
      
      - name: Upload known companies
        if: always()
        run: |
          # Save to gist for persistence
          curl -X PATCH \
            -H "Authorization: token ${{ secrets.GIST_TOKEN }}" \
            -d '{"files":{"known_companies.json":{"content":"'"$(cat known_companies.json)"'"}}}' \
            https://api.github.com/gists/${{ secrets.GIST_ID }}
```

**Secrets cần thêm (GitHub repo settings → Secrets and variables → Actions):**
- `TELEGRAM_BOT_TOKEN` (optional - nếu dùng Telegram)
- `TELEGRAM_CHAT_ID` (optional - nếu dùng Telegram)
- `DISCORD_WEBHOOK_URL` (optional - nếu dùng Discord)
- `GIST_TOKEN` (Personal Access Token với gist scope)
- `GIST_ID` (ID của gist để lưu known_companies.json)

## 🎨 Discord Notification Example

Discord sẽ nhận **rich embed** với:
- ✅ Màu xanh: Còn slot trống
- 🟠 Màu cam: Đã đầy hoặc cần kiểm tra
- 🔵 Màu xanh dương: Chưa rõ trạng thái
- Thumbnail logo BKU
- Các field hiển thị đầy đủ thông tin
- Link trực tiếp đến website
- Timestamp

## 🔥 Tips

1. **Dùng cả Telegram + Discord** để không bỏ lỡ thông báo
2. **Railway/Render** tốt hơn GitHub Actions vì check liên tục (mỗi 2 phút)
3. **GitHub Actions** miễn phí nhưng chỉ check mỗi 5 phút (giới hạn của GitHub)
4. Kiểm tra logs để đảm bảo bot hoạt động đúng
5. Test webhook trước khi deploy bằng cách chạy local

## ⚠️ Troubleshooting

### Discord webhook không hoạt động
- Kiểm tra webhook URL có đúng format không
- Webhook có bị xóa trong Discord settings không?
- Check logs để xem error message

### Telegram không nhận tin
- Đảm bảo đã `/start` bot
- Check CHAT_ID có đúng không (phải là số)
- BOT_TOKEN phải lấy từ @BotFather

### Không nhận thông báo cả 2 platform
- Check environment variables đã set chưa
- Xem console logs để biết service nào failed
- Test local trước khi deploy
