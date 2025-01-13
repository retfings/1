from bs4 import BeautifulSoup
import requests
from copy import deepcopy
import csv
key_words = ['semiconductor','semi-conductor','Metrology','Ion Implantation','Epitaxy','Chemical Vapor Deposition','Cleanroom','Doping','Etching','Photolithography','Silicon','quantum physics']
template = {
    'name':'',
    'author':'',
    'year':'',
    'link':''
}
def scrapy(keyword):
    result = []
    base_url = 'https://libgen.gs/index.php?req='+str(keyword)+'&topics%5B%5D=l&curtab=f&order=&ordermode=desc&filesuns=all&page='
    for i in range(20):
        url = base_url + str(i+1)
        print("scrapying the url:"+str(url)+"……")
        try:
            text = requests.get(url).text   

            soup = BeautifulSoup(text,'html.parser')
            soup = soup.find("table",{'class':'table table-striped'})
            soup = soup.find("tbody")
            elem = soup.find_all('tr')

            
            for ele in elem:#每本书
                book = deepcopy(template)
                info = ele.find_all("td") 
                name = info[0].find("a").text
                author = info[1].text
                year = info[3].text
                link = info[8].find("a").get("href")

                book['name'] = str(name)
                book['author'] = str(author)
                book['year'] = str(year)
                
                text = requests.get(link).text
                soup = BeautifulSoup(text,'html.parser')
                soup = soup.find("table")
                link = soup.find("a").get("href")
                book['link'] = 'https://libgen.rocks/' + link
                result.append(book)
        except:
                print("页面太少，无法加载")
    return result

with open("book_list.csv","w",encoding = "utf-8") as f:
    writer = csv.DictWriter(f,fieldnames = ['name','author','year','link'])
    writer.writeheader()
    for key_word in key_words:
        result = scrapy(key_word)
        for row in result:
            writer.writerow(row)
