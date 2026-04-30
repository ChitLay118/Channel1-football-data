import requests
from bs4 import BeautifulSoup
import json

def scrape_data():
    # URL ကို တိုက်ရိုက် soccer streams page ကို ညွှန်းပါမယ်
    url = "https://ymovies.top/soccerstreams/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # ymovies ရဲ့ တကယ့် structure ကို ရှာဖွေခြင်း
        # ပုံမှန်အားဖြင့် table သို့မဟုတ် a tag တွေထဲမှာ ရှိတတ်ပါတယ်
        # အသုံးများတဲ့ class name တွေကို စမ်းကြည့်ပါမယ်
        links = soup.find_all('a')

        for link in links:
            href = link.get('href', '')
            # link ထဲမှာ stream သို့မဟုတ် soccer အစရှိတာ ပါတဲ့ link တွေကိုပဲ ယူမယ်
            if '/soccerstreams/' in href and href != '/soccerstreams/':
                title = link.get_text().strip()
                
                # အကယ်၍ title က အလွတ်ဖြစ်နေရင် title attribute ကို ရှာမယ်
                if not title:
                    title = link.get('title', 'Live Match')

                full_link = href
                if not href.startswith('http'):
                    full_link = "https://ymovies.top" + href

                matches.append({
                    "title": title,
                    "link": full_link,
                    "status": "LIVE"
                })

        # တကယ်လို့ ဘာမှ ရှာမတွေ့ရင် (Empty ဖြစ်နေရင်) စမ်းသပ်ဖို့ Sample data တစ်ခု ထည့်ပေးထားမယ်
        if not matches:
            print("No matches found on site. Adding test data...")
            # matches.append({"title": "No Live Matches Currently", "link": "#", "status": "OFFLINE"})

        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully scraped {len(matches)} matches.")

    except Exception as e:
        print(f"Error occurred: {e}")
        # Error တက်ရင်လည်း json file မပျက်အောင် အလွတ်သိမ်းထားမယ်
        with open('matches.json', 'w') as f:
            json.dump([], f)

if __name__ == "__main__":
    scrape_data()
