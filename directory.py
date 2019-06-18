import os

class MangaDirectory(object):
    
    def __init__(self, basedir, name):
        self.name = name
        self.basedir = basedir
        if MangaDirectory.checkExists(name, basedir) == False:
            MangaDirectory.createFolder('/home/amshel/', 'Manga')
    
    @classmethod
    def createFolder(cls, basedir, name):
        if cls.checkExists(name, basedir) == False:
            path = basedir+name
            os.mkdir(path)
        return path
        
    def multipleDirs(self, basedir, *args):

        folder = ''
        for arg in args:
            folder= folder +arg+'/'
        path = basedir+folder
        os.makedirs(path)
        return path

    def list_chapters(self):
        return len(os.listdir(self.basedir+self.name))
    
    @classmethod
    def checkExists(cls, name, basedir):
        if name in os.listdir(basedir):
            return True
        else:
             return False

    @staticmethod
    def createTempFile():
        if os.path.exists('temp.json') == False:
            open('temp.json', 'x')
    
    @staticmethod
    def deleteTempFile():
        if os.path.exists('temp.json'):
            os.remove('temp.json')
        
    @staticmethod    
    def saveDictToTemp(data):
        if os.path.exists('temp.json'):
            file = open('temp.json', 'a')
            file.write(data)

            file.close()
