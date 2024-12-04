import requests 
from bs4 import BeautifulSoup
import json 
import time
from datetime import datetime

URL = "https://www.iso.org/insights"
BASE_URL= "https://www.iso.org"

def get_all_insights_tag_and_link(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        tags = soup.find_all("a", class_="nav-link ps-0")
        target = []
        for tag in tags:
            href = tag.get("href")
            if href and "insights" in str(href):
                data = [href, tag.text.strip()]
                target.append(data)
        target = target[1:-1]
        return target 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching insights tags: {e}")
        return []

def crawl_all_link_in_tag(target):
    result = []
    for arr_tag in target:
        try:
            sub_res = []
            arr_link = []
            link = BASE_URL + arr_tag[0]
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            herf_arr = soup.find_all("a", class_="link-dark")
            
            for herf in herf_arr:
                link = herf.get("href")
                if link:
                    full_link = BASE_URL + link if not link.startswith('http') else link
                    arr_link.append(full_link)
            
            sub_res.append(arr_link)
            sub_res.append(arr_tag[1])
            result.append(sub_res)
            
            # Add a delay to avoid overwhelming the server
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error crawling links for {arr_tag[1]}: {e}")
    return result 

def crawl_infor(sub_res):
    arr_link = sub_res[0]
    tag = sub_res[1]
    all_results = []
    
    for link in arr_link:
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            
            title_tag = soup.find("h1")
            title = title_tag.text.strip() if title_tag else "No title available"
            
            abstract_tag = soup.find("div", itemprop="abstract")
            abstract = abstract_tag.text.strip() if abstract_tag else "No abstract available"
            
            content_section = soup.find("div", id="newsBody")
            if content_section :

                content_section = content_section.text.strip() 
            elif soup.find("div", itemprop = "articleBody"):
                content_section = soup.find("div", itemprop = "articleBody").text.strip()
            else :
                content_section ="No published day"

            date = soup.find('meta', attrs={'name': 'pubdate'})
            if date :
                date = date.get("content")
            else :
                date = "none"
            pubdate = datetime.strptime(date, '%Y%m%d')
    
            formatted_pubdate = pubdate.strftime('%B %d, %Y') 
            result = {
                "tag": tag,
                "link": link, 
                "title": title,
                "published_day": formatted_pubdate,
                "abstract": abstract,
                "content": content_section
            }
            print(result)
            all_results.append(result)
            
            # Add a delay to avoid overwhelming the server
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error crawling information for {link}: {e}")
    
    return all_results 

def main():
    try:
        # Get insights tags and links
        tags_and_links = get_all_insights_tag_and_link(URL)
        
        # Crawl links for each tag
        crawled_links = crawl_all_link_in_tag(tags_and_links)
        
        # Crawl information for each link
        arr_crawled_data = []
        for sub_res in crawled_links:
            crawled_data = crawl_infor(sub_res)
            arr_crawled_data.extend(crawled_data)
        
        # Save to JSON
        with open("data_insights.json", "w", encoding="utf-8") as f:
            json.dump(arr_crawled_data, f, ensure_ascii=False, indent=4)
        
        print("Scraping completed successfully!")
    
    except Exception as e:
        print(f"An error occurred during scraping: {e}")

if __name__ == "__main__":
    main()