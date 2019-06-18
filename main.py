import requests, os
from directory import MangaDirectory
from scraper import Scraper
from downloader import Downloader


print('Welcome to manga downloader')
manga_name = input('Please enter name of manga you wish to download: ')
results = Scraper.getSearchResults(manga_name)

print('Type a number tha matches the manga: ')
search_list = []
for result in results.keys():
    search_list.append(result)
    print(str(search_list.index(result))+':'+result)

num = int(input("Enter Number: "))

real_name = Scraper.getName(results.get(search_list[num]))

scraper = Scraper(real_name)
manga_info = scraper.getMangaInfo()

print(search_list[num]+ " has {} chapters".format(manga_info.get('count')))
print("Select which chapter to download. ie 10 for chapter 10")
chapter = int(input('Chapter to download: '))

scraper.getImagesUrl(chapter)


job = Downloader()
job.startDownload()








