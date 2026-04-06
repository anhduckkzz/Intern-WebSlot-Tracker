"""
Internship Monitor - Cloud Version
Monitors https://internship.cse.hcmut.edu.vn for new companies
Sends Telegram notification when new company detected

Deploy to: Railway, Render, GitHub Actions, or any cloud platform
"""

import requests
import json
import time
import os
from datetime import datetime

# ============ CONFIGURATION ============
BASE_URL = "https://internship.cse.hcmut.edu.vn"
COMPANIES_API = f"{BASE_URL}/home/company/all"

# Check interval in seconds (2 minutes)
CHECK_INTERVAL = 120

# ============ TELEGRAM SETTINGS ============
# Get from @BotFather on Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
# Get from @userinfobot or @getmyid_bot
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ============ STORAGE ============
# For cloud deployment, use environment variable or file
KNOWN_COMPANIES_FILE = "known_companies.json"


def load_known_companies():
    """Load previously known companies"""
    # Try environment variable first (for stateless deployment)
    env_data = os.environ.get("KNOWN_COMPANIES")
    if env_data:
        try:
            return json.loads(env_data)
        except:
            pass
    
    # Try file
    try:
        with open(KNOWN_COMPANIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_known_companies(companies):
    """Save known companies to file"""
    try:
        with open(KNOWN_COMPANIES_FILE, "w", encoding="utf-8") as f:
            json.dump(companies, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[WARN] Could not save to file: {e}")


def fetch_companies():
    """Fetch all companies from the API"""
    try:
        timestamp = int(time.time() * 1000)
        url = f"{COMPANIES_API}?t={timestamp}&condition="
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data.get("items", [])
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch companies: {e}")
        return None


def fetch_company_details(company_id):
    """Fetch detailed information about a specific company"""
    try:
        timestamp = int(time.time() * 1000)
        url = f"{BASE_URL}/home/company/id/{company_id}?t={timestamp}"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data.get("item", data)
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch company details: {e}")
        return None


def send_telegram_message(message):
    """Send message via Telegram bot"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[WARN] Telegram not configured")
        print(message)
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"[ERROR] Telegram send failed: {e}")
        return False


def notify_new_company(company):
    """Send notification about new company"""
    company_name = company.get("fullname", "Unknown")
    short_name = company.get("shortname", "")
    company_id = company.get("_id", "")
    
    # Get additional details
    details = fetch_company_details(company_id)
    max_register = "N/A"
    current_register = "N/A"
    max_accept = "N/A"
    
    if details:
        max_register = details.get("maxRegister", "N/A")
        current_register = details.get("studentRegister", "N/A")
        max_accept = details.get("maxAcceptedStudent", "N/A")
    
    # Check if has available slots
    has_slots = False
    if isinstance(max_register, int) and isinstance(current_register, int):
        has_slots = current_register < max_register
    
    status_emoji = "✅" if has_slots else "⚠️"
    
    message = f"""
🔔 <b>CÔNG TY MỚI!</b> 🔔

{status_emoji} <b>{company_name}</b>
📝 Viết tắt: {short_name}

📊 <b>Thông tin đăng ký:</b>
• Slot: {current_register}/{max_register}
• Nhận tối đa: {max_accept} SV

🔗 <a href="{BASE_URL}">Vào đăng ký ngay!</a>

⏰ {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}
"""
    
    # Console log
    print(f"\n{'='*50}")
    print(f"🆕 NEW COMPANY: {company_name}")
    print(f"   Slots: {current_register}/{max_register}")
    print(f"{'='*50}\n")
    
    # Send Telegram
    send_telegram_message(message)


def check_for_new_companies():
    """Check for new companies and notify if found"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] Checking for new companies...")
    
    # Load known companies
    known = load_known_companies()
    
    # Fetch current companies
    companies = fetch_companies()
    if companies is None:
        return 0
    
    # Convert to dict with ID as key
    current = {c["_id"]: c for c in companies}
    
    # Find new companies
    new_company_ids = set(current.keys()) - set(known.keys())
    
    if new_company_ids:
        print(f"✨ Found {len(new_company_ids)} new company(ies)!")
        
        for company_id in new_company_ids:
            notify_new_company(current[company_id])
    else:
        print(f"   No new companies. Total: {len(current)}")
    
    # Update known companies
    save_known_companies(current)
    
    return len(new_company_ids)


def send_startup_message():
    """Send startup notification"""
    companies = fetch_companies()
    count = len(companies) if companies else 0
    
    # Count available slots
    available = 0
    if companies:
        for c in companies:
            details = fetch_company_details(c["_id"])
            if details:
                max_reg = details.get("maxRegister", 0)
                current_reg = details.get("studentRegister", 0)
                if isinstance(max_reg, int) and isinstance(current_reg, int):
                    if current_reg < max_reg:
                        available += 1
    
    message = f"""
🟢 <b>Monitor Started!</b>

📊 Tổng công ty: {count}
✅ Còn slot: {available}
⏱️ Check interval: {CHECK_INTERVAL}s

Bot đang chạy và sẽ thông báo khi có công ty mới!
"""
    send_telegram_message(message)


def main():
    """Main loop"""
    print("="*50)
    print("🎓 INTERNSHIP MONITOR - CLOUD VERSION")
    print("="*50)
    print(f"Website: {BASE_URL}")
    print(f"Check interval: {CHECK_INTERVAL}s")
    print(f"Telegram: {'Configured' if TELEGRAM_BOT_TOKEN else 'NOT SET'}")
    print("="*50)
    
    # Send startup message
    send_startup_message()
    
    # Initial check (initialize known companies)
    check_for_new_companies()
    
    # Continuous monitoring
    print("\n🔄 Starting continuous monitoring...\n")
    while True:
        time.sleep(CHECK_INTERVAL)
        try:
            check_for_new_companies()
        except Exception as e:
            print(f"[ERROR] Check failed: {e}")
            # Continue running even if one check fails


if __name__ == "__main__":
    main()
