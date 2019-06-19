from bs4 import BeautifulSoup
import requests
import enum
from pprint import pformat
import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)


class Scraper():
    
    @staticmethod
    def getChapter(obj):
        chapter_number = 'chapter_'+str(obj.get('chapter'))
        final_dict = (chapter_number, [])
        
        
        url = Scraper.urlBuilder(UrlType.chapter.name,
                                 obj.get('name'), chapter_number)

        logging.info(pformat(url))
        soup = Scraper.getSoup(url)
        image_div = soup.find('div', attrs={'class': 'vung-doc'})
        images = image_div.findAll('img')
        
        
        for link in images:
            final_dict[1].append(link.get('src'))

        logging.info(pformat(final_dict))
        return final_dict


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
        story_item = soup.findAll('h3', attrs= {'class': 'story_name'})
        for item in story_item:
            link = item.find('a')
            search_results[link.string] = link.get('href')

        logging.info('search result: %s', str(search_results))
        return search_results

        
    @staticmethod
    def getMangaInfo(name):
        manga_info = dict(count=0, chapters=[])

        url = Scraper.urlBuilder(UrlType.manga.name, name)

        soup = Scraper.getSoup(url)

        chapter_list = soup.find('div', attrs={'class': 'chapter-list'})

        chapters = chapter_list.findAll('div', attrs={'class': 'row'})
        manga_info['count'] = len(chapters)
        for chapter in chapters:
            link = chapter.find('a')
            manga_info['chapters'].append({link.get('title'): link.get('href')})
        
        # logging.info('manga info: %s', str(manga_info))
        return manga_info

    
    @classmethod
    def getSoup(cls, url):
        html = requests.get(url)
        return BeautifulSoup(html.content, 'html.parser')

    @classmethod
    def urlBuilder(cls, enumType, *args):
        base_url = 'https://manganelo.com/'+enumType
        separator = '/'
        for word in args:
            base_url = base_url+separator+word

        return base_url


class UrlType(enum.Enum):
    search = 'search'
    manga = 'manga'
    chapter = 'chapter'
