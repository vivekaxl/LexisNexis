from  requests import request
from fuzzywuzzy import process
from bs4 import BeautifulSoup as Soup
from re import split as Split
import logging
import requests
#find_music works as an drive program to parse www.tunefind.com to access music list of tv shows by name
#for each object of find_music session gets created to www.tunefind.com.
class find_music():
    names = []
    site_url = "http://www.tunefind.com"
    original_name = ""
    use_name = ""
    episodes_dict = {}
    def __init__(self,name,type):
        self.url = "http://www.tunefind.com/browse/"
        self.s = requests.session()
        self.p = self.s.get(self.site_url)
        self.tname = name.replace(" ","-")
        self.name=name
        self.type = type
        self.__fuzzy_match__()

#get_list method return list of names of all tv shows on www.tunefind.com
    def get_List(self):
        if self.type == "tv":
            url = self.url + self.type
        elif self.type == "movie":
            url = self.url + self.type
        else:
            return []
        req = self.s.get(url)
        soap = Soup(req.text)
        self.names = []
        for body in soap.findAll('div',{"class":"col-md-4"}):
            self.names.append(body.find('a').string.encode('ascii','ignore'))
        return self.names

#fuzzy_match() method is used to get correct name of tv show from specified name at creation of object using fuzzy_search
    def __fuzzy_match__(self):
        temp_names = self.get_List()
        self.original_name =  process.extract(self.name,choices=temp_names,limit=1)[0][0]

#return list of names of seasons for specified tv show_name
    def get_seasons(self):
        self.use_name = self.original_name.replace(' ','-').lower()

        url = "http://www.tunefind.com/show/" + self.use_name
        req = self.s.get(url)
        seasons=[]
        soap = Soup(req.text)
        for body in soap.find_all('div',{"class":"panel panel-default tf-panel"}):
            for names in  body.find_all('a'):
                seasons.append(names.string.encode('ascii','ignore'))

        return seasons

#return dict as dict['episode_name'] : 'link for that episode'
    def __get_episodes_dict(self,season_name):
        season_name = season_name.replace(' ','-').lower()
        url = "http://www.tunefind.com/show/"+self.get_OriginalName().lower().replace(" ","-")+"/" + season_name
        req = self.s.get(url)
        episodes = {}

        soap = Soup(req.text)
        for body in soap.find_all('ul',{'class':"list-group"}):
            for episode_body in body.find_all('li',{'class':'list-group-item'}):
                episodes[episode_body.find('a').string.encode('ascii','ignore').replace('\n','').strip(' ')] = episode_body.find('a').get('href')
        self.episodes_dict = episodes
        return episodes

#driver method to return list episodes in specified season
    def get_episodes(self,season_name):
        return self.__get_episodes_dict(season_name).keys()

#for specified episode name return music of that episode #note season needs to be the same for that instance.
    def getMusicdict(self,season_name,episode_name):
        url = self.site_url + self.episodes_dict[episode_name]
        req = self.s.get(url)
        soap = Soup(req.text)
        episodes = []
        for body in soap.find_all('div',{'class':"media-body"}):
            for k in body.find_all('a',{'class':"tf-popup tf-song-link"}):
                temp  = Split(r'\s{2}',body.getText().encode('ascii','ignore').replace('\n','').lstrip(' '))
                episode_str = ''
                cnt = 0
                for l in temp:
                    if l != '':
                        episode_str = episode_str + " " + l
                        cnt = cnt + 1
                    if cnt > 1:
                        break
                episodes.append(episode_str.lstrip(" "))
        return episodes

#drive method to return correct_name for tv show ----fuzzy_search
    def get_OriginalName(self):
        return self.original_name
'''
# demo driver program
logging.basicConfig(filename="logs.txt",level=logging.DEBUG,filemode="w") #created a logger in debug mode.
obj = find_music(name='howImetyourrrmother',type='tv')
print obj.get_OriginalName()
#How I Met Your Mother

print obj.get_seasons()
#['Season 9', 'Season 8', 'Season 7', 'Season 6', 'Season 5', 'Season 4', 'Season 3', 'Season 2', 'Season 1']

print obj.get_episodes('Season 8')
#["18. Weekend at Barney's", '23. Something Old', '7. The Stamp Tramp', '6. Splitsville', '10. The Over-Correction', '19. The Fortress', '8. Twelve Horny Women', '4. Who Wants to Be a Godparent?', '13. Band or DJ?', '5. The Autumn of Break-Ups', '22. The Bro Mitzvah', '24. Something New', '1. Farhampton', '15. P.S. I Love You', '11. The Final Page (1)', '16. Bad Crazy', '12. The Final Page (2)', '21. Romeward Bound', '17. The Ashtray', '2. The Pre-Nup', '3. Nannies', '14. Ring Up!', '20. The Time Travelers', '9. Lobster Crawl']

print obj.getMusicdict(season_name='Season 3',episode_name='1. Farhampton')
#['The Funeral by Band of Horses', 'Simple Song by The Shins']
'''
