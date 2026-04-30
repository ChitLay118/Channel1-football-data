import requests
from bs4 import BeautifulSoup
import json
import time
import os

def get_matches_from_source(url, source_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=25)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # ၁။ Featured Matches (Logo ပါတဲ့ Slider ထဲကဟာတွေ ယူမယ်)
        featured_items = soup.find_all('div', class_='swiper-slide')
        for item in featured_items:
            try:
                link_tag = item.find('a')
                if not link_tag: continue
                
                href = link_tag['href']
                link = href if href.startswith('http') else f"https://{source_name}" + href
                
                league = item.find('div', class_='match-header').contents[0].strip()
                m_date = item.find('span', class_='match-date').text.strip()
                
                # Logos ဆွဲထုတ်ခြင်း
                imgs = item.find_all('img')
                h_logo = imgs[0]['src'] if len(imgs) > 0 else ""
                a_logo = imgs[1]['src'] if len(imgs) > 1 else ""
                
                # Team Names
                teams = item.find('div', class_='team-name').get_text(separator="|").split("|")
                h_team = teams[0].strip()
                a_team = teams[1].strip() if len(teams) > 1 else ""

                matches.append({
                    "league": league,
                    "title": f"{h_team} vs {a_team}",
                    "home_team": h_team,
                    "away_team": a_team,
                    "home_logo": h_logo if h_logo.startswith('http') else f"https://{source_name}" + h_logo,
                    "away_logo": a_logo if a_logo.startswith('http') else f"https://{source_name}" + a_logo,
                    "time": m_date,
                    "link": link,
                    "is_live": True,
                    "type": "featured"
                })
            except: continue

        # ၂။ Normal Match List (အောက်က List အကုန်ယူမယ်)
        rows = soup.find_all('div', class_='macthline')
        for row in rows:
            try:
                league = row.find('span', class_='league').text.strip()
                date_str = row.find('span', class_='date').text.strip()
                
                link_tag = row.find('a')
                href = link_tag['href']
                link = href if href.startswith('http') else f"https://{source_name}" + href
                
                spans = link_tag.find('div').find_all('span')
                h_team = spans[0].text.strip()
                m_time = spans[1].text.strip()
                a_team = spans[2].text.strip()
                
                is_live = "today" in spans[1].get('class', [])

                matches.append({
                    "league": league,
                    "title": f"{h_team} vs {a_team}",
                    "home_team": h_team,
                    "away_team": a_team,
                    "home_logo": "", 
                    "away_logo": "",
                    "time": f"{date_str} {m_time}",
                    "link": link,
                    "is_live": is_live,
                    "type": "list"
                })
            except: continue

        return matches
    except Exception as e:
        print(f"Error on {source_name}: {e}")
        return []

def main():
    print("Starting Scraper...")
    
    # ymovies.top မှ အရင်ယူမယ်
    final_matches = get_matches_from_source("https://ymovies.top/soccerstreams/", "ymovies.top")
    
    # မရရင် xscore808 မှ ထပ်ယူမယ်
    if not final_matches:
        print("Ymovies failed, trying xscore808...")
        final_matches = get_matches_from_source("https://xscore808.com/home/", "xscore808.com")

    # Data တွေကို matches.json ထဲသိမ်းမယ်
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(final_matches, f, indent=4, ensure_ascii=False)
    
    print(f"Scrape Complete! {len(final_matches)} matches found.")

if __name__ == "__main__":
    main()
