import os, sys
from pprint import pprint, pformat
from PyInquirer import prompt
from examples import custom_style_1
from scraper import Scraper
from downloader import Downloader



import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)


class cli():
    def __init__(self):
        print('Welcome to manga downloader')
        # check if the user has 
        if not os.path.exists('.env'):
            self.first_launch()
            
        self.manga_obj = dict()
        self.chaptersToDownload()
        pass

    def first_launch(self):
        basedir = os.environ.get('HOME')
        # windows system
        if basedir is None:
            basedir = os.environ.get('HOMEPATH')
        
        with open('.env', 'w') as f:
            data = 'DOWNLOAD='+basedir+"/Manga"
            f.write(data)
        return True 
    
    def searchManga(self):
        questions = [
            {
                'type': 'input',
                'name': 'manga',
                'message': 'Enter the name of the manga you want to download?'
            },
        ]
        obj = prompt(questions, style=custom_style_1)
        self.manga_obj['typed_name'] = obj.get('manga')
                

    def searchResults(self):
        self.searchManga()
        manga_name = self.manga_obj.get('typed_name')
        choices = Scraper.getSearchResults(manga_name)
        if len(choices) < 1:
            print("MANGA NOT FOUND")
            sys.exit()

        questions = [
            {
                'type': 'list',
                'name': 'manga',
                'message': 'Search Results',
                'choices': choices.keys()
            },
        ]

        obj = prompt(questions, style=custom_style_1)
        self.manga_obj['manga'] = obj.get('manga')
        self.manga_obj['link'] = choices.get(obj['manga'])
        self.manga_obj['url_name'] = cli.getName(self.manga_obj.get('link'))

    def chaptersToDownload(self):
        self.searchResults()
        chapters = Scraper.getMangaInfo(self.manga_obj.get('url_name'))
        self.manga_obj['total'] = chapters.get('count')
        print('{} has {} chapters'.format(self.manga_obj.get('manga'), self.manga_obj.get('total')))
        questions = [
            {
                'type': 'input',
                'name': 'chapters',
                'message': 'Which Chapters you want to download? ie 1 or 1-7 or all'
            },
        ]

        obj = prompt(questions, style=custom_style_1)
        
        self.fetchChapters(obj.get('chapters'))
        pass
    
    def fetchChapters(self, chapters):
        if chapters.isnumeric():
            self.manga_obj['chapters'] = int(chapters)
        elif chapters.isalpha():
            self.manga_obj['chapters'] = range(1, self.manga_obj.get('total'))
        elif len(chapters.split('-')) > 1:
            lst = [int(i) for i in chapters.split('-')]
            self.manga_obj['chapters'] = range(lst[0], lst[1]+1)
        else:
            print('invalid input')
            return
        logging.info(pformat(self.manga_obj))
        Downloader(self.manga_obj)
        pass


    @classmethod
    def getName(cls, url):
        url_list = url.split('/')
        last_index = 0
        if len(url_list) > 0:
            last_index = len(url_list) - 1
        
        return url_list[last_index]
