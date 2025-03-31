# hf_restart_trigger.py
import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")  # 환경변수에 등록 필요
SPACE_ID = "aitree2025/markdown_portal_ai_2025"

def restart_space():
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    response = requests.post(
        f"https://huggingface.co/api/spaces/{SPACE_ID}/restart",
        headers=headers
    )
    print("✅ 재시작 요청 완료:", response.status_code, response.text)

if __name__ == "__main__":
    restart_space()