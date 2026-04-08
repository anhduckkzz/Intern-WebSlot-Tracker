# 💬 Discord Webhook Setup Guide

This guide will help you set up Discord webhook notifications for the Internship Monitor.

## 🎯 What is a Discord Webhook?

A webhook is a special URL that allows external applications to send messages to your Discord channel. It's simpler than a bot and doesn't require authentication tokens.

## 📋 Step-by-Step Setup

### Step 1: Choose a Discord Server

1. Open Discord
2. Select the server where you want to receive notifications
3. You need "Manage Webhooks" permission in that server

### Step 2: Create a Webhook

1. **Right-click** on the channel where you want notifications
2. Click **"Edit Channel"**
3. Go to **"Integrations"** tab on the left
4. Click **"Webhooks"** (or "View Webhooks")
5. Click **"New Webhook"** button

### Step 3: Configure the Webhook

1. **Name**: Give it a meaningful name (e.g., "Internship Monitor")
2. **Avatar**: (Optional) Upload a custom image
3. **Channel**: Ensure it's the correct channel
4. **Copy Webhook URL**: Click "Copy Webhook URL" button

### Step 4: Save the Webhook URL

The webhook URL will look like this:
```
https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQR
```

⚠️ **IMPORTANT**: Keep this URL secret! Anyone with this URL can send messages to your channel.

### Step 5: Add to Environment Variables

#### For Local Testing (.env file)
```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN
```

#### For Railway/Render/Cloud Deployment
Add environment variable:
- **Name**: `DISCORD_WEBHOOK_URL`
- **Value**: Your webhook URL

## 🧪 Test Your Webhook

### Option 1: Use curl
```bash
curl -H "Content-Type: application/json" \
     -d '{"content":"Test message from Internship Monitor!"}' \
     YOUR_WEBHOOK_URL
```

### Option 2: Run the monitor script
```bash
python monitor_cloud.py
```

You should receive a "Monitor Started!" message in Discord.

## 🎨 Rich Embed Features

The monitor sends **rich embeds** to Discord with:

### Color Coding
- 🟢 **Green (0x00FF00)**: Company has available slots
- 🟠 **Orange (0xFF9900)**: Company is full or needs checking
- 🔵 **Blue (0x3498DB)**: Status unknown

### Information Displayed
- Company full name (title)
- Short name
- Current status (còn chỗ / cần kiểm tra)
- Slot information (registered/max)
- Available slots remaining
- Max students accepted
- Direct link to registration website
- HCMUT logo thumbnail
- Timestamp of detection

## 📱 Notification Example

When a new company is detected, you'll receive an embed like this:

```
╔══════════════════════════════════════╗
║  🔔 CÔNG TY MỚI ĐĂNG KÝ!           ║
╠══════════════════════════════════════╣
║  CÔNG TY TNHH ABC TECHNOLOGY        ║
║                                      ║
║  📝 Tên viết tắt: ABC               ║
║  📊 Trạng thái: ✅ Còn chỗ          ║
║  👥 Slot đăng ký: 5/20              ║
║  ✅ Còn trống: 15 slot              ║
║  🎯 Nhận tối đa: 10 SV              ║
║  🔗 Vào website ngay!               ║
║                                      ║
║  CSE HCMUT Internship Monitor       ║
║  14:30:25 06/04/2026                ║
╚══════════════════════════════════════╝
```

## 🔧 Advanced Configuration

### Custom Webhook Name and Avatar

Edit the webhook in Discord settings:
1. Go to Channel Settings → Integrations → Webhooks
2. Click on your webhook
3. Change name and avatar
4. Save changes

### Multiple Webhooks

You can create multiple webhooks for:
- Different channels (announcements, alerts, logs)
- Different notification types
- Backup notification channel

To use multiple webhooks, you can modify the code or set up separate monitor instances.

## 🛡️ Security Best Practices

1. **Never commit webhook URL to git**
   - Use `.env` file (already in `.gitignore`)
   - Use environment variables in cloud platforms

2. **Rotate webhook if exposed**
   - Delete old webhook in Discord
   - Create new webhook
   - Update environment variable

3. **Limit webhook permissions**
   - Only give access to specific channel
   - Don't share webhook URL publicly

## ❓ Troubleshooting

### Webhook not sending messages

**Check webhook URL format:**
- Must start with `https://discord.com/api/webhooks/`
- Must contain webhook ID and token
- No spaces or extra characters

**Check webhook status in Discord:**
- Go to Channel Settings → Integrations → Webhooks
- Ensure webhook is not deleted
- Check if channel still exists

**Check rate limits:**
- Discord webhooks have rate limits
- The monitor respects these limits automatically
- If sending too many messages, some may be dropped

### Messages not formatted correctly

**Ensure you're using `monitor_cloud.py`:**
- The cloud version has rich embed support
- Local version (`internship_monitor.py`) doesn't use Discord

**Check Discord permissions:**
- Webhook needs permission to send embeds
- Channel must allow webhook messages

### No startup message received

**Check environment variable:**
```bash
# Print to verify (Linux/Mac)
echo $DISCORD_WEBHOOK_URL

# Print to verify (Windows)
echo %DISCORD_WEBHOOK_URL%
```

**Check logs:**
- Look for `[✓] Discord notification sent`
- Or `[ERROR] Discord webhook failed: ...`

**Test webhook independently:**
```python
import requests

webhook_url = "YOUR_WEBHOOK_URL"
payload = {
    "content": "Test message!"
}
response = requests.post(webhook_url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
```

## 🌟 Tips

1. **Use a dedicated channel** for internship notifications to avoid spam
2. **Enable mobile notifications** for that channel to get instant alerts
3. **Pin important messages** about high-priority companies
4. **Use with Telegram** for redundancy - configure both!
5. **Test before deploying** to ensure everything works

## 📚 Additional Resources

- [Discord Webhooks Documentation](https://discord.com/developers/docs/resources/webhook)
- [Discord Embed Limits](https://discord.com/developers/docs/resources/channel#embed-limits)
- [Discord Rate Limits](https://discord.com/developers/docs/topics/rate-limits)

## 🤝 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review console logs for error messages
3. Test webhook with curl or Postman
4. Verify environment variables are set correctly
5. Check Discord server permissions

---

**Happy monitoring! 🎓**
