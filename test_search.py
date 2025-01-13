from googlesearch import search
for i in search("site:http://www.ime.cas.cn/ 半导体",lang='zh'):
    print(i)
# print(search("Google"))


# import wikipediaapi

# def get_wikipedia_summary(page_title, lang='en'):
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
#     wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent,language=lang)
#     page = wiki_wiki.page(page_title)

#     if page.exists():
#         print(f"Title: {page.title}")
#         print(f"Summary:\n{page.summary}")
#     else:
#         print(f"Page '{page_title}' does not exist in the '{lang}' language Wikipedia.")

# if __name__ == "__main__":
#     # Example: Get a summary for the 'Python (programming language)' page
#     get_wikipedia_summary(page_title="PoC",lang='en')

