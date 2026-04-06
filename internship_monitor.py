"""
Internship Website Monitor Script
Monitors https://internship.cse.hcmut.edu.vn for new companies
Runs every 2 minutes and notifies when new companies are added

Features:
- Monitor for new companies via API (no login required)
- Auto-open browser for quick registration when new company detected
- Auto-registration feature (requires session cookies from browser)

API Endpoints discovered:
- GET /home/company/all - List all companies
- GET /home/company/id/{id} - Get company details
- GET /home/state - Get user info and registration status
- PUT /student/company/register {companyId, studentId} - Register for company
- PUT /student/company/cancel {companyId, studentId} - Cancel registration
- GET /student/company/status - Get student's registration status
"""

import requests
import json
import time
import os
import sys
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

# ============ CONFIGURATION ============
# API URLs
BASE_URL = "https://internship.cse.hcmut.edu.vn"
COMPANIES_API = f"{BASE_URL}/home/company/all"
STATE_API = f"{BASE_URL}/home/state"
REGISTER_API = f"{BASE_URL}/student/company/register"

# Data file to store known companies
DATA_FILE = Path(__file__).parent / "known_companies.json"
COOKIES_FILE = Path(__file__).parent / "session_cookies.json"

# Check interval in seconds (2 minutes)
CHECK_INTERVAL = 120

# ============ NOTIFICATION SETTINGS ============
ENABLE_NOTIFICATION = True
ENABLE_SOUND = True
AUTO_OPEN_BROWSER = True  # Auto open browser when new company detected

# ============ AUTO-REGISTRATION (experimental) ============
# Set to True to enable auto-registration when new company with slots is detected
# IMPORTANT: Requires valid session cookies from a logged-in browser
ENABLE_AUTO_REGISTER = False

# Priority keywords for auto-registration (case-insensitive)
# If company name contains any of these keywords, prioritize for auto-registration
PRIORITY_KEYWORDS = []  # e.g., ["VNG", "Grab", "Shopee"]

# Chrome profile for persistent login (optional - for auto-registration)
CHROME_PROFILE_DIR = Path(__file__).parent / "chrome_profile"


def load_known_companies():
    """Load previously known companies from file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_known_companies(companies):
    """Save known companies to file"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)


def load_session_cookies():
    """Load session cookies from file (for auto-registration)"""
    if COOKIES_FILE.exists():
        try:
            with open(COOKIES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return None


def save_session_cookies(cookies):
    """Save session cookies to file"""
    with open(COOKIES_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)


def create_session_with_cookies():
    """Create a requests session with saved cookies"""
    session = requests.Session()
    cookies = load_session_cookies()
    if cookies:
        for name, value in cookies.items():
            session.cookies.set(name, value)
    return session, cookies is not None


def fetch_user_state(session=None):
    """Fetch current user state including registration status"""
    try:
        timestamp = int(time.time() * 1000)
        url = f"{STATE_API}?t={timestamp}"
        
        if session:
            response = session.get(url, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch user state: {e}")
        return None


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
        # API returns {error: null, item: {...}}
        return data.get("item", data)
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch company details: {e}")
        return None


def play_alert_sound():
    """Play alert sound"""
    if not ENABLE_SOUND:
        return
    
    try:
        # Windows beep
        import winsound
        # Play multiple beeps for attention
        for _ in range(3):
            winsound.Beep(1000, 300)  # 1000Hz for 300ms
            time.sleep(0.1)
    except:
        print("\a")  # Fallback to terminal bell


def send_windows_notification(title, message):
    """Send Windows toast notification"""
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name="Internship Monitor",
            timeout=10
        )
    except ImportError:
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=10, threaded=True)
        except ImportError:
            print("[INFO] Install 'plyer' for desktop notifications: pip install plyer")


def open_browser_for_registration():
    """Open browser to the internship website"""
    if AUTO_OPEN_BROWSER:
        webbrowser.open(BASE_URL)


def register_for_company(session, company_id, student_id):
    """
    Register for a company using the API
    
    Args:
        session: requests.Session with valid cookies
        company_id: Company ID to register for
        student_id: Student ID (your user ID)
    
    Returns:
        (success: bool, message: str)
    """
    try:
        timestamp = int(time.time() * 1000)
        url = f"{REGISTER_API}?t={timestamp}"
        
        payload = {
            "companyId": company_id,
            "studentId": student_id
        }
        
        response = session.put(url, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("error"):
            return False, data.get("error")
        
        if data.get("item"):
            return True, "Đăng ký thành công!"
        
        return False, "Phản hồi không xác định"
    
    except requests.RequestException as e:
        return False, f"Lỗi kết nối: {e}"


def try_auto_register(company, session, student_id):
    """
    Try to automatically register for a company if enabled and has slots
    
    Returns:
        (registered: bool, message: str)
    """
    if not ENABLE_AUTO_REGISTER:
        return False, "Auto-registration disabled"
    
    company_id = company.get("_id")
    company_name = company.get("fullname", "Unknown")
    
    # Get details to check if slots available
    details = fetch_company_details(company_id)
    if not details:
        return False, "Không thể lấy thông tin công ty"
    
    max_register = details.get("maxRegister", 0)
    current_register = details.get("studentRegister", 0)
    
    # Check if slots available
    if current_register >= max_register:
        return False, f"Công ty đã đầy ({current_register}/{max_register})"
    
    # Check priority keywords
    is_priority = False
    if PRIORITY_KEYWORDS:
        company_name_lower = company_name.lower()
        is_priority = any(kw.lower() in company_name_lower for kw in PRIORITY_KEYWORDS)
    
    print(f"\n🤖 AUTO-REGISTER: Attempting to register for {company_name}...")
    if is_priority:
        print(f"   ⭐ This is a PRIORITY company!")
    
    # Try to register
    success, message = register_for_company(session, company_id, student_id)
    
    if success:
        print(f"   ✅ {message}")
        return True, message
    else:
        print(f"   ❌ {message}")
        return False, message


def notify_new_company(company, session=None, student_id=None):
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
    
    print("\n" + "="*70)
    print("🔔🔔🔔 CÔNG TY MỚI ĐĂNG KÝ! 🔔🔔🔔")
    print("="*70)
    print(f"📌 Tên đầy đủ: {company_name}")
    print(f"📌 Tên viết tắt: {short_name}")
    print(f"📌 ID: {company_id}")
    print(f"📊 Số lượng đăng ký tối đa: {max_register}")
    print(f"📊 Đã đăng ký: {current_register}")
    print(f"📊 Số sinh viên được nhận tối đa: {max_accept}")
    print(f"🔗 Link: {BASE_URL}")
    print("="*70)
    print("⚡ HÃY NHANH CHÓNG VÀO ĐĂNG KÝ! ⚡")
    print("="*70 + "\n")
    
    # Play alert sound
    play_alert_sound()
    
    # Windows notification
    if ENABLE_NOTIFICATION:
        try:
            send_windows_notification(
                title="🆕 CÔNG TY MỚI - Internship CSE!",
                message=f"{company_name}\nSlot: {current_register}/{max_register}"
            )
        except Exception as e:
            print(f"[WARN] Could not send desktop notification: {e}")


def check_for_new_companies():
    """Check for new companies and notify if found"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Đang kiểm tra công ty mới...")
    
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
    
    # Setup session for auto-registration if enabled
    session = None
    student_id = None
    if ENABLE_AUTO_REGISTER:
        session, has_cookies = create_session_with_cookies()
        if has_cookies:
            state = fetch_user_state(session)
            if state and state.get("user"):
                student_id = state["user"].get("_id")
                print(f"   [AUTH] Logged in as: {state['user'].get('email')}")
            else:
                print("   [WARN] Session cookies invalid - auto-registration disabled")
                session = None
        else:
            print("   [WARN] No session cookies - auto-registration disabled")
            session = None
    
    if new_company_ids:
        print(f"\n✨ Phát hiện {len(new_company_ids)} công ty mới!")
        
        # Open browser first for quick action
        open_browser_for_registration()
        
        for company_id in new_company_ids:
            company = current[company_id]
            notify_new_company(company, session, student_id)
            
            # Try auto-registration if enabled and session valid
            if session and student_id:
                try_auto_register(company, session, student_id)
    else:
        print(f"   Không có công ty mới. Tổng số: {len(current)} công ty.")
    
    # Update known companies
    save_known_companies(current)
    
    return len(new_company_ids)


def show_current_companies():
    """Display current companies with registration status"""
    print("\n📋 DANH SÁCH CÔNG TY HIỆN TẠI:")
    print("-" * 80)
    
    companies = fetch_companies()
    if not companies:
        print("Không thể lấy danh sách công ty.")
        return
    
    for i, company in enumerate(companies, 1):
        details = fetch_company_details(company["_id"])
        if details:
            max_reg = details.get("maxRegister", 0)
            current_reg = details.get("studentRegister", 0)
            status = "✅ CÒN CHỖ" if current_reg < max_reg else "❌ ĐÃ ĐẦY"
            print(f"{i:2}. [{status}] {company['shortname']}")
            print(f"    └─ Đăng ký: {current_reg}/{max_reg} | {company['fullname'][:50]}...")
        else:
            print(f"{i:2}. {company['shortname']} - {company['fullname'][:50]}...")
    
    print("-" * 80)


def main():
    """Main loop"""
    print("="*70)
    print("🎓 INTERNSHIP MONITOR - CSE HCMUT 🎓")
    print("="*70)
    print(f"🌐 Website: {BASE_URL}")
    print(f"⏱️  Kiểm tra mỗi: {CHECK_INTERVAL} giây ({CHECK_INTERVAL//60} phút)")
    print(f"📁 File lưu trữ: {DATA_FILE}")
    print(f"🔔 Thông báo: {'BẬT' if ENABLE_NOTIFICATION else 'TẮT'}")
    print(f"🔊 Âm thanh: {'BẬT' if ENABLE_SOUND else 'TẮT'}")
    print(f"🌐 Tự mở browser: {'BẬT' if AUTO_OPEN_BROWSER else 'TẮT'}")
    print(f"🤖 Auto-register: {'BẬT' if ENABLE_AUTO_REGISTER else 'TẮT'}")
    print("="*70)
    print("\n📌 Nhấn Ctrl+C để dừng\n")
    
    # Show current companies on start
    show_current_companies()
    
    # Initial check
    print("\n🔄 Bắt đầu theo dõi...\n")
    check_for_new_companies()
    
    # Continuous monitoring
    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            check_for_new_companies()
    except KeyboardInterrupt:
        print("\n\n[INFO] Đã dừng theo dõi.")


def show_status():
    """Show current user status and registration info"""
    print("\n📊 TRẠNG THÁI ĐĂNG NHẬP:")
    print("-" * 50)
    
    session, has_cookies = create_session_with_cookies()
    
    if not has_cookies:
        print("❌ Chưa có session cookies.")
        print("   Sử dụng --export-cookies để xuất cookies từ browser.")
        return
    
    state = fetch_user_state(session)
    if not state or not state.get("user"):
        print("❌ Session cookies không hợp lệ hoặc đã hết hạn.")
        return
    
    user = state["user"]
    print(f"✅ Đã đăng nhập!")
    print(f"   Tên: {user.get('lastname', '')} {user.get('firstname', '')}")
    print(f"   Email: {user.get('email', '')}")
    print(f"   MSSV: {user.get('organizationId', 'N/A')}")
    print(f"   ID: {user.get('_id', '')}")
    
    # Registration status
    comp_state = state.get("companyState", {})
    registered = comp_state.get("registered", [])
    accepted = comp_state.get("accepted", [])
    max_register = state.get("internshipMaxRegister", 3)
    
    print(f"\n📝 ĐĂNG KÝ:")
    print(f"   Số lượng đã đăng ký: {len(registered)}/{max_register}")
    print(f"   Số lượng đã được nhận: {len(accepted)}")
    
    if registered:
        print(f"   Công ty đã đăng ký: {', '.join(registered)}")
    if accepted:
        print(f"   Công ty đã nhận: {', '.join(accepted)}")
    
    print("-" * 50)


def export_cookies_guide():
    """Show guide to export cookies from browser"""
    print("""
📚 HƯỚNG DẪN XUẤT SESSION COOKIES:

Để sử dụng chức năng auto-registration, bạn cần xuất cookies từ browser đã đăng nhập.

CÁCH 1: Sử dụng Developer Tools (Chrome/Edge)
1. Đăng nhập vào website: https://internship.cse.hcmut.edu.vn
2. Mở Developer Tools (F12)
3. Vào tab Application → Cookies → https://internship.cse.hcmut.edu.vn
4. Tìm và copy giá trị của cookie "connect.sid"
5. Tạo file session_cookies.json với nội dung:
   {"connect.sid": "<giá trị cookie>"}

CÁCH 2: Sử dụng extension EditThisCookie
1. Cài extension EditThisCookie cho Chrome
2. Đăng nhập vào website
3. Click icon EditThisCookie → Export → Copy
4. Lưu vào file và chuyển đổi sang format:
   {"cookie_name": "cookie_value", ...}

File cookies cần lưu tại: {COOKIES_FILE}

⚠️  LƯU Ý: Cookies có thể hết hạn, cần xuất lại khi gặp lỗi authentication.
""".format(COOKIES_FILE=COOKIES_FILE))


if __name__ == "__main__":
    # Command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--list":
            show_current_companies()
        elif arg == "--check":
            check_for_new_companies()
        elif arg == "--status":
            show_status()
        elif arg == "--export-cookies":
            export_cookies_guide()
        elif arg == "--help" or arg == "-h":
            print("""
🎓 INTERNSHIP MONITOR - CSE HCMUT
Giám sát công ty thực tập và thông báo khi có công ty mới

USAGE:
  python internship_monitor.py              Chạy giám sát liên tục (mỗi 2 phút)
  python internship_monitor.py --list       Hiển thị danh sách công ty hiện tại
  python internship_monitor.py --check      Kiểm tra một lần và thoát
  python internship_monitor.py --status     Kiểm tra trạng thái đăng nhập
  python internship_monitor.py --export-cookies  Hướng dẫn xuất cookies

CONFIGURATION (edit script):
  CHECK_INTERVAL          Thời gian giữa mỗi lần kiểm tra (giây)
  ENABLE_NOTIFICATION     Bật/tắt thông báo Windows
  ENABLE_SOUND            Bật/tắt âm thanh cảnh báo
  AUTO_OPEN_BROWSER       Tự động mở browser khi có công ty mới
  ENABLE_AUTO_REGISTER    Tự động đăng ký (cần cookies)
  PRIORITY_KEYWORDS       Danh sách keywords công ty ưu tiên

API ENDPOINTS:
  GET  /home/company/all                  Danh sách công ty
  GET  /home/company/id/{id}              Chi tiết công ty
  GET  /home/state                        Thông tin user & đăng ký
  PUT  /student/company/register          Đăng ký công ty
  PUT  /student/company/cancel            Hủy đăng ký
""")
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information")
    else:
        main()
