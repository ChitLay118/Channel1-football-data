import requests
from bs4 import BeautifulSoup
import json
import time

def get_matches(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"URL: {url} | Status: {response.status_code}")
        
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # macthline class ကို ရှာမယ်
        rows = soup.find_all('div', class_='macthline')
        
        for row in rows:
            try:
                league = row.find('span', class_='league').text.strip()
                link_tag = row.find('a')
                href = link_tag['href']
                link = href if href.startswith('http') else "https://ymovies.top" + href
                
                # အသင်းနာမည်နဲ့ အချိန်
                spans = link_tag.find('div').find_all('span')
                home = spans[0].text.strip()
                m_time = spans[1].text.strip()
                away = spans[2].text.strip()

                matches.append({
                    "league": league,
                    "title": f"{home} vs {away}",
                    "time": m_time,
                    "link": link,
                    "is_live": "today" in spans[1].get('class', [])
                })
            except:
                continue
        
        return matches
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def main():
    # ပထမ link ကနေ စမ်းမယ်
    results = get_matches("https://ymovies.top/soccerstreams/")
    
    # အကယ်၍ ပထမ link က ဘာမှမရရင် ဒုတိယ link (backup) နဲ့ ထပ်စမ်းမယ်
    if not results:
        print("First source failed, trying backup...")
        results = get_matches("https://xscore808.com/home/")

    # ရလာတဲ့ results ကို json ထဲ သိမ်းမယ်
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print(f"Final Count: {len(results)} matches saved.")

if __name__ == "__main__":
    main()
