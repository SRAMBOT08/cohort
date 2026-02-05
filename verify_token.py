
import os
import sys
from supabase import create_client
from dotenv import load_dotenv

# Load env
load_dotenv('.env.cloudflare')
load_dotenv('.env.production')

url = os.getenv('VITE_SUPABASE_URL') or os.getenv('SUPABASE_URL')
# We need Service Role Key to simulate backend behavior
service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

print(f"Checking Supabase URL: {url}")
if not service_key:
    # Try to prompt or use explicit env var
    service_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

if not service_key:
    print("❌ SUPABASE_SERVICE_ROLE_KEY not found in environment!")
    print("Please run: export SUPABASE_SERVICE_ROLE_KEY=... before running this script")
    sys.exit(1)

print(f"Using Service Role Key: {service_key[:10]}...")

token = input("Paste your Access Token here: ").strip()
if not token:
    print("❌ No token provided")
    sys.exit(1)
    
if token.startswith('"') and token.endswith('"'):
    token = token[1:-1]

print(f"\nVerifying token with Supabase API...")

try:
    client = create_client(url, service_key)
    user_response = client.auth.get_user(token)
    
    if user_response and user_response.user:
        print("\n✅ Token is VALID!")
        print(f"User ID: {user_response.user.id}")
        print(f"Email: {user_response.user.email}")
        print("Backend should accept this token if keys match.")
    else:
        print("\n❌ Token verification returned no user.")

except Exception as e:
    print(f"\n❌ Token verification FAILED: {e}")
    if "Invalid API key" in str(e):
        print("⚠️  YOUR SERVICE ROLE KEY IS INVALID. Update it on Render!")
    elif "expired" in str(e).lower():
        print("⚠️  Token is EXPIRED. Log out and log in again.")
