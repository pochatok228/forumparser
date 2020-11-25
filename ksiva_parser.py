import requests
from bs4 import BeautifulSoup
import json
import time

class KsivaParser:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        self.mainPageBoardLinkTitleClass = 'node-title'
        self.forumUrl : str = "https://3board.ksivi.bz"
        self.MessagesQuantity = 0
        self.session = requests.Session()
        self.keywords = [
            'Telegram', 'telegram', 'TELEGRAM', 'tg', 'TG', 'telega', 't.me/', '@', 'телега',
            'телег',
            'Телег', 'телеграм', 'Телеграм'
        ]
        

    def Autorize(self):
        
        cookiesArray = requests.cookies.RequestsCookieJar()
        cookiesArray.set("userinit", "689eb77d6756950c122274772c7d052c", domain = "3board.ksivi.bz", path="/login")
        cookiesArray.set("xf_csrf", "Q98ZPOpxePVloEqo", domain = "3board.ksivi.bz", path="/")
        cookiesArray.set("xf_logged_in", "1", domain = "3board.ksivi.bz", path="/")
        cookiesArray.set("xf_session", "Sdq9bTpoyV38M1VwRcG1EovMbZnPTiB7", domain = "3board.ksivi.bz", path="/")
        cookiesArray.set("xf_user", "51304%2Cuejo01dh0ZOzC9X46gtLz4bIWOPHezM7phksb5Fc", domain = "3board.ksivi.bz", path="/")
        self.session.cookies = cookiesArray


    def BoardParsing(self, jsonFileToSave : str) -> None:
        boardLinks = {}
        mainPageSoup = BeautifulSoup(requests.get(self.forumUrl, headers = self.headers).text, features="lxml")
        boardHeaders = mainPageSoup.find_all('h3', {'class' : self.mainPageBoardLinkTitleClass})
        for boardHeader in boardHeaders:
            boardName = boardHeader.text
            print(boardName)
            urlLinkToBoard = boardHeader.find("a")['href']
            stringMessagesQuantity = boardHeader.parent.find("div", {'class'  : "node-meta"}).find("div").find_all("dl")[-1].find("dd").text
            if "тыс." in stringMessagesQuantity:
                stringMessagesQuantity = int(float(stringMessagesQuantity.split(' ')[0]) * 1000)
            else:
                stringMessagesQuantity = int(stringMessagesQuantity)
            self.MessagesQuantity += stringMessagesQuantity
            boardUrl = self.forumUrl + urlLinkToBoard
            boardLinks[boardName] = {"url": boardUrl, "messageQuantity": stringMessagesQuantity}
        with open(jsonFileToSave, 'w', encoding='utf-8') as file:
            file.write(json.dumps(boardLinks))


    def ThreadsParsing(self, jsonFileWithBoards : str, jsonFileWithThreads : str) -> None:
        with open(jsonFileWithBoards, 'r', encoding='utf-8') as file:
            boardsDict = json.loads(file.read())

        thread_list = []
        for board_name in boardsDict:
            boardInfo = boardsDict[board_name]
            boardUrl = boardInfo['url']
            print(board_name, boardUrl)
            print()
            print()
            while True:
                responce = self.session.get(boardUrl)
                boardSoup = BeautifulSoup(responce.text, features='lxml')
                print(responce, boardUrl)
                threadTitles = boardSoup.find_all('div', {'class' : 'structItem-title'})
                for threadTitle in threadTitles:
                    linkToThread = threadTitle.find_all('a')[-1]
                    # print(linkToThread.text, linkToThread['href'])
                    thread_list.append(linkToThread['href'])
                nextPageButton = boardSoup.find("a", {"class" : "pageNav-jump pageNav-jump--next"})
                if nextPageButton is not None:
                    boardUrl = self.forumUrl + nextPageButton['href']
                else:
                    time.sleep(5)
                    break
                time.sleep(5)
            time.sleep(30)
            print()
            print()
            print()
            print()
                    

        with open(jsonFileWithThreads, 'w', encoding='utf-8') as file:
            file.write(json.dumps(thread_list))
                    

    def checkAuth(self):
        mainPageSoup = BeautifulSoup(self.session.get(self.forumUrl, headers = self.headers).text, features='lxml')
        for span in mainPageSoup.find_all('span', {'class' : 'p-navgroup-linkText'}):
            print(span.text)


    def printQuantityOfThreads(self, thread_file):
        with open(thread_file, 'r', encoding='utf-8') as file:
            threads = json.loads(file.read())
        print(len(threads))

    def restructThreadLinksFile(self, thread_file, forum_file):
        with open(thread_file, 'r', encoding='utf-8') as file:
            threads = json.loads(file.read())
        subforums = []
        i = 0
        while True:
            try:
                thread = threads[i]
                if 'forums' in thread:
                    subforums.append(threads.pop(i))
                    i-=1 
                i+=1
            except IndexError:
                break
        print(subforums)
    
    def ThreadParseOnSubforums(self, subforum_links, thread_links):
        with open(subforum_links, 'r', encoding='utf-8') as file:
            subforums = file.read().split('\n')
        thread_list = []
        for subforum in subforums:
            subforumResponse = self.session.get(subforum)
            subforumSoup = BeautifulSoup(subforumResponse.text, features='lxml')
            boardTitles = subforumSoup.find_all('h3', {'class' : 'node-title'})
            for boardTitle in boardTitles:
                boardUrl = self.forumUrl + boardTitle.find('a')['href']
                while True:
                    responce = self.session.get(boardUrl)
                    boardSoup = BeautifulSoup(responce.text, features='lxml')
                    print(responce, boardUrl)
                    threadTitles = boardSoup.find_all('div', {'class' : 'structItem-title'})
                    for threadTitle in threadTitles:
                        linkToThread = threadTitle.find_all('a')[-1]
                        # print(linkToThread.text, linkToThread['href'])
                        thread_list.append(linkToThread['href'])
                    nextPageButton = boardSoup.find("a", {"class" : "pageNav-jump pageNav-jump--next"})
                    if nextPageButton is not None:
                        boardUrl = self.forumUrl + nextPageButton['href']
                    else:
                        time.sleep(5)
                        break
                    time.sleep(5)
                time.sleep(30)
        with open(thread_links, 'w', encoding='utf-8') as file:
            file.write(json.dumps(thread_list))

    def mergeAllThreadLinks(self, file1, file2, file_write):
        merged_array = []
        with open(file1, 'r', encoding='utf-8') as file:
            array1 = json.loads(file.read())
        with open(file2, 'r', encoding='utf-8') as file:
            array2 = json.loads(file.read())
        for element in array1: merged_array.append(element)
        for element in array2: merged_array.append(element)
        with open(file_write, 'w', encoding='utf-8') as file:
            file.write(json.dumps(merged_array))
        
    def allThreadsQuantity(self, file_threads):
        with open(file_threads, 'r', encoding='utf-8') as file:
            threads = json.loads(file.read())
        print(len(threads))

    def ParseThread(self, thread_url):
        tagsForReturn = []
        while True:
            threadResponse = self.session.get(thread_url)
            threadSoup = BeautifulSoup(threadResponse.text, features='lxml')
            articles = threadSoup.find_all('div', {'class' : 'message-content js-messageContent'})
            print(len(articles), thread_url)
            for article in articles:
                for string in article.strings:
                    tags_parsed = self.ParseStringForContact(string)
                    # if tags != []: print(*tags)
                    for tag in tags_parsed:
                        if tag not in tagsForReturn:
                            tagsForReturn.append(tag) 
                for link in article.find_all('a'):
                    try:
                        tag = self.ParseHrefForContact(link['href'])
                        # if tag != '': print(tag)
                        if tag not in tagsForReturn and tag != '':
                            tagsForReturn.append(tag)
                    except Exception:
                        pass
            try:
                nextPageButton = threadSoup.find("a", {"class" : "pageNav-jump pageNav-jump--next"})
                thread_url = self.forumUrl + nextPageButton['href']
                time.sleep(0.1)
            except Exception:
                time.sleep(0.1)
                break

        return tagsForReturn

    def ParseStringForContact(self, string):
        array_for_return = []
        words = string.split()
        for i in range(len(words)):
            word = words[i]
            if '@' in word:
                if word[0] == '@':
                    array_for_return.append(word[1 : ])
            else:
                for keyword in self.keywords:
                    if keyword in word:
                        try:
                            array_for_return.append(words[i + 1])
                        except Exception:
                            pass
        filtered_array = []
        for tag in array_for_return:
            string_tag = ''
            for letter in tag:
                if letter.isalpha() or letter.isdigit() or letter == '_' or letter == '.':
                    string_tag += letter
            if string_tag != '': filtered_array.append('http://t.me/' + string_tag)
        return filtered_array
            
            
                     
    def ParseHrefForContact(self, href):
        if 't.me' in href:
            return href
        else:
            return ''

    def ParseThreads(self, file_with_threads, file_with_links, threadNumber):
        with open(file_with_threads, 'r', encoding='utf-8') as file:
            threads = json.loads(file.read())[:threadNumber]
        tags = []
        with open(file_with_links, 'a', encoding='utf-8') as file:
            while True:
                try:
                    print('Парсим тред. Осталось {}. Всего отпарсили {}%'.format(len(threads), int((7926 - len(threads)) / 7926 * 100)))
                    threadToParse = threads.pop()
                    returned_tags = self.ParseThread(self.forumUrl + threadToParse)
                    for returned_tag in returned_tags:
                        if returned_tag not in tags:
                            tags.append(returned_tag)
                            file.write(returned_tag + ";" + self.forumUrl + threadToParse + '\n')
                    print("Количество ссылок на телеграмм: {}".format(len(tags)))
                except Exception as e:
                    print(e)
                    break

    def makeJsonWithTags(self, fileWithLinks, newFileWithLinks):
        with open(fileWithLinks, 'r', encoding='utf-8') as file:
            notes = file.read().split('\n')
        tags = {}
        for note in notes:
            notea = note.split(';')
            print(notea)
            try:
                noteurl = notea[0]
                noteref = notea[1]
                if noteurl not in tags:
                    tags[noteurl] = noteref
            except Exception:
                continue

        print(len(tags))
        with open(newFileWithLinks, 'w', encoding='utf-8') as file:
            file.write(json.dumps(tags))

    def valid(self, fileWithTags, newFileWithTags):
        with open(fileWithTags, 'r', encoding='utf-8') as file:
            tags = json.loads(file.read())
        confirmedTags = {}
        for tag in tags:
            validint = -1
            print(tag)
            response = requests.get(tag)
            responseSoup = BeautifulSoup(response.text, features='lxml')
            valid = responseSoup.find('div', {'class' : "tgme_page_photo"})
            if valid is not None:
                validint = 1
            else:
                valid = responseSoup.find('div', {'class' : 'tgme_page_icon'})
                if valid is not None:
                    validint = 0
                else:
                    validint = -1

            if validint == 1:
                confirmedTags[tag] = [tags[tag], 'APPLIED']
            elif validint == 0:
                confirmedTags[tag] = [tags[tag], 'DELETED OR NOT CREATED']
            print(validint)
            time.sleep(0.25)

        with open(newFileWithTags, 'a', encoding='utf-8'):
            for tag in confirmedTags:
                newFileWithTags.write(tag +  '     ' +  confirmedTags[tag][0] + '      ' + confirmedTags[tag][1]) 

        

                

        






if __name__ == "__main__":
    parser = KsivaParser()
    parser.Autorize() 
    # parser.checkAuth()
    # parser.ThreadsParsing('board_links.json', 'thread_link.json')
    # parser.printQuantityOfThreads('thread_link.json')
    # parser.restructThreadLinksFile('thread_link.json', 'subforums_link.json')
    # parser.ThreadParseOnSubforums('subforum.txt', 'thread_subforum_links.json')
    # parser.mergeAllThreadLinks('thread_link.json', 'thread_subforum_links.json', 'all_threads.json')
    # parser.allThreadsQuantity('all_threads.json')
    # parser.ParseThread('https://3board.ksivi.bz/threads/obraschenie-k-administracii.9274/')
    # parser.ParseThreads('all_threads.json', 'links.txt', 4881)
    # parser.makeJsonWithTags('links.txt', 'links.json')
    parser.valid('links.json', 'valid_links.json')