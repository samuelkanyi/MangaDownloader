from bs4 import BeautifulSoup
import requests, enum
from directory import MangaDirectory

class Scraper():
    
    # the name is the actual manga as represented in the url
    def __init__(self, name):
        self.name = name
        MangaDirectory.deleteTempFile()
        pass

    @classmethod
    def getSoup(cls, url):
        html = requests.get(url)
        return BeautifulSoup(html.content, 'html.parser')

    
    def getMangaInfo(self):
        manga_info = dict(count=0, chapters= [])

        url = Scraper.urlBuilder(UrlType.manga.name, self.name)

        soup = Scraper.getSoup(url)

        chapter_list = soup.find('div', attrs={'class':'chapter-list'})

        chapters = chapter_list.findAll('div', attrs={'class':'row'})
        manga_info['count'] = len(chapters)
        for chapter in chapters:
            link = chapter.find('a')
            manga_info['chapters'].append({link.get('title'):link.get('href')})
        return manga_info

    def getImagesUrl(self, num):
        chapter_number = 'chapter_'+str(num)
        final_dict = dict(manga= self.name, chapter=chapter_number, url_list=[])
        
        url = Scraper.urlBuilder(UrlType.chapter.name, self.name, chapter_number)
        soup = Scraper.getSoup(url)
        image_div = soup.find('div', attrs={'class':'vung-doc'})
        images = image_div.findAll('img')

        for link in images:
            final_dict['url_list'].append(link.get('src'))

        MangaDirectory.createTempFile()
        MangaDirectory.saveDictToTemp(str(final_dict))

    # This function will take a string name and return list containing a
    # dictionary of name of the manga and the url
    @staticmethod
    def getSearchResults(name):
        search_results = dict()
        
        fname = name.replace(" ", "_")
        # build sarch url
        url = Scraper.urlBuilder(UrlType.search.name, fname)
        
        soup = Scraper.getSoup(url)
        
        # get the div that contains the info i need
        story_item = soup.findAll('h3', attrs= {'class':'story_name'})
        for item in story_item:
            link = item.find('a')
            search_results[link.string] = link.get('href')
        
        return search_results

    @classmethod
    def urlBuilder(cls, enumType, *args):
        base_url = 'https://manganelo.com/'+enumType
        separator = '/'
        for word in args:
            base_url = base_url+separator+word
        
        return base_url
    
    @classmethod
    def getName(cls, url):
        url_list = url.split('/')
        last_index = 0
        if len(url_list) > 0:
            last_index = len(url_list) - 1
        
        return url_list[last_index]

class UrlType(enum.Enum):
    search = 'search'
    manga = 'manga'
    chapter = 'chapter'