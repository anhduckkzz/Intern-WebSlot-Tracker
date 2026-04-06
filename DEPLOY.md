# Internship Monitor - Cloud Deployment

Monitor website thực tập CSE HCMUT và thông báo qua Telegram khi có công ty mới.

## 🚀 Quick Deploy

### Option 1: Railway (Recommended - Free)

1. Fork/Push code lên GitHub
2. Vào [railway.app](https://railway.app)
3. New Project → Deploy from GitHub repo
4. Thêm Environment Variables:
   - `TELEGRAM_BOT_TOKEN`: Token từ @BotFather
   - `TELEGRAM_CHAT_ID`: Chat ID của bạn
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

## 📱 Setup Telegram Bot

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

## 🔧 Environment Variables

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

## 📁 Files

- `monitor_cloud.py` - Script chính cho cloud
- `requirements_cloud.txt` - Dependencies
- `Procfile` - Cho Railway/Heroku
- `internship_monitor.py` - Script local (có notification Windows)

## 🧪 Test Local

```bash
# Set environment variables
set TELEGRAM_BOT_TOKEN=your_token
set TELEGRAM_CHAT_ID=your_chat_id

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

**Secrets cần thêm:**
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `GIST_TOKEN` (Personal Access Token với gist scope)
- `GIST_ID` (ID của gist để lưu known_companies.json)
