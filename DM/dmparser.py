import requests
from bs4 import BeautifulSoup
import json
import time


class DMParser:

    def __init__(self):
        self.mainPageUrl = 'https://darkmoney.la'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        self.session = requests.session()
        

    def autorize(self):
        self.cookiesArray = requests.cookies.RequestsCookieJar()
        self.cookiesArray.set('IDstack', '%2C232827%2C', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('__cfduid', 'dbb29e4531c2b93a1408051183c9033081606748612', domain='.darkmoney.la', path = '/')
        # self.cookiesArray.set('bbforum_view', '667d5c3de15eacc6399eb8f01189987a1f59c9c1a-2-%7Bi-109_i-1606745222_i-346_i-1606745699_%7D', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bblastactivity', '0', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bblastvisit', '1606748401', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bbsessionhash', 'cf75daee9f124a774b78d9ac78c470ea', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bbpassword', '0e0df0a7c88bb46cbcfa15a92f9dffc9', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bbuserid', '232827', domain = 'darkmoney.la', path = '/')
        self.cookiesArray.set('vbseo_loggedin', 'yes', domain = 'darkmoney.la', path = '/')
        self.session.cookies = self.cookiesArray
        


    def parseBoards(self, boardLinksFile):
        boards = []
        mainPage = self.session.get(self.mainPageUrl, headers = self.headers)
        MainPageSoup = BeautifulSoup(mainPage.text, features='lxml')
        BlocksWithBoardLinks = MainPageSoup.find_all("tbody")
        for block in BlocksWithBoardLinks:
            try:
                blockId = block['id']
            except Exception:
                continue
            if 'collapseobj_forumbit' in blockId:
                divsWithBoardLinks = block.find_all('tr')
                for tr in divsWithBoardLinks:
                    td = tr.find('td', {'class' : 'alt1Active'})
                    if td is None:
                        continue
                    link = tr.find('a')
                    if link is not None:
                        boards.append(link['href'])
        with open(boardLinksFile, 'w', encoding='utf-8') as file:
            file.write(json.dumps(boards))

    def ThreadParse(self, boardLinksFile, threadLinksFile, BoardIdStart):
        with open(boardLinksFile, 'r', encoding='utf-8') as file:
            boardUrls = json.loads(file.read())
        with open(threadLinksFile, 'a', encoding='utf-8') as file:
            for i in range(BoardIdStart, len(boardUrls)):
                threadLinks = []
                boardUrl = boardUrls[i]
                while True:
                    print("PARSING BOARD #{} from {}, link = {}".format(i, len(boardUrls), boardUrl))
                    boardPage = self.session.get(self.mainPageUrl + boardUrl, headers = self.headers)
                    boardPageSoup = BeautifulSoup(boardPage.text, features='lxml')
                    tds = boardPageSoup.find_all('td')
                    for tdTag in tds:
                        try:
                            tdId = tdTag['id']
                        except Exception:
                            continue
                        if 'td_threadtitle' in tdId:
                            linkObject = tdTag.find('a')
                            if linkObject is not None:
                                # print(linkObject)
                                threadLinks.append(linkObject['href'])
                    next_page_button = boardPageSoup.find('a', {'rel' : 'next'})
                    if next_page_button is not None:
                        boardUrl = next_page_button['href']
                    else:
                        break
                print(threadLinks != [])
                file.write(json.dumps(threadLinks))
                file.write('\n')
                time.sleep(0.5)
            time.sleep(2)

    def formSingleList(self, threadLinksFile, newThreadLinksFile):
        threads = []
        with open(threadLinksFile, 'r', encoding='utf-8') as file:
            threadList = file.read().split('\n')
        
        boardcounter = 1
        for board in threadList:
            print(boardcounter)
            try:
                board = json.loads(board)
            except Exception:
                continue
            for thread in board:
                if thread not in threads:
                    threads.append(thread)
            boardcounter += 1
        print(len(threads))
        with open(newThreadLinksFile, 'w', encoding='utf-8') as file:
            file.write(json.dumps(threads))        





if __name__ == '__main__':
    parser = DMParser()
    parser.autorize()
    # parser.parseBoards('board_links.json')
    # parser.ThreadParse('board_links.json', 'thread_links.json', 118)
    # parser.formSingleList('thread_links.json', 'single_threads_links.json')