#!/usr/bin/env python3
"""
Test Script for Discord Webhook Integration
Run this script to test your Discord webhook before deploying
"""

import requests
import os
import sys
from datetime import datetime

def test_discord_webhook(webhook_url):
    """Test Discord webhook with a sample notification"""
    
    if not webhook_url:
        print("❌ Error: No webhook URL provided")
        print("\nUsage:")
        print("  python test_discord.py <webhook_url>")
        print("  Or set DISCORD_WEBHOOK_URL environment variable")
        return False
    
    print("🧪 Testing Discord Webhook...")
    print(f"URL: {webhook_url[:50]}...")
    
    # Test 1: Simple message
    print("\n1️⃣ Testing simple message...")
    try:
        payload = {
            "content": "✅ Test message from Internship Monitor!"
        }
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print("   ✓ Simple message sent successfully!")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 2: Rich embed (like real notification)
    print("\n2️⃣ Testing rich embed notification...")
    try:
        embed = {
            "embeds": [{
                "title": "🔔 CÔNG TY MỚI ĐĂNG KÝ! (TEST)",
                "description": "**CÔNG TY TNHH TEST TECHNOLOGY**",
                "color": 0x00FF00,  # Green
                "fields": [
                    {
                        "name": "📝 Tên viết tắt",
                        "value": "TEST",
                        "inline": True
                    },
                    {
                        "name": "📊 Trạng thái",
                        "value": "✅ Còn chỗ",
                        "inline": True
                    },
                    {
                        "name": "👥 Slot đăng ký",
                        "value": "5/20",
                        "inline": True
                    },
                    {
                        "name": "✅ Còn trống",
                        "value": "15 slot",
                        "inline": True
                    },
                    {
                        "name": "🎯 Nhận tối đa",
                        "value": "10 SV",
                        "inline": True
                    },
                    {
                        "name": "🔗 Link đăng ký",
                        "value": "[Vào website ngay!](https://internship.cse.hcmut.edu.vn)",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "CSE HCMUT Internship Monitor - TEST"
                },
                "timestamp": datetime.utcnow().isoformat(),
                "thumbnail": {
                    "url": "https://www.hcmut.edu.vn/img/nhanDienThuongHieu/01_logobachkhoasang.png"
                }
            }]
        }
        response = requests.post(webhook_url, json=embed, timeout=10)
        response.raise_for_status()
        print("   ✓ Rich embed sent successfully!")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 3: Startup message
    print("\n3️⃣ Testing startup message...")
    try:
        startup_embed = {
            "embeds": [{
                "title": "🟢 Monitor Started! (TEST)",
                "description": "Bot đang hoạt động và sẽ thông báo khi có công ty mới",
                "color": 0x00FF00,  # Green
                "fields": [
                    {
                        "name": "📊 Tổng công ty",
                        "value": "27",
                        "inline": True
                    },
                    {
                        "name": "✅ Còn slot",
                        "value": "12",
                        "inline": True
                    },
                    {
                        "name": "⏱️ Check interval",
                        "value": "120s (2 phút)",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "CSE HCMUT Internship Monitor - TEST"
                },
                "timestamp": datetime.utcnow().isoformat()
            }]
        }
        response = requests.post(webhook_url, json=startup_embed, timeout=10)
        response.raise_for_status()
        print("   ✓ Startup message sent successfully!")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    print("\n" + "="*50)
    print("✅ ALL TESTS PASSED!")
    print("="*50)
    print("\n📱 Check your Discord channel for 3 test messages:")
    print("   1. Simple text message")
    print("   2. Rich embed with company info")
    print("   3. Startup notification")
    print("\n🚀 Your webhook is ready to use!")
    print("\n💡 Next steps:")
    print("   1. Set DISCORD_WEBHOOK_URL in your .env file")
    print("   2. Or add it to your cloud platform environment variables")
    print("   3. Deploy and enjoy real-time notifications!")
    
    return True


def main():
    """Main function"""
    print("="*50)
    print("🧪 DISCORD WEBHOOK TEST SCRIPT")
    print("="*50)
    
    # Get webhook URL from command line or environment
    webhook_url = None
    
    if len(sys.argv) > 1:
        webhook_url = sys.argv[1]
    else:
        webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "")
    
    if not webhook_url:
        print("\n❌ No webhook URL provided!")
        print("\nUsage:")
        print("  python test_discord.py <webhook_url>")
        print("\nOr set environment variable:")
        print("  export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'")
        print("  python test_discord.py")
        print("\n📚 See DISCORD_SETUP.md for detailed setup instructions")
        sys.exit(1)
    
    success = test_discord_webhook(webhook_url)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
