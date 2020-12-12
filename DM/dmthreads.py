import requests
from bs4 import BeautifulSoup
import json
import time
from threading import Thread
import os

class ParsingThread(Thread):

    def __init__(self, number):
        Thread.__init__(self)
        self.number = number
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        self.session = requests.session()
        self.cookiesArray = requests.cookies.RequestsCookieJar()
        self.cookiesArray.set('IDstack', '%2C232827%2C', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('__cfduid', 'dbb29e4531c2b93a1408051183c9033081606748612', domain='.darkmoney.la', path = '/')
        # self.cookiesArray.set('bbforum_view', '667d5c3de15eacc6399eb8f01189987a1f59c9c1a-2-%7Bi-109_i-1606745222_i-346_i-1606745699_%7D', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bblastactivity', '0', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bblastvisit', '1606748401', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bbsessionhash', 'ae8ba8a781933c94eff7971bd68e86d1', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bbpassword', '0e0df0a7c88bb46cbcfa15a92f9dffc9', domain='darkmoney.la', path = '/')
        self.cookiesArray.set('bbuserid', '232827', domain = 'darkmoney.la', path = '/')
        self.cookiesArray.set('vbseo_loggedin', 'yes', domain = 'darkmoney.la', path = '/')
        self.session.cookies = self.cookiesArray

        """
        with open('TelegramLinks_0', 'r', encoding='utf-8') as file:
            self.tags_set = set()
            array = file.read().split('\n')
            for value in array:
                self.tags_set.add(value.split('\t')[0])
        
        print("andregood" in BeautifulSoup(self.session.get(forumUrl, headers = self.headers).text, features = 'lxml').strings, "STARTED")
        """
        self.link_prefix = 'http://t.me/'
        self.tags_set = set()
        self.keywords = [
            'Telegram', 'telegram', 'TELEGRAM', 'tg', 'TG', 'telega', 't.me/', '@', 'телега',
            'телег',
            'Телег', 'телеграм', 'Телеграм'
        ]

    def run(self):
        threads_quantity = 70000
        global info_string
        for thread_index in range(20792, threads_quantity):
            with open('TelegramLinks_{}'.format(self.number), 'a', encoding='utf-8') as file:
                if thread_index == 4: continue;
                try:
                    threadUrl = forumUrl + threads[thread_index]
                    old_thread_url = ''
                    if True:
                        info_string = "Thread {} parsing {} / {} ({}%). \t Contacts: {} \t Url {}".format(self.number, 
                                                                                                            thread_index,
                                                                                                            threads_quantity, 
                                                                                                            int((thread_index) / (threads_quantity * 100)),
                                                                                                            len(self.tags_set),
                                                                                                            threadUrl)
                        if threadUrl == old_thread_url:
                            time.sleep(5)
                            break
                        old_thread_url = threadUrl
                        threadSoup = BeautifulSoup(self.session.get(threadUrl, headers = self.headers).text, features = 'lxml')
                        for string in threadSoup.strings:
                            tags = self.ParseStringForContact(string)
                            for tag in tags:
                                if tag not in self.tags_set:
                                    self.tags_set.add(tag)
                                    file.write(tag + '\t\t\t' + threadUrl)
                                    file.write('\n')
                        for linkObject in threadSoup.find_all('a'):
                            try:
                                tag = self.ParseHrefForContact(linkObject['href'])
                                if tag != '':
                                    tag = tag.replace('https://', 'http://')
                                    if tag not in self.tags_set:
                                        self.tags_set.add(tag)
                                        file.write(tag + '\t\t\t' + threadUrl)
                                        file.write('\n')
                            except Exception as e:
                                # print(e)
                                continue
                        try:
                            nextPageButton = threadSoup.find('a', {'rel': "next"})
                            if threadUrl == forumUrl + nextPageButton['href']:
                                continue
                            threadUrl = forumUrl + nextPageButton['href']
                        except Exception as e:
                            # print(e)
                            continue
                except Exception as e:
                    print(e)
                    time.sleep(5)
                    continue

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
                if letter in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM' or letter == '_' or letter == '.':
                    string_tag += letter
            if string_tag != '': filtered_array.append('http://t.me/' + string_tag)
        return filtered_array

    def ParseHrefForContact(self, href):
        if 't.me' in href:
            return href
        else:
            return ''

    def valid(self):
        tags = {}
        with open("TelegramLinks_0", 'r', encoding='utf-8') as file:
            data = file.read().split('\n')[9705:]
            for dataRow in data:
                try:
                    dataRowList = dataRow.split("\t")
                    tagLink = dataRowList[0]
                    threadLink = dataRowList[-1]
                    if tagLink[-1] in '.,_;:':
                        tagLink = tagLink[:-1]
                    tags[tagLink] = threadLink
                except Exception:
                    print("Exception on split", dataRow)
                    continue
        currentTag = 1; lastTag = len(tags)
        verified = 0; deleted = 0; broken = 0
        usedTags = []
        with open('verified', 'r', encoding='utf-8') as file:
            for data in file.read().split("\n\n"):
                try:
                    usedTags.append(data.split('\n')[0].split("\t")[1])
                except Exception:
                    continue
        with open('broken', 'r', encoding='utf-8') as file:
            for data in file.read().split('\n'):
                usedTags.append(data.split('\t\t')[0])
        print(len(usedTags))
        # print(usedTags)
        for tag in tags:
            if tag in usedTags:
                continue;
            try:
                tgSoup = BeautifulSoup(requests.get(tag, headers = self.headers).text, features='lxml')
                if tgSoup is None:
                    continue;
            except Exception as e:
                print(e)
                continue
            if tgSoup.title.string == "Telegram Messenger":
                with open("broken", 'a', encoding='utf-8') as file:
                    file.write("{}\t\t{}\n".format(tag, tags[tag]))
                    broken += 1
            else:
                if tgSoup.find_all("div", {'class': 'tgme_page_title'}) != []:
                    with open("verified", 'a', encoding='utf-8') as file:
                        file.write('{}\t{}\n{}\n\n'.format("APPLIED", tag, tags[tag]))
                        verified += 1
                else:
                    for string in tgSoup.strings:
                        if ", you can contact " in string:
                            with open("verified", 'a', encoding='utf-8') as file:
                                file.write('{}\t{}\n{}\n\n'.format("DELETED OR NOT CREATED", tag, tags[tag]))
                                deleted += 1
                            break
                    else:
                        with open("broken", 'a', encoding='utf-8') as file:
                            file.write("{}\t\t{}\n".format(tag, tags[tag]))
                            broken += 1

            print("{}/{} | {}%\t\t{}|{}|{}\t\t{}".format(currentTag, lastTag, int(currentTag / lastTag * 100), verified, deleted, broken, tag))
            currentTag += 1
            time.sleep(0.2)

    
    def count(self):
        apl = 0; deleted = 0
        with open('verified', 'r', encoding='utf-8') as file:
            text = file.read()
            apl = text.count("APPLIED")
            deleted = text.count("DELETED OR NOT CREATED")
            print(apl, deleted, apl + deleted)



class PrintingThread(Thread):

    def __init__(self):
        Thread.__init__(self, daemon=True)

    def run(self):
        while True:
            os.system('cls')
            print(info_string)
            time.sleep(1)



a = ParsingThread(0)
# a.valid()
a.count()