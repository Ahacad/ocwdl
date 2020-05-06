#! /usr/bin/env python

import os
import re
import urllib.request
from bs4 import BeautifulSoup as BSP
import wget
import argparse
from header import *


class course():
    
    def __init__(self, pageUrl, outputLocation, name=None, choices=["assignments", "exams"]):
        """
        self.outputLocation  : the place where courses resources lay
        self.mainPageUrl     : the url of the main page of the very course in OCW
        self.name            : the name of the course
        self.dlFolder        : the place where resources of the very course will be downloaded
        """
        self.pageUrl = pageUrl
        self.outputLocation = outputLocation
        
    def startocw(self, fileTypes=[r'pdf', r'zip', r'gz', r'tex', r'png', r'ipynb', r'py', r'tar', r'c', r'cpp'], choices=None):
            self.dlPage(self.outputLocation,
                        fileTypes=fileTypes)

    def dlPage(self, downloadLocation, fileTypes=[r'pdf', r'zip', r'gz', r'tex', r'png', r'ipynb', r'py', r'tar', r'c', r'cpp']):

        downloadUrl = self.pageUrl
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
            print('\n\n\n' + BARRIER + '\n' + '                   ###FINISHED DOWNLOAD' 
                  + str(fileType) + '###\n' + BARRIER + '\n') 


    def dlFile(self, location, url, header = "https://ocw.mit.edu"):
        """
        down file from url to location
        location should be a folder, and url should be complete
        """
        if url[0] != 'h':
            url = header + url

        print('\n'+ BARRIER + '\n###Downloading:', url,'###\n' + BARRIER + '\n')
        wget.download(url, out=location)
        


def readFromFile(fileName):
    """get course urls from file"""
    with open(fileName, 'r') as f:
        for line in f:
            try:
                ocw = course(line[:-1], "/home/ahacad/test/OCW")
            except Exception:
                print(ERROR)
                print('error happening while downloading   ' + str(line) + '\n')
                with open('/home/ahacad/ocwdlerror', 'a') as f:
                    f.write('error happening while downloading   ' + str(line) + '\n')
            finally:
                pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="please input"
                        "the url of the main page")
    # parser.add_argument("-l", "--list", help="read from list in a text file")
    # parser.add_argument("-c", "--choices", help="the subsections in"
                        # " the main page, like 'exams', 'projects'")
    # parser.add_argument("-t", "--types", help="customize your file types")
    parser.add_argument("-r", "--recursive", help="download a page "
                        "recursively, default off", action="store_true")
    parser.add_argument("-o", "--output", help="output location", default = './')

    args = parser.parse_args()

    # choices = args.choices
    # if choices: 
        # choices = choices.split(' ')
    # types = args.types
    # if types:
        # types = types.split(' ')
    # else:
        # types = [r'pdf', r'zip', r'gz', r'tex', r'png', r'ipynb', r'py', r'tar', r'c', r'cpp']
    # if args.list:
        # readFromFile(args.list)
        # return 0
    ocw = course(args.url, args.output)
    ocw.startocw()
    

if __name__ == "__main__":
    main()




#"https://ocw.mit.edu/courses/mathematics/18-06-linear-algebra-spring-2010/", "/home/ahacad/test/OCW"
