#-------------------------------------------------------------------------------
# Name:        Song Chotu
# Purpose:     To download songs from internet
#
# Author:      Abhishek Chakravarty (abhi072592@gmail.com)
#
# Created:     03-01-2015
# Copyright:   None
# Licence:     Use Any
#-------------------------------------------------------------------------------

import sys
import requests
from bs4 import BeautifulSoup
import os

def get_movie(url):
    movie_search_page = requests.get(url, allow_redirects= True)
    if movie_search_page.status_code == 200:
        movie_search_soup = BeautifulSoup(movie_search_page.text)
        movie_p_tags = movie_search_soup.findAll(class_="dj")
        for num, movie_names in enumerate(movie_p_tags):
            if movie_names.a.text != 'Home':
                print str(num+1)+'. '+movie_names.a.text
        movie_index = int(raw_input("Enter movie number: "))
        return movie_p_tags[movie_index-1].a['href']
    else:
        return 'failed to connect'


def get_song(movie_link):
    song_search_page = requests.get(movie_link)
    song_search_soup = BeautifulSoup(song_search_page.text)
    song_p_tags = song_search_soup.findAll(class_="dj")
    for num, song_names in enumerate(song_p_tags):
        if song_names.a.text == '48Kbps':
            break
        else:
            print str(num+1)+'. '+song_names.a.text
    song_index = int(raw_input("Enter song number: "))
    return song_p_tags[song_index-1].a.text, song_p_tags[song_index-1].a['href']



def main():
    print '='*30
    print 'Song Downloader'
    print '='*30
    base_url = 'http://m.djraag.net/m/page/allmusic'
    movie = raw_input("Please enter the movie name: ")
    if not movie:
        print 'No movie name. exiting...'
        sys.exit(1)
    else:
        url = base_url+'/search1.php?search='+movie+'&type=album'
        movie_link = get_movie(url)
        if movie_link == 'failed to connect':
            print 'failed to connect'
            sys.exit(1)
        else:
            movie_link = base_url+movie_link[1:]
            song_name, song_url = get_song(movie_link)
            song_url = base_url+song_url[1:]
            print 'downloading...'
            page = requests.get(song_url)
            soup = BeautifulSoup(page.text)
            link = soup.findAll('a',href=True)
            song_url = link[1]['href']
            data = requests.get(song_url).content

            os.chdir('songs')
            filename = song_name+".mp3"

            with open(filename, 'wb') as f:
                    f.write(data)
            print 'download complete'
            print 'saved in '+os.getcwd()+' as '+filename


if __name__ == '__main__':
    main()
