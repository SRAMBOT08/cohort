
import os
from supabase import create_client
from dotenv import load_dotenv

# Load .env.cloudflare or .env.production
load_dotenv('.env.cloudflare')

url = os.getenv('VITE_SUPABASE_URL') or os.getenv('SUPABASE_URL')
key = os.getenv('VITE_SUPABASE_ANON_KEY') or os.getenv('SUPABASE_ANON_KEY')

print(f"Checking URL: {url}")
print(f"Checking Key: {key[:10]}... (len={len(key) if key else 0})")

if not url or not key:
    print("❌ Missing Supabase URL or Key in environment")
    exit(1)

try:
    client = create_client(url, key)
    # Try a simple health check or fetch
    # Authenticating as anon user to check connection
    user = client.auth.sign_up({
        "email": "test_connection@example.com",
        "password": "password123"
    })
    # We don't actually need to sign up, just see if it connects without network error
    print("✅ Connection to Supabase successful (Client initialized)")
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
    
# Check Service Role Key if available (which is what backend uses)
service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
if service_key:
    print(f"\nChecking Service Role Key: {service_key[:10]}...")
    try:
        admin_client = create_client(url, service_key)
        # Try a simple admin operation - list users (limit 1)
        users = admin_client.auth.admin.list_users(page=1, per_page=1)
        print("✅ Service Role Key works! (Admin access verified)")
    except Exception as e:
        print(f"❌ Service Role Key failed: {str(e)}")
else:
    print("\n⚠️ SUPABASE_SERVICE_ROLE_KEY not found in local env files")
