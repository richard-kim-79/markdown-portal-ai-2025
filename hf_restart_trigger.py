# hf_restart_trigger.py

import os
import requests

SPACE_ID = "aitree2025/markdown_portal_ai_2025"
HF_TOKEN = os.environ.get("HF_TOKEN")

def trigger_restart():
    print("🔁 Hugging Face Space 재시작 요청 중...")
    response = requests.post(
        f"https://api.huggingface.co/spaces/{SPACE_ID}/restart",
        headers={"Authorization": f"Bearer {HF_TOKEN}"}
    )

    if response.status_code == 200:
        print("✅ Space 재시작 성공!")
    else:
        print(f"❌ 재시작 실패: {response.status_code} {response.text}")

if __name__ == "__main__":
    trigger_restart()