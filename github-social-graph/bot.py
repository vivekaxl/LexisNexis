
import argparse, os, time
import urlparse, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def getPeopleLinks(page):
    links = []
    for link in page.find_all('a', 'title'):
        url = link.get('href')
        if url:
            if 'profile/view?id=' in url:
                links.append(url)
    return links

def getJobLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if '/jobs' in url:
                links.append(url)
    return links

def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]

def get_projects(page):
    ret_projects = []
    curr = page.find("div", {"class": "editable-item section-item current-position"})
    t_curr = {}
    try:
        t_curr["title"] = str(curr.find("a", {"name": "title"}).text)
    except:
        t_curr["title"] = "?"

    aux_str = ""

    time = curr.find("span", {"class": "experience-date-locale"})
    try:
        t_curr["duration"] = str(time.find("time").text + "Present")
    except:
        t_curr["duration"] = "?"
    try:
        t_curr["place"] = str(curr.find("span", {"class": "locality"}).text)
    except:
        t_curr["place"] = "?"
    ret_projects.append(t_curr)
    for link in page.find_all("div", {"class": "editable-item section-item past-position"}):
        temp = {}
        try:
            temp["title"] = str(link.find("a", {"name": "title"}).text)
        except:
            temp["title"] = "?"
        try:

            time = link.find("span", {"class": "experience-date-locale"})
            aux_str = ""
            for tim in time.find_all("time"):
                aux_str += tim.text
            # print aux_str
            temp["duration"] = aux_str
        except:
            temp["duration"] = "?"
        try:
            temp["place"] = str(link.find("span", {"class": "locality"}).text)
        except:
            temp["place"] = "?"
        ret_projects.append(temp)

    return ret_projects


def get_skills(page):
    # def breakit(str):
    #     for i in xrange(len(str)):
    #         if str[i].isdigit():
    #             pass
    #         else:
    #             return [str[:i], str[i:]]

    skills = []
    for link in page.find_all('a', {'class': 'endorse-item-name-text'}):
        skills.append(link.text)
    return skills

def get_education(page):
    # for link in page.find_all("a", {'title': 'More details for this school'}):
    #     print link.text
    #     print link
    # for link in page.find_all("span", {'class': 'major'}):
    #     print link.text
    return_list = []
    background_education = page.find("div", {"id":"background-education"})
    for school in background_education.find_all("div",{"class":"editable-item section-item"}):
        temp = {}
        # print dir(school.find("a", {"title": "More details for this school"}))
        try:
            print "School: ", school.find("h4", {"class": "summary fn org"}).text
            temp["School"] = school.find("h4", {"class": "summary fn org"}).text
        except:
            temp["School"] = "?"
        try:
            print "Course: ", school.find("span", {"class": "degree"}).text
            temp['Course'] = school.find("span", {"class": "degree"}).text
        except:
            temp['Course'] ="?"
        try:
            print "Specialization: ", school.find("span", {"class": "major"}).text
            temp['Specialization'] = school.find("span", {"class": "major"}).text
        except:
            temp['Specialization'] = "?"
        try:
            print "Duration: ",
            tmp = ""
            for t in date.find_all("time"):
                print t.text,
                tmp += t.text
            temp['Duration'] = tmp
            print
        except:
            temp['Duration'] = "?"
        return_list.append(temp)

    return return_list

def search_people(browser, str):

    time.sleep(random.uniform(1,2.9))
    browser.get('https://www.linkedin.com/?trk=nav_logo')

    # driver.findElement(By.xpath("//*[@id='main-search-box']")).sendKeys("amdocs");
    # email_element = browser.find_element_by_class("search-box-container")
    element = browser.find_element_by_xpath(".//input[@name='keywords']")
    element.send_keys(str)
    element.submit()
    time.sleep(random.uniform(3.5,6.9))

    #time.sleep(random.uniform(3.5,6.9))

    page = BeautifulSoup(browser.page_source)
    people = getPeopleLinks(page)
    print "Number of returned profiles: ", len(people)
    if len(people) != 1:
        print "Confusion"
        return -1
    else:
        return_dict = {}
        browser.get(people[-1])
        time.sleep(random.uniform(0.9, 1.8))
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(0.9, 1.8))

        f = open("temp.txt", "w")
        f.write(browser.page_source.encode("utf-8", "ignore"))
        f.close()

        page = BeautifulSoup(browser.page_source)
        return_dict["jobs"] = get_projects(page)
        return_dict["education"] = get_education(page)
        return_dict['skills'] = ", ".join(get_skills(page))

    return return_dict



def ViewBot(browser):
    visited = {}
    pList = []
    count = 0
    while True:
        #sleep to make sure everything loads, add random to make us look human.
        time.sleep(random.uniform(3.5,6.9))
        page = BeautifulSoup(browser.page_source)
        people = getPeopleLinks(page)
        if people:
            for person in people:
                ID = getID(person)
                if ID not in visited:
                    pList.append(person)
                    visited[ID] = 1
        if pList: #if there is people to look at look at them
            person = pList.pop()
            browser.get(person)
            count += 1
        else: #otherwise find people via the job pages
            jobs = getJobLinks(page)
            if jobs:
                job = random.choice(jobs)
                root = 'http://www.linkedin.com'
                roots = 'https://www.linkedin.com'
                if root not in job or roots not in job:
                    job = 'https://www.linkedin.com'+job
                browser.get(job)
            else:
                print "I'm Lost Exiting"
                break

        #Output (Make option for this)
        print "[+] "+browser.title+" Visited! \n(" \
              +str(count)+"/"+str(len(pList))+") Visited/Queue)"


def get_browser():
    email = "vivekaxl@gmail.com"
    passwd = "Iamafool09"
    browser = webdriver.Firefox()
    browser.get("https://linkedin.com/uas/login")


    emailElement = browser.find_element_by_id("session_key-login")
    emailElement.send_keys(email)
    passElement = browser.find_element_by_id("session_password-login")
    passElement.send_keys(passwd)
    passElement.submit()

    return browser






if __name__ == '__main__':
    Main()