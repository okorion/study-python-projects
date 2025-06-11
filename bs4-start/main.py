from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/news")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")
articles = soup.find_all(name="tr", class_="athing")

article_texts = []
article_links = []
article_upvotes = []

for article in articles:
    # 제목, 링크
    titleline = article.find("span", class_="titleline")
    a_tag = titleline.find("a")
    title = a_tag.get_text()
    link = a_tag.get("href")

    # 해당 tr 다음 tr에서 점수 가져오기
    next_row = article.find_next_sibling("tr")
    score_tag = next_row.find("span", class_="score")

    if score_tag:
        score = int(score_tag.get_text().split()[0])
        article_texts.append(title)
        article_links.append(link)
        article_upvotes.append(score)

# 최대 upvote 기사 정보 출력
largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)

print("🔥 가장 높은 upvote 기사:")
print("제목:", article_texts[largest_index])
print("링크:", article_links[largest_index])
print("업보트:", largest_number)

#
# with open("website.html", encoding="utf-8") as file:
#     contents = file.read()
#
# soup = BeautifulSoup(contents, "html.parser")
# # print(soup.title)
# # print(soup.title.string)
#
# # print(soup.prettify())
#
# # print(soup.p)
#
# all_anchor_tags = soup.find_all(name="a")
# print(all_anchor_tags)
#
# for tag in all_anchor_tags:
#     # print(tag.getText())
#     print(tag.get("href"))
#
# heading = soup.find(name="h1", id="name")
#
# class_is_heading = soup.find_all(class_="heading")
# print(class_is_heading)
#
# h3_heading = soup.find(name="h3", class_="heading")
# print(h3_heading)
#
# name = soup.select_one("#name")
# print(name)
#
# headings = soup.select(".heading")
# print(headings)
