import requests
from config import ADMIN_TOKEN, ADMIN_CHAT_ID

def admin_ga_yuborish(text):
    url = f"https://api.telegram.org/bot{ADMIN_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": ADMIN_CHAT_ID, "text": text})