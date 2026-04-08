# 📐 System Architecture

## Overview

The Internship Monitor is a multi-channel notification system that monitors the CSE HCMUT internship website and sends real-time alerts.

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTERNSHIP MONITOR SYSTEM                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCE                             │
├─────────────────────────────────────────────────────────────────┤
│  https://internship.cse.hcmut.edu.vn/home/company/all          │
│  • Public API (no authentication required)                      │
│  • Returns JSON list of all companies                           │
│  • Checked every 120 seconds                                    │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MONITOR CORE LOGIC                          │
├─────────────────────────────────────────────────────────────────┤
│  monitor_cloud.py (Cloud) / internship_monitor.py (Local)       │
│                                                                  │
│  1. Fetch companies from API                                    │
│  2. Compare with known_companies.json                           │
│  3. Detect new companies                                        │
│  4. Fetch detailed info (slots, max accept)                     │
│  5. Send notifications                                          │
│  6. Update known_companies.json                                 │
└─────────────────────────────────────────────────────────────────┘
                              ▼
            ┌─────────────────┴──────────────────┐
            ▼                                    ▼
┌────────────────────────┐          ┌────────────────────────┐
│   TELEGRAM BOT API     │          │   DISCORD WEBHOOK      │
├────────────────────────┤          ├────────────────────────┤
│  • HTML formatted msg  │          │  • Rich embed format   │
│  • Push notifications  │          │  • Color coding        │
│  • Cross-platform      │          │  • Thumbnail image     │
│  • Private DM          │          │  • Server-based        │
└────────────────────────┘          └────────────────────────┘
            ▼                                    ▼
┌────────────────────────┐          ┌────────────────────────┐
│  TELEGRAM CLIENT       │          │  DISCORD CLIENT        │
├────────────────────────┤          ├────────────────────────┤
│  📱 Mobile App         │          │  📱 Mobile App         │
│  💻 Desktop App        │          │  💻 Desktop App        │
│  🌐 Web Client         │          │  🌐 Web Client         │
└────────────────────────┘          └────────────────────────┘
            ▼                                    ▼
┌────────────────────────┐          ┌────────────────────────┐
│     👨‍🎓 STUDENT         │          │  👥 STUDENT GROUP      │
└────────────────────────┘          └────────────────────────┘
```

## Component Details

### 1. Data Source
**API Endpoint:** `https://internship.cse.hcmut.edu.vn/home/company/all`

**Response Format:**
```json
{
  "error": null,
  "items": [
    {
      "_id": "company_id_123",
      "fullname": "CÔNG TY TNHH ABC TECHNOLOGY",
      "shortname": "ABC",
      "maxRegister": 20,
      "studentRegister": 5,
      "maxAcceptedStudent": 10
    }
  ]
}
```

### 2. Monitor Core

**Files:**
- `monitor_cloud.py` - For cloud deployment (Telegram + Discord)
- `internship_monitor.py` - For local Windows (Toast notifications)

**Key Functions:**
```python
fetch_companies()          # Get all companies from API
load_known_companies()     # Load previously seen companies
check_for_new_companies()  # Compare and detect new ones
notify_new_company()       # Send notifications
send_telegram_message()    # Telegram notification
send_discord_webhook()     # Discord notification
```

**State Management:**
```
known_companies.json
{
  "company_id_1": {...},
  "company_id_2": {...},
  ...
}
```

### 3. Notification Channels

#### Telegram Bot
- **Setup:** Requires bot creation via @BotFather
- **Auth:** Bot token + Chat ID
- **Format:** HTML-formatted text
- **Rate Limit:** 30 messages/second
- **Best For:** Personal mobile notifications

#### Discord Webhook
- **Setup:** Create webhook in channel settings
- **Auth:** Webhook URL only
- **Format:** Rich embeds with colors
- **Rate Limit:** 5 requests/2 seconds
- **Best For:** Team/server notifications

### 4. Deployment Options

```
┌──────────────────────────────────────────────────────────┐
│                   DEPLOYMENT OPTIONS                      │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  🏠 LOCAL (Windows PC)                                   │
│  └─ internship_monitor.py                               │
│     • Windows Toast notifications                        │
│     • No cloud needed                                    │
│     • Must keep PC running                               │
│                                                           │
│  ☁️  CLOUD (24/7)                                        │
│  ├─ Railway (Recommended)                                │
│  │  • Free tier: Always running                          │
│  │  • Easy deployment from GitHub                        │
│  │  • Environment variables in UI                        │
│  │                                                        │
│  ├─ Render                                               │
│  │  • Free tier: 750 hours/month                         │
│  │  • Auto-sleep after 15 min idle                       │
│  │  • Background worker support                          │
│  │                                                        │
│  └─ GitHub Actions                                       │
│     • Free tier: Unlimited                               │
│     • Runs every 5+ minutes (cron)                       │
│     • State stored in Gist                               │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## Data Flow

### Initial Run
```
1. Load known_companies.json (or empty {})
2. Fetch all companies from API
3. Save to known_companies.json
4. Send "Monitor Started" notification
5. Wait CHECK_INTERVAL seconds
```

### Continuous Monitoring
```
Loop:
  1. Fetch current companies from API
  2. Compare with known_companies
  3. If NEW companies found:
     a. Fetch detailed info
     b. Send Telegram notification (if configured)
     c. Send Discord notification (if configured)
     d. Log to console
  4. Update known_companies.json
  5. Wait CHECK_INTERVAL seconds (120s = 2 min)
```

### When New Company Detected
```
1. Extract company info:
   - Full name
   - Short name
   - ID
   
2. Fetch detailed info:
   - maxRegister (total slots)
   - studentRegister (current registrations)
   - maxAcceptedStudent (max accepted)
   
3. Calculate:
   - Slots remaining = maxRegister - studentRegister
   - Status = "Còn chỗ" if slots > 0 else "Đã đầy"
   
4. Format notifications:
   - Telegram: HTML text with emojis
   - Discord: Rich embed with color
   
5. Send notifications:
   - POST to Telegram API (if configured)
   - POST to Discord webhook (if configured)
   
6. Log results:
   - [✓] Telegram notification sent
   - [✓] Discord notification sent
```

## Environment Configuration

```
┌─────────────────────────────────────────────────────────┐
│              ENVIRONMENT VARIABLES                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  REQUIRED (at least one):                               │
│  • TELEGRAM_BOT_TOKEN      (for Telegram)               │
│  • TELEGRAM_CHAT_ID        (for Telegram)               │
│  • DISCORD_WEBHOOK_URL     (for Discord)                │
│                                                          │
│  OPTIONAL:                                              │
│  • KNOWN_COMPANIES         (for stateless deployment)   │
│  • PORT                    (for web server, default 5000)│
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Notification Flow

### Telegram Flow
```
Monitor → Telegram API → Telegram Server → User's Device
         (HTTP POST)    (Push Service)    (Notification)
```

### Discord Flow
```
Monitor → Discord Webhook → Discord Server → User's Device
         (HTTP POST)        (Push Service)   (Notification)
```

## Error Handling

```
┌─────────────────────────────────────────────────────────┐
│                  ERROR HANDLING                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  API Fetch Failed:                                      │
│  └─ Log error, continue next iteration                  │
│                                                          │
│  Telegram Send Failed:                                  │
│  └─ Log error, try Discord (if configured)              │
│                                                          │
│  Discord Send Failed:                                   │
│  └─ Log error, try Telegram (if configured)             │
│                                                          │
│  Both Failed:                                           │
│  └─ Log to console, continue monitoring                 │
│                                                          │
│  File Save Failed:                                      │
│  └─ Log warning, continue (use env var fallback)        │
│                                                          │
│  General Exception:                                     │
│  └─ Log error, wait, retry next iteration               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Performance Characteristics

| Metric | Value | Note |
|--------|-------|------|
| **Check Interval** | 120 seconds | 2 minutes between checks |
| **API Response Time** | ~1-2 seconds | Depends on network |
| **Notification Latency** | ~1-3 seconds | Telegram + Discord combined |
| **Total Cycle Time** | ~3-5 seconds | Check + notify |
| **Checks per Day** | 720 | 60 min × 24 hr ÷ 2 min |
| **Memory Usage** | ~50-100 MB | Python + requests + Flask |
| **CPU Usage** | <1% | Mostly idle |
| **Network Usage** | ~1-2 MB/day | Small JSON responses |

## Security Considerations

```
┌─────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Environment Variables                               │
│     • Secrets not in code                               │
│     • .env in .gitignore                                │
│     • Platform-managed in cloud                         │
│                                                          │
│  2. API Authentication                                  │
│     • Telegram: Bot token                               │
│     • Discord: Webhook URL (secret)                     │
│     • Source API: Public (no auth)                      │
│                                                          │
│  3. Network Security                                    │
│     • HTTPS only                                        │
│     • Timeout limits (10s)                              │
│     • No credential storage                             │
│                                                          │
│  4. Input Validation                                    │
│     • JSON parsing with error handling                  │
│     • Safe string formatting                            │
│     • No code injection risks                           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Scalability

The system is designed for personal/small group use:
- ✅ Supports 1-100 users easily
- ✅ No database required
- ✅ Stateless (except known_companies.json)
- ✅ Can run multiple instances independently
- ⚠️ Rate limits prevent mass deployment

For large-scale use, consider:
- Database for state management
- Queue system for notifications
- Load balancing for API requests
- Caching layer for API responses

---

**Architecture Status: ✅ Production Ready**

The system is simple, robust, and maintainable with clear separation of concerns and comprehensive error handling.
