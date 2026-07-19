import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("LOVABLE_API_URL")
SECRET = os.getenv("EXTERNAL_BACKEND_SECRET")

headers = {
    "Authorization": f"Bearer {SECRET}",
    "Content-Type": "application/json",
}

# Dummy payload matching the exact Zod schema Lovable built
payload = {
    "startup": {
        "name": "Test Terminal Connection 8",
        "synopsis": "Verifying the backend-to-frontend bridge",
        "industry": "DevTools",
        "signal_source": "github",
        "signal_reason": "Testing secure handshake",
        "growth_velocity": 91.9,
        "ai_score": 98,
        "sparkline": [10, 20, 30, 40, 50, 99],
    },
    "pipeline": {
        "stage": "ingested",
        "aggregated_score": 99,
        "deadline_at": "2026-07-21T18:00:00Z",
    },
}

print("Firing test packet to Lovable Cloud...")
try:
    url = f"{BASE_URL.rstrip('/')}/api/public/pipeline"
    r = requests.post(url, json=payload, headers=headers, timeout=15)
    r.raise_for_status()
    print("✅ Success! Response:", r.json())
except Exception as e:
    print("❌ Failed to connect:", e)
    if 'r' in locals():
        print("Status Code:", r.status_code)
        print("Response Body:", r.text)