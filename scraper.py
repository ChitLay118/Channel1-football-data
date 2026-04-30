import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_data():
    url = "https://ymovies.top/soccerstreams/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # ymovies ရဲ့ class structure ပေါ်မူတည်ပြီး ပြင်ဆင်ထားပါတယ်
        # များသောအားဖြင့် a tag ထဲမှာ match details ရှိတတ်ပါတယ်
        items = soup.select('a.match-link, .match-box, .match-item') 

        for item in items:
            title = item.get_text(separator=" ").strip()
            link = item.get('href')
            if not link.startswith('http'):
                link = "https://ymovies.top" + link
            
            # ပွဲချိန် နဲ့ အသင်းနာမည်တွေကို ခွဲထုတ်ဖို့ ကြိုးစားခြင်း
            matches.append({
                "title": title,
                "link": link,
                "status": "LIVE" if "Live" in title else "UPCOMING"
            })

        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=4, ensure_ascii=False)
        print("Successfully scraped matches.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_data()
