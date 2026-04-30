import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_data():
    url = "https://xscore808.com/home/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # ၁။ Top Matches (Slider) ထဲက data တွေယူမယ်
        slider_items = soup.find_all('div', class_='swiper-slide')
        for item in slider_items:
            try:
                league = item.find('div', class_='match-header').contents[0].strip()
                match_date = item.find('span', class_='match-date').text.strip()
                
                teams_info = item.find('div', class_='teams-info')
                team_names = teams_info.find('div', class_='team-name').get_text(separator="|").split("|")
                home_team = team_names[0].strip()
                away_team = team_names[1].strip() if len(team_names) > 1 else ""

                logos = item.find_all('div', class_='team-logo')
                home_logo = logos[0].find('img')['src'] if len(logos) > 0 else ""
                away_logo = logos[1].find('img')['src'] if len(logos) > 1 else ""

                link = item.find('a')['href']
                if not link.startswith('http'): link = "https://xscore808.com" + link

                matches.append({
                    "league": league,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_logo": "https://xscore808.com" + home_logo if home_logo.startswith('/') else home_logo,
                    "away_logo": "https://xscore808.com" + away_logo if away_logo.startswith('/') else away_logo,
                    "time": match_date,
                    "link": link,
                    "is_featured": True
                })
            except: continue

        # ၂။ Normal Match List ထဲက data တွေယူမယ်
        match_rows = soup.find_all('div', class_='macthline')
        for row in match_rows:
            try:
                league = row.find('span', class_='league').text.strip()
                date_span = row.find('span', class_='date').text.strip()
                
                link_div = row.find('a').find('div')
                spans = link_div.find_all('span')
                home_team = spans[0].text.strip()
                match_time = spans[1].text.strip()
                away_team = spans[2].text.strip()
                
                status_class = spans[1].get('class', [])
                status = "LIVE" if "today" in status_class else "UPCOMING"

                link = row.find('a')['href']
                if not link.startswith('http'): link = "https://xscore808.com" + link

                matches.append({
                    "league": league,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_logo": "", # List ထဲမှာ logo မပါလို့ အလွတ်ထားမယ်
                    "away_logo": "",
                    "time": f"{date_span} {match_time}",
                    "link": link,
                    "status": status,
                    "is_featured": False
                })
            except: continue

        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=4, ensure_ascii=False)
        print(f"Scraped {len(matches)} matches total.")

    except Exception as e:
        print(f"Scraper Error: {e}")

if __name__ == "__main__":
    scrape_data()
