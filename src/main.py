from lxml import html
import requests
import re
import webbrowser
import sys
import os

pattern = "https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=(.*)/+"


def addName(names):

    with open("data\\namelist.txt") as f:
        namelist = f.readlines()
    nameset = set()
    for name in namelist:
        nameset.add(name.rstrip('\n'))

    f = open("data\\namelist.txt", 'a')

    print("Adding")
    for name in names:
        print(".")
        name = name.rstrip('\n')
        if name in nameset:
            continue
        nameset.add(name)

        page = requests.get('https://www.dmm.co.jp/digital/videoa/-/list/=/article=actress/id=' + name + '/sort=date/')
        tree = html.fromstring(page.content)
        urls = [x for x in tree.xpath('//a/@href') if 'https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=' in x]
        
        videos = set()
        for url in urls:
            videos.add(re.search(pattern, url).group(1))

        with open('data\\' + name + '.txt', 'w') as hf:
            for video in videos:
                hf.write("%s\n" % video)

        f.write("%s\n" % name)
    
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

def update(argv):
    with open("data\\namelist.txt", 'r') as f:
        namelist = f.readlines()
    nameset = set()
    for name in namelist:
        nameset.add(name.rstrip('\n'))

    if argv:
        updateset = set(argv)
    else:
        updateset = nameset

    videodict = {}
    newvideodict = {}
    oldvideodict = {}
    for name in updateset:
        try:
            with open('data\\' + name + '.txt', 'r') as f:
                oldvideodict[name] = set(x.rstrip('\n') for x in f.readlines())
        except FileNotFoundError:
            pass

    for name in updateset:
        page = requests.get('https://www.dmm.co.jp/digital/videoa/-/list/=/article=actress/id=' + name + '/sort=date/')
        tree = html.fromstring(page.content)
        urls = [x for x in tree.xpath('//a/@href') if 'https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=' in x]
        
        videodict[name] = set()
        for url in urls:
            videodict[name].add(re.search(pattern, url).group(1))        

        newvideodict[name] = videodict[name].copy()
        for video in oldvideodict[name]:
            newvideodict[name].discard(video)
        
        if len(newvideodict[name]) >= 120:
            print("new page for id=" + name + "\n")
    
    for name in updateset:
        for video in newvideodict[name]:
            webbrowser.open('https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=' + video, new=2)
        
    for name in updateset:
        if len(newvideodict[name]):
            with open('data\\' + name + '.txt', 'w') as f:
                for video in videodict[name]:
                    f.write("%s\n" % video)

    
        

def main(argv):
    if len(argv) < 2:
        print("nothing to do")
        sys.exit(2)
    elif argv[1] == "initialize":
        initialize()
    elif argv[1] == "add":
        addName(argv[2:])
    elif argv[1] == "update":
        update(argv[2:])
    else:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)

    
        
