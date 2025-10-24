# utils/quote_generator.py
import requests

def get_daily_quote():
    try:
        response = requests.get("https://zenquotes.io/api/today")
        if response.status_code == 200:
            data = response.json()
            quote = data[0]["q"]
            author = data[0]["a"]
            return f"“{quote}” — {author}"
        else:
            return "Stay positive and keep moving forward!"
    except Exception as e:
        return "Stay positive and keep moving forward!"
