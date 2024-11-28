import requests 
from bs4 import BeautifulSoup
import json 
URL = "https://www.iso.org/insights"
BASE_URL= "https://www.iso.org"
def get_all_insights_tag_and_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.find_all("a", class_ = "nav-link ps-0")
    target =[]
    for tag in tags :
        href = tag.get("href")
        if "insights" in str(href).split("/"):
            data = []
            data.append(tag.get("href"))
            data.append(tag.text)
            target.append(data)
    target = target[1:-1]
    return target 
def crawl_all_link_in_tag(target):
    result = []
    for arr_tag in target :
        sub_res =[]
        arr_link=[]
        link = BASE_URL + arr_tag[0]
        response =requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        herf_arr = soup.find_all("a", class_= "link-dark")
        for herf in herf_arr :
            link = herf.get("href")
            arr_link.append(BASE_URL+ link)
        sub_res.append(arr_link)
        sub_res.append(arr_tag[1])
        result.append(sub_res)
    return result 
def crawl_infor(sub_res):
    arr_link = sub_res[0]
    tag = sub_res[1]
    all_results =[]
    for link in arr_link :
        response = requests.get(link)
        soup = BeautifulSoup(response.text , "html.parser")
        title = soup.find("h1").text.strip()
        abstract_tag = soup.find("div", itemprop="abstract")
        abstract = abstract_tag.text.strip() if abstract_tag else "No abstract available"
        table_of_contents = soup.find_all("h2")
        content_section = soup.find("div", id="newsBody")
        all_headers_in_content = content_section.find_all("h2") if content_section else []
        content_data = [] 
        for i in range(len(all_headers_in_content) - 1):
            p_elements = all_headers_in_content[i].find_all_next('p')
            section_content = {"header": all_headers_in_content[i].text.strip(), "paragraphs": []}
            for p in p_elements:
                if p.find_previous_sibling('h2') == all_headers_in_content[i]:
                    section_content["paragraphs"].append(p.text.strip())
            content_data.append(section_content)
        if all_headers_in_content:
            last_header = all_headers_in_content[-1]
            p_elements = last_header.find_all_next('p')
            last_section = {"header": last_header.text.strip(), "paragraphs": []}
            for p in p_elements:
                last_section["paragraphs"].append(p.text.strip())
            content_data.append(last_section)
        result = {
            
            "tag" : tag,
            "link": link, 
            "title": title,
            "abstract": abstract,
            "content": content_data
        }
        all_results.append(result)
    return all_results 
sub_res = [["https://www.iso.org/home/insights-news/navigation-menu-hidden/renewable-energy.html"], "Renewable energy"]
# res  = crawl_all_link_in_tag(get_all_insights_tag_and_link(URL))
arr_crawled_data =[]

crawled_data = crawl_infor(sub_res)
arr_crawled_data.append(crawled_data)
with open("a.json", "w", encoding="utf-8") as f:
    json.dump(arr_crawled_data, f, ensure_ascii=False, indent=4)
print("xong")

