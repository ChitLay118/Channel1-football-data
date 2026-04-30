import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_data():
    # ymovies.top ကို တိုက်ရိုက်ပစ်မှတ်ထားမယ်
    url = "https://ymovies.top/soccerstreams/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # ၁။ Top Slider ထဲက ပွဲစဉ်တွေ (Logos ပါတာတွေ) ယူမယ်
        featured = soup.find_all('div', class_='swiper-slide')
        for item in featured:
            try:
                link_tag = item.find('a')
                if not link_tag: continue
                
                link = link_tag['href']
                if not link.startswith('http'): link = "https://ymovies.top" + link
                
                league = item.find('div', class_='match-header').contents[0].strip()
                time = item.find('span', class_='match-date').text.strip()
                
                # အသင်းနာမည်နဲ့ Logo များ
                logos = item.find_all('img')
                home_logo = logos[0]['src'] if len(logos) > 0 else ""
                away_logo = logos[1]['src'] if len(logos) > 1 else ""
                
                team_names = item.find('div', class_='team-name').get_text(separator="|").split("|")
                home_team = team_names[0].strip()
                away_team = team_names[1].strip() if len(team_names) > 1 else ""

                matches.append({
                    "league": league,
                    "title": f"{home_team} vs {away_team}",
                    "home_logo": home_logo if home_logo.startswith('http') else "https://ymovies.top" + home_logo,
                    "away_logo": away_logo if away_logo.startswith('http') else "https://ymovies.top" + away_logo,
                    "time": time,
                    "link": link,
                    "is_live": True,
                    "type": "featured"
                })
            except: continue

        # ၂။ အောက်က Match List အကုန်လုံးကို ဆွဲထုတ်မယ်
        rows = soup.find_all('div', class_='macthline')
        for row in rows:
            try:
                league = row.find('span', class_='league').text.strip()
                date = row.find('span', class_='date').text.strip()
                
                link_tag = row.find('a')
                link = link_tag['href']
                if not link.startswith('http'): link = "https://ymovies.top" + link
                
                spans = link_tag.find('div').find_all('span')
                home = spans[0].text.strip()
                m_time = spans[1].text.strip()
                away = spans[2].text.strip()
                
                is_live = "today" in spans[1].get('class', [])

                matches.append({
                    "league": league,
                    "title": f"{home} vs {away}",
                    "home_logo": "", 
                    "away_logo": "",
                    "time": f"{date} {m_time}",
                    "link": link,
                    "is_live": is_live,
                    "type": "list"
                })
            except: continue

        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully scraped {len(matches)} matches from ymovies.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_data()
