import ocwdl
import os
import re
import wget





def main():
    ocw = ocwdl.course('https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/','/home/ahacad/test/OCW')
    ocw.download('/home/ahacad/test/OCW/6-006-introduction-to-algorithms-fall-2011', choice = 'lecture-notes')

if __name__ == '__main__':
    main()

