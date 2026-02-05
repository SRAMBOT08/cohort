import os
import dj_database_url
import socket
from urllib.parse import urlparse

# Load env manually or assume it's set
# For this test, we'll read .env manually if needed, or rely on user environment
# But better to read .env explicitly
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR.parent / '.env'

def read_env():
    print(f"Reading {ENV_FILE}")
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith("DATABASE_URL="):
                return line.strip().split('=', 1)[1]
    return None

db_url = read_env()
print(f"--------------------------------------------------")
print(f"Raw DATABASE_URL: {db_url}")
print(f"--------------------------------------------------")

if db_url:
    # 1. Parse with dj_database_url
    config = dj_database_url.parse(db_url)
    print(f"Parsed Config:")
    print(f"  ENGINE: {config.get('ENGINE')}")
    print(f"  NAME: {config.get('NAME')}")
    print(f"  USER: {config.get('USER')}")
    print(f"  HOST: {config.get('HOST')}")
    print(f"  PORT: {config.get('PORT')}")
    
    # 2. Parse with urllib
    parsed = urlparse(db_url)
    print(f"Urllib Parse:")
    print(f"  Hostname: {parsed.hostname}")
    print(f"  Port: {parsed.port}")
    print(f"  Username: {parsed.username}")
    
    # 3. DNS Lookup
    host = config.get('HOST')
    print(f"--------------------------------------------------")
    print(f"Attempting DNS resolution for: {host}")
    try:
        ip = socket.gethostbyname(host)
        print(f"SUCCESS: Resolved {host} to {ip}")
    except Exception as e:
        print(f"FAILURE: Could not resolve {host}: {e}")
        
else:
    print("DATABASE_URL not found in .env")
