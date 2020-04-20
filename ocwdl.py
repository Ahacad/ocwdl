#! /usr/bin/env python

import os 
import re
import urllib.request
from bs4 import BeautifulSoup as BSP
import wget

namePattern = r'/[\~A-Za-z0-9-.:_]*/'
filePattern = r'[\~A-Za-z0-9-/.:_]*' 

BARRIER = r'##############################################################'
ERROR = r'ERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERROR'




class course():
    
    def __init__(self, mainPageUrl, outputLocation, name = None):
        """
        self.outputLocation  : the place where courses resources lay
        self.mainPageUrl     : the url of the main page of the very course in OCW
        self.name            : the name of the course
        self.dlFolder        : the place where resources of the very course will be downloaded to
        """
        
        self.outputLocation = outputLocation
        self.mainPageUrl = mainPageUrl
        if name == None:
            self.name = re.findall(namePattern, self.mainPageUrl)[-1][1:-1]
        
        # make folders to store files
        if not os.path.exists(self.outputLocation):
            os.mkdir(self.outputLocation)
        self.dlFolder = self.outputLocation + '/' + self.name
        if not os.path.exists(self.dlFolder):
            os.mkdir(self.dlFolder)
        # -- * --
        
    def startocw(self):
        try:
            self.download(downloadLocation = self.dlFolder, choice = "assignments")
        finally:
            self.download(downloadLocation = self.dlFolder, choice = "exams")


    def dlPage(self, downloadLocation, choice = '', fileTypes = [r'pdf', r'zip', r'gz', r'tex', r'png', r'ipynb', r'py']):

        # make folder to store files
        if not os.path.exists(downloadLocation):
            os.mkdir(downloadLocation)
        downloadLocation = downloadLocation + '/' + choice
        if not os.path.exists(downloadLocation):
            os.mkdir(downloadLocation)
        # -- * -- 

        downloadUrl = self.mainPageUrl + '/' + choice
        html = urllib.request.urlopen(downloadUrl)
        bs = BSP(html, 'html.parser')

        
        for fileType in fileTypes:
            filefinds = bs.find_all('a', {'href':re.compile(filePattern + r'.' + fileType)})
            for filefind in filefinds:
                try:
                    self.dlFile(downloadLocation, filefind['href'])
                except:
                    print('\n' + ERROR + '\n')
                    with open('./ocwdlerror', 'a') as f:
                        f.write('error happened while downloading' + str(filefind) + '\n')
                finally:
                    pass
            print('\n\n\n' + BARRIER + '\n' + '                   ###FINISHED DOWNLOAD' + str(fileType) + '###\n' + BARRIER + '\n') 


    def dlFile(self, location, url, header = "https://ocw.mit.edu"):
        """
        down file from url to location
        location should be a folder, and url should be complete
        """
        if url[0] != 'h':
            url = header + url

        if not os.path.exists(location):
            os.mkdir(location)
        print('\n'+ BARRIER + '\n###Downloading:', url,'###\n' + BARRIER + '\n')
        wget.download(url, out=location)
        


def readFromFile(fileName):
    """get course urls from file"""
    with open(fileName, 'r') as f:
        for line in f:
            try:
                ocw = course(line[:-1], "/home/ahacad/test/OCW")
            except:
                print(ERROR)
                print('errow happening while downloading   ' + str(line) + '\n')
                with open('/home/ahacad/ocwdlerror', 'a') as f:
                    f.write('errow happening while downloading   ' + str(line) + '\n')
            finally:
                pass


def main():
    #ocw = course("https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/", "/home/ahacad/test/OCW")
    readFromFile("/home/ahacad/ocwlist")
    

if __name__ == "__main__":
    main()

#"https://ocw.mit.edu/courses/mathematics/18-06-linear-algebra-spring-2010/", "/home/ahacad/test/OCW"
