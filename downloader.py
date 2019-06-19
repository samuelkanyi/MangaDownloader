import os
import requests
from queue import Queue
from threading import Thread
from pprint import pformat, pprint
from scraper import Scraper
import logging
from dotenv import load_dotenv


logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

class Downloader():
    def __init__(self, obj):
        load_dotenv()
        self.obj = obj
        self.manga = obj.get('manga')
        self.chapter = obj.get('chapters')
        self.basedir = os.getenv('DOWNLOAD')
        
        if type(self.chapter) == int:
            item = dict(chapter=self.chapter, name= obj.get('url_name'))
            self.download_single(item)
            pass
        elif type(self.chapter) == range:
            self.queue = Queue()
            self.enqueue()
        pass
    
    def download_single(self, obj):
        images = Scraper.getChapter(obj)
        return self.download_manga(images[0], images[1]) 

    def enqueue(self):
        num_of_threads = 5
        for chapter in self.chapter:
            structure = dict(chapter=chapter, name=self.obj.get('url_name'))
            self.queue.put(structure)
            pass
        
        for i in range (num_of_threads):
            worker = Thread(target=self.multithreading, args= (self.queue, ))
            worker.setDaemon(True)
            worker.start()
        
        self.queue.join()
        print('All chapters downloaded')
        print('Download at '+os.getenv('DOWNLOAD'))

    def multithreading(self, q):
        while True:
            self.download_single(q.get())
            q.task_done()
        
        pass

    def download_manga(self, chapter, links):
        # create directory
        if not os.path.exists(f'{self.basedir}/{self.manga}/{chapter}'):
            os.makedirs(f'{self.basedir}/{self.manga}/{chapter}/')
        
        path = f'{self.basedir}/{self.manga}/{chapter}/'
        for url in links:
            image_name = __class__.getName(url)
            response = requests.get(url)
            with open(path+image_name, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)

        
        print(f"Download for {self.manga} {chapter} has completed")
        return True
            
    @classmethod
    def getName(cls, url):
        url_list = url.split('/')
        last_index = 0
        if len(url_list) > 0:
            last_index = len(url_list) - 1
        
        return url_list[last_index]