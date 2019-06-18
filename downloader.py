import requests, os, ast
from directory import MangaDirectory

class Downloader():
    def __init__(self):
        self.directory = MangaDirectory('/home/amshel/', 'Manga')
        data = open('temp.json', 'r')
        self.parsed_dict = ast.literal_eval(data.read())
        
    def startDownload(self):
        self.path = self.directory.multipleDirs('/home/amshel/Manga/', self.parsed_dict.get('manga'), self.parsed_dict.get('chapter'))
        for link in self.parsed_dict.get('url_list'):
            self.downloadManga(link, self.parsed_dict.get('url_list').index(link))
        

    def downloadManga(self, url, index):
        response = requests.get(url)
        
        with open(self.path+str(index)+'.jpg', 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)