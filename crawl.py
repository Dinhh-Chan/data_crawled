import requests 
from bs4 import BeautifulSoup
import json 
URL = "https://www.iso.org/insights"
BASE_URL= "https://www.iso.org"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
a_tags = soup.find_all("a", class_= "nav-link ps-0")
print(len(a_tags))
insights_tag = []
news_tag =[]
for a_tag in a_tags :
    href= a_tag.get("href")
    if "insights" in str(href).split("/"):
        insights_tag.append(a_tag)
    else:
        news_tag.append(a_tag)
insights_tag = insights_tag[1:]
def crawl_insights_links(a_tag):
    link = BASE_URL + a_tag.get("href")
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    href_arr = soup.find_all("a", class_= "link-dark")
    return href_arr
def crawl_info(url):
    tag = url[1:]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
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
        "title": title,
        "abstract": abstract,
        "content": content_data
    }
    return json.dumps(result, indent=4)


