#importing liblraries
import requests
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import pandas as pd
    
#trie class for node
class TrieNode: 
      
     
    def __init__(self): 
        self.children = [None]*26
        self.urls = {}
        
        self.isEndOfWord = False
  
#Trie data structure class
class Trie: 
      
    
    def __init__(self): 
        self.root = self.getNode() 
  
    def getNode(self): 
      
        
        return TrieNode() 
  
    def _charToIndex(self,ch): 
          
          
        return ord(ch)-ord('a') 
  
  
    def insert(self, key, url): 
          
        pCrawl = self.root 
        length = len(key) 
        for level in range(length): 
            index = self._charToIndex(key[level]) 
  
        #if character not found
            if not pCrawl.children[index]: 
                pCrawl.children[index] = self.getNode() 
            pCrawl = pCrawl.children[index] 
  
        # mark last node as leaf 
        if url in pCrawl.urls:
            pCrawl.urls[url] = pCrawl.urls[url] + 1
        else:
            pCrawl.urls[url] = 1
        pCrawl.isEndOfWord = True
  
    def search(self, key): 
          
        # search in trie and return true if found else false
        pCrawl = self.root 
        length = len(key) 
        for level in range(length): 
            index = self._charToIndex(key[level]) 
            if not pCrawl.children[index]: 
                return False
            pCrawl = pCrawl.children[index] 
  
        if pCrawl != None and pCrawl.isEndOfWord:
            return pCrawl.urls
        else:
            return None
  
#main function
 
  
menu = True
while menu:
    print ("""
           1. Extract News
           2. Enter text to search
           3. Output
           4. Exit/Quit
           """)
    menu = input("Enter input: ") 
    if menu == "1": 
        links = ['https://thinktwicenish.wordpress.com/2018/01/21/2017-ended-well/',
         'https://thinktwicenish.wordpress.com/2017/12/24/flashback17-my-wisdom-boost-year/',
         'https://thinktwicenish.wordpress.com/2017/12/17/flashback-travel17/',
         'https://thinktwicenish.wordpress.com/2017/12/09/flashback-dec16/',
         'https://thinktwicenish.wordpress.com/2017/11/18/things-i-learned-from-the-mumbai-local/',
         'https://thinktwicenish.wordpress.com/2017/11/12/things-i-learned-from-people-as-i-traveled/',
         'https://thinktwicenish.wordpress.com/2017/06/19/what-ladakh-taught-me/',
         'https://thinktwicenish.wordpress.com/2017/11/05/things-i-learned-from-the-crazy-old-man/',
         'https://thinktwicenish.wordpress.com/2018/02/18/the-balance-ii/',
         'https://thinktwicenish.wordpress.com/2018/02/11/the-balance-i/']
        stop_words = stopwords.words("english")
        tokenizer = RegexpTokenizer(r'\w+')
        database = []
        for link in links:
            response = requests.get(link, timeout=5)
            content = BeautifulSoup(response.content, "html.parser")
            paragraphs = content.find_all("p")
            words_list = []
            for para in paragraphs:
                words_list = words_list + tokenizer.tokenize(para.text)
    
            filtered_list = [word.lower() for word in words_list if word not in stop_words and re.match(r"^[a-zA-Z]+$", word) != None]
            database.append({'url': link, 'words_list': filtered_list})
    

        t = Trie() 
  

        for data in database:
            for word in data['words_list']:
                t.insert(word, data['url'])
    elif menu == "2":
        search_input = input("Enter word to search: ")
    
    elif menu == "3":
        output = {}
        inputs = search_input.split()
        for word in inputs:
            i = re.sub(r"[^a-zA-Z]", "", word)
            results = t.search(i)
            if results:
                for url in results.keys():
                    if url not in output.keys():
                        output[url] = {}
                    output[url][i] = results[url]
        df = pd.DataFrame.from_dict(output, orient='index')

        df = df.assign(Count_NA = lambda x: x.isnull().sum(axis=1)).sort_values('Count_NA', ascending=True).drop('Count_NA', axis=1).fillna(0)    
        print(df)
    elif menu == "4":
        menu = False
    elif menu != "":
        print("\n Not Valid Choice Try again") 