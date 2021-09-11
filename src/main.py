from lxml import html
import re
import sys
import os
from selenium import webdriver

pattern = "https://www.r18.com/videos/vod/movies/detail/-/id=(.*)/\?dmmref=video.movies.new+"

def addName(names):

    with open("data\\namelist.txt") as f:
        namelist = f.readlines()
    nameset = set()
    for name in namelist:
        nameset.add(name.rstrip('\n'))

    f = open("data\\namelist.txt", 'a')

    print("Adding")
    driver = webdriver.Firefox()
    driver.get("https://www.r18.com/")
    driver.find_element_by_link_text("Yes, I am.").click()
    for name in names:
        print(".")
        name = name.rstrip('\n')
        if name in nameset:
            continue
        nameset.add(name)

        page = driver.get('https://www.r18.com/videos/vod/movies/list/id=' + name + '/pagesize=30/price=all/sort=new/type=actress/page=1/')
        videos = set(re.findall(pattern, driver.page_source))

        with open('data\\' + name + '.txt', 'w') as hf:
            for video in videos:
                hf.write("%s\n" % video)

        f.write("%s\n" % name)
    
    driver.quit()
    f.close()
    print("done")

def initialize():
    with open("data\\namelist.txt") as f:
        namelist = f.readlines()
    
    for name in namelist:
        try:
            os.remove("data\\" + name.rstrip('\n') + ".txt")
        except:
            pass
     
    with open("data\\namelist.txt", "w") as f:
        pass

def removeName(argv):
    with open("data\\namelist.txt", 'r') as f:
        namelist = f.readlines()
    nameset = set()
    for name in namelist:
        nameset.add(name.rstrip('\n'))
    print("Removing")
    removecount = 0
    for name in argv:
        print(".")
        name = name.rstrip('\n')
        nameset.discard(name)
        try:
            os.remove("data\\" + name + ".txt")
            removecount += 1
        except:
            pass
    if removecount:
        with open("data\\namelist.txt", "w") as f:
            for name in nameset:
                f.write("%s\n" % name)

def update(argv):
    
    if argv:
        updateset = set(argv)
    else:
        with open("data\\namelist.txt", 'r') as f:
            namelist = f.readlines()
        nameset = set()
        for name in namelist:
            nameset.add(name.rstrip('\n'))
        updateset = nameset

    videodict = {}
    newvideodict = {}
    oldvideodict = {}

    print("Updating")

    for name in updateset:
        try:
            with open('data\\' + name + '.txt', 'r') as f:
                oldvideodict[name] = set(x.rstrip('\n') for x in f.readlines())
        except FileNotFoundError:
            with open('data\\' + name + '.txt', 'w') as hf:
                oldvideodict[name] = set()
    driver = webdriver.Firefox()
    driver.get("https://www.r18.com/")
    driver.find_element_by_link_text("Yes, I am.").click()
    for name, oldvideos in oldvideodict.items():

        print(".")
        driver.get('https://www.r18.com/videos/vod/movies/list/id=' + name + '/pagesize=30/price=all/sort=new/type=actress/page=1/')
        pageSource = driver.page_source
        videodict[name] = set(re.findall(pattern, pageSource))    
        newvideodict[name] = videodict[name].copy()

        for video in oldvideos:
            newvideodict[name].discard(video)
        
        if len(newvideodict[name]) >= 30:
            print("new page for id=" + name + "\n")
    
    newvideoset = set()
    for name, newvideos in newvideodict.items():
        if newvideos:
            for video in newvideos:
                if video not in newvideoset:
                    newvideoset.add(video)
                    print('https://www.r18.com/videos/vod/movies/detail/-/id=' + video + '\n')
            with open('data\\' + name + '.txt', 'w') as f:
                for video in videodict[name]:
                    f.write("%s\n" % video)

    driver.quit()
    print("done")

    
def main(argv):
    if len(argv) < 2:
        update(None)
    elif argv[1] == "initialize":
        initialize()
    elif argv[1] == "add":
        addName(argv[2:])
    elif argv[1] == "update":
        update(argv[2:])
    elif argv[1] == "remove":
        removeName(argv[2:])
    else:
        print(argv[1] + " undefined") 
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)