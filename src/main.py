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

        page = requests.get('https://www.dmm.co.jp/digital/videoa/-/list/=/article=actress/id=' + name + '/limit=30/sort=date/')
        videos = set(re.findall(pattern, page.text))

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

    print("Updating")

    for name in updateset:
        try:
            with open('data\\' + name + '.txt', 'r') as f:
                oldvideodict[name] = set(x.rstrip('\n') for x in f.readlines())
        except FileNotFoundError:
            pass

    for name, oldvideos in oldvideodict.items():

        print(".")
        page = requests.get('https://www.dmm.co.jp/digital/videoa/-/list/=/article=actress/id=' + name + '/limit=30/sort=date/')
        
        videodict[name] = set(re.findall(pattern, page.text))    
        newvideodict[name] = videodict[name].copy()

        for video in oldvideos:
            newvideodict[name].discard(video)
        
        if len(newvideodict[name]) >= 30:
            print("new page for id=" + name + "\n")
    
    newvideoset = set()
    for name, newvideos in newvideodict.items():
        if newvideos:
            with open('data\\' + name + '.txt', 'w') as f:
                for video in videodict[name]:
                    f.write("%s\n" % video)
            for video in newvideos:
                if video not in newvideoset:
                    newvideoset.add(video)
                    webbrowser.open('https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=' + video, new=2)        

    print("done")

    
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
    elif argv[1] == "remove":
        removeName(argv[2:])
    else:
        print(argv[1] + " undefined") 
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
