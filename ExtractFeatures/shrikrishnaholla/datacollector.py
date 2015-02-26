#!/usr/bin/python
"""This module is used by the testing console to provide different methods to collect profile data"""
import deserializer
import scraper
import generator
import multiprocessing
from datetime import datetime

def collect():
    global resultset
    """Method to collect profile data"""
    
    method = raw_input("""
Enter the method for data collection of your choice:
1: Scrape from public link
2: Enter individual data
3: Generate data
4: Read data from file

""")
    resultset = dict()

    if method == '1':
        scraper.initiate()
        for profile in scraper.links: # TODO: variables musn't be global - functions must return them
            if profile.find('linkedin.com/pub/') > -1:
                profile = profile[(profile.find('linkedin.com/pub/')+17):]
            resultset[profile] = scraper.resumelist[profile]   # TODO: Devise a method to get the profile's mail id
            # take the username and remove the /xxx/yyy/zzz numbers

    elif method == '2':
        uname = raw_input('Enter uname: ')
        details = dict()
        details['fname'] = raw_input('First name: ')
        details['lname'] = raw_input('Last name: ')
        details['email'] = raw_input('email: ')
        details['locality'] = raw_input('Locality: ')
        details['industry'] = raw_input('Industry: ')
        details['current'] = raw_input('Current position: ')
        details['past'] = raw_input('Past positions [separator: "|"]: ').split('|')
        details['experience'] = int(raw_input('Total job experience in years: '))
        details['education'] = raw_input('Education [separator: "|"]: ').split('|')
        details['skills'] = raw_input('Skills [separator: "|"]:').split('|')
        details['project-descriptions'] = raw_input('Project descriptions [separator: "|"]: ').split('|')
        resultset[uname] = details
    
    elif method == '3':
        number = int(raw_input("How many profiles do you want to generate? "))
        # If number < 1000, delay negligible
        if number < 1000:
            resultset.update(generator.generate(number))
        else:
            # Use python multiprocessing capabilities to divide work
            start = datetime.now()
            pool = multiprocessing.Pool()
            factor = number/1000
            for worker in xrange(0,multiprocessing.cpu_count()*factor): # Split the task of generating n numbers to all cpus
                pool.apply_async(generator.generate, (number/(multiprocessing.cpu_count()*factor),), callback=lambda profiles: appender(profiles))
            pool.close()
            pool.join()
            end = datetime.now()
            print 'Finished generating', number, 'profiles in',
            print (str((end-start).seconds)+'.'+str((end-start).microseconds)), 'seconds'
            import gc
            gc.collect()

    elif method == '4':
        resultset = deserializer.deserialize('data/datastore.in')

    return resultset

def appender(profiles):
    global resultset
    resultset.update(profiles)
    del profiles
