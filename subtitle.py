from bs4 import BeautifulSoup
import requests
from urllib.request import quote
import os
import zipfile

def make_sub_dir(query):
    global subspath
    subspath = "E:\\subtitle\\" + query
    print(subspath)
    if not os.path.exists(subspath):
        os.makedirs(subspath)

def search_and_return_result(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    print(soup.prettify)

    titles = [title.get_text() for title in soup.find_all('h3',{'class':'media-heading','itemprop':'name'})]
    links = [link['href']for link in soup.find_all('a')if 'imdb' in link['href']]
    return titles,links

def get_links_of_selected_sub(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    return soup.find_all('a')
    
def get_zip_links(all_links):
    for each_link in all_links:
        if 'english' in each_link['href']:
            sub_req = requests.get(base_url+each_link['href'])
            sub_soup = BeautifulSoup(sub_req.content)

            dwnld_links = [link['href'] for link in sub_soup.find_all('a')]
            for link in dwnld_links:
                if 'zip' in link:
                    print(link)
                    yield link

def dwnld_zip_files(link):
    name = link.split('/')[-1]
    zipfile_path = subspath+name

    print(name)
    print("\nDOWNLOWDING....\n")

    with open(zipfile_path,"wb") as foo:
        final_file = requests.get(link)
        for chunk in final_file.iter_content(chunk_size=1024):
            if chunk:
                foo.write(chunk)
                foo.flush()
    print("DOWNLOADED!\n\n")
    return zipfile_path


def unzip_file(zipfile_path):
    print("unziping File...\n\n")
    try:
        z = zipfile.ZipFile(zipfile_path)
        z.extractall(path=subspath)
        z.close()
        os.remove(zipfile_path)
        print("unzipped! :)\n\n")
        print("*"*40)
    except:
        print(str(e))
        print("\nFailed To Unzip...\n")
        print("*"*40)



def main():
    query = input("Enter query:\n>>")
    make_sub_dir(query)
    query = quote(query)

    global base_url
    base_url = "http://www.yifysubtitles.com"
    url = base_url+"/search?q="+query
    
    titles,links = search_and_return_result(url)
    if len(titles)==0:
        print("\nsubtitels Not Found!\n try again\n\n")
        main()
    else:
        print('\n\n')
        for num,i in enumerate(titles):
            print("Token : {}".format(num+1))
            print(i,"\n")
            print(".x"*20)
            print("\n")

    token = int(input("Enter token number : \n>>"))
    selected_sub_url = base_url + links[token-1]

    all_links = get_links_of_selected_sub(selected_sub_url)
    dwnld_link = get_zip_links(all_links)

    num = int(input("\nHow many Subs You Want?\n>> "))

    for i in range(num):
        try:
            zip_path = dwnld_zip_files(next(dwnld_link))
            unzip_file(zip_path)
        except Exception as e:
            print(str(e))
            print("No More Available :(")
            break
    action = input("\n * Do You want to quit? (y/n) \n").lower()

    if action == 'n':
        main()
    else:
        exit(0)

if __name__ == '__main__':  
    print("YIFY-Subs".center(40,'-'))    
    main()
