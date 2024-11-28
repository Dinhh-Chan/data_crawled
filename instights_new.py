from bs4 import BeautifulSoup
import requests
import json
import time

BASE_URL = "https://www.iso.org"
expert_talk_link = "https://www.iso.org/cms/render/live/en/sites/isoorg/home/insights-news/navigation-menu-hidden/renewable-energy/pagecontent/section-insights-latest/section-insights-latest/row-insights-latest-title/row-insights-latest-title-main/latest-insights.html.ajax?nb-74d62af8-ecea-4b05-8f70-a2667c33d9dd=8&offset-74d62af8-ecea-4b05-8f70-a2667c33d9dd=0&tag="

def get_all_link(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, "html.parser")
        a_tag = soup.find_all("a", class_="link-dark")
        arr_link = [BASE_URL + a.get("href") for a in a_tag]
        return arr_link
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

arr_crawled_data = []

def crawl_infor(arr_link, tag):
    for link in arr_link:
        try:
            print(f"Crawling: {link}")
            response = requests.get(link)
            response.raise_for_status()  # Check if the request was successful
            soup = BeautifulSoup(response.text, "html.parser")

            # Title extraction
            title = soup.find("h1").text.strip() if soup.find("h1") else "No title found"

            # Abstract extraction
            abstract_tag = soup.find("div", itemprop="abstract")
            abstract = abstract_tag.text.strip() if abstract_tag else "No abstract available"

            # Content extraction
            content = soup.find("div", id="newsBody")
            if content is None:
                content = soup.find("div", itemprop="articleBody")
                if content is None:
                    content = soup.find("div", class_="row row-bottom-sm row-sticky")
                    content = content.text.strip() if content else "No content available"
                else:
                    content = content.text.strip()
            else:
                content = content.text.strip()

            # Store the extracted data
            res = {
                "tag": tag,
                "link": link,
                "title": title,
                "abstract": abstract,
                "content": content
            }
            arr_crawled_data.append(res)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {link}: {e}")
        time.sleep(1)  # Delay between requests to avoid overloading the server

# Crawl 'Expert talk' section
crawl_infor(get_all_link(expert_talk_link), "Renewable energy")

# Optional: Uncomment and loop through more sections if needed (e.g., "Standards world")
# for i in standards_world_links:
#     crawl_infor(get_all_link(i), "Standards world")

# Save crawled data to JSON file
with open("a.json", "w", encoding="utf-8") as f:
    json.dump(arr_crawled_data, f, ensure_ascii=False, indent=4)

print("Crawling complete. Data written to 'iso_insight_news_data.json'.")
