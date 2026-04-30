import requests
from bs4 import BeautifulSoup
import json

def scrape_data():
    url = "https://xscore808.com/home/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # HTML ထဲက macthline ဆိုတဲ့ class ရှိတဲ့ div တွေကို ရှာမယ်
        match_rows = soup.find_all('div', class_='macthline')

        for row in match_rows:
            try:
                # League နာမည်ယူမယ်
                league = row.find('span', class_='league').text.strip()
                
                # အသင်းနာမည်တွေနဲ့ ပွဲချိန်ကို ယူမယ်
                # a tag ထဲက div ထဲမှာ span ၃ ခုရှိတယ် (Team A, Time, Team B)
                match_info = row.find('a').find('div')
                spans = match_info.find_all('span')
                
                home_team = spans[0].text.strip()
                match_time = spans[1].text.strip()
                away_team = spans[2].text.strip()
                
                # Link ယူမယ်
                link = row.find('a')['href']
                if not link.startswith('http'):
                    link = "https://xscore808.com" + link

                matches.append({
                    "league": league,
                    "title": f"{home_team} vs {away_team}",
                    "time": match_time,
                    "link": link,
                    "status": "LIVE" if "today" in spans[1].get('class', []) else "UPCOMING"
                })
            except Exception as e:
                continue

        # matches.json ထဲကို သိမ်းမယ်
        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully scraped {len(matches)} matches.")

    except Exception as e:
        print(f"Main Error: {e}")
        with open('matches.json', 'w') as f:
            json.dump([], f)

if __name__ == "__main__":
    scrape_data()
