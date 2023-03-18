import requests as re
from bs4 import BeautifulSoup

URL = "https://kaggle.com"
response = re.get(URL)
print("response = " , response)
print("Type = ",  type(response))
print("Text = ", response.text)
print("Content = ", response.content)
print("Status_code = ", response.status_code)

if response.status_code != 200:
    print("HTTP connection is not successful! Try again")
else:
    print("HTTP connection is successful!")

soup = BeautifulSoup(response.content, "html.parser")

print("Title with tags = ", soup.title)
print("Title with tags = ", soup.title.text)

for link in soup.find_all("link"):
    print(link.get("href"))

print(soup.get_text())

# Vid one ends here

import os

# 1 Create a folder to save HTML files

folder = "mini_dataset"

if not os.path.exists(folder):
    os.mkdir(folder)


# 2 Define a function that scrapes and returns it

def scrape_content(URL):
    response = re.get(URL)
    if response.status_code == 200:
        print("HTTP connection is Successful! for URL : ", URL)
        return response
    else:
        print("HTTP connection is not Successful! for the URL : ", URL)
        return None


# 3 define a function to save HTML file for the scraped Webpages in a directory folder

path = os.getcwd() + "/" + folder

def save_html(to_where, text, name):
    file_name  = name + ".html"

    with open(os.path.join(to_where,file_name), "w", encoding="utf-8") as f:
        f.write(text)
    # with open(os.path.join(to_where,file_name), "w") as f:
    #     f.write(text)

test_text = response.text
save_html(path, test_text, "example")


# 4 Define a URL list

URL_list = [
    "https://www.kaggle.com",
    "https://www.stackoverflow.com",
    "https://www.researchgate.net",
    "https://www.python.org",
    "https://www.w3schools.com",
    "https://wwwen.uni.lu",
    "https://github.com",
    "https://scholar.google.com",
    "https://www.mendeley.com",
    "https://www.overleaf.com",
    "https://in.tradingview.com"
]


# 5 Define a function which takes URL list as parameter and run step 2 and 3 for each step

def create_mini_dataset(to_where, URL_list):
    for i in range(0, len(URL_list)):
        content = scrape_content(URL_list[i])
        if content is not None:
            save_html(to_where, content.text, str(i))
        else:
            pass
    print("Mini_dataset is Created !")

create_mini_dataset(path, URL_list)


# 6 Check if you have 10 different files