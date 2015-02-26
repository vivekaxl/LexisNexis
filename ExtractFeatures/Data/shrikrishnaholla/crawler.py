#!/usr/bin/python
"""This module is used to crawl through and scrape useful information from a LinkedIn profile web page"""
import re
import dbinterface

def contentExtractor(page, public_profile_url):
    """Extract contents from LinkedIn profile page and add them to the database if not present"""
    tags = list()
    first_name = fieldExtractor(page, '<span class="given-name">', "</span>")

    last_name = fieldExtractor(page, '<span class="family-name">', "</span>")

    headline = fieldExtractor(page, '<p class="headline-title title" style="display:block">', "</p>")

    locality = fieldExtractor(page, '<span class="locality">', "</span>")
    tags.append(locality)

    industry = fieldExtractor(page, '<dd class="industry">','</dd>')
    tags.append(industry)

    degrees = multipleInstanceExtractor(page, '<span class="degree">', '</span>')
    for degree in degrees:
        tags.append(degree)

    majors = multipleInstanceExtractor(page, '<span class="major">', '</span>')
    for major in majors:
        tags.append(major)

    colleges = multipleInstanceExtractor(page, '<h3 class="summary fn org">', '</h3>')
    for college in colleges:
        tags.append(college)

    skills = multipleInstanceExtractor(page, 'class="jellybean">', '</a>')
    for skill in skills:
        tags.append(skill)

    job_titles = multipleInstanceExtractor(page, '<span class="title">', '</span>')
    for job in job_titles:
        tags.append(job)

    companies = multipleInstanceExtractor(page, '<span class="org summary">', '</span>')
    for company in companies:
        tags.append(company)

    profile = {
        'first_name'         : first_name,
        'last_name'          : last_name,
        'headline'           : headline,
        'locality'           : locality,
        'industry'           : industry,
        'degrees'            : degrees,
        'majors'             : majors,
        'colleges'           : colleges,
        'skills'             : skills,
        'job_titles'         : job_titles,
        'companies'          : companies,
        'tags'               : tags,              # Tags are used to provide best-effort results to queries
        #'public_profile_url' : public_profile_url
    }

    if dbinterface.collection.find(profile).count() == 0:
        dbinterface.collection.save(profile)

def fieldExtractor(page, startTag, endTag):
    """Extract entries whose nature is of the form 'Field:Value'"""
    splitstring = re.split(startTag, page)
    if len(splitstring) > 1:
        splitstring = splitstring[1]
        content = splitstring[:splitstring.index(endTag)]
        return content.strip().replace('&amp;','&').lower()
    else:
        return None

def multipleInstanceExtractor(page, startTag, endTag):
    """Extract entries that can have more than one values. Returned as a list of instances of occurance"""
    instances = re.findall(startTag+r'(?:[a-zA-Z0-9\.-]|[ \n]|[,&;\(\)])*'+endTag, page, re.MULTILINE)
    for instance in instances:
        newinstance = instance.replace(startTag,'').replace(endTag,'').replace('&amp;','&')
        newinstance = newinstance.strip().lower()
        instances[instances.index(instance)] = newinstance
    return instances

if __name__ == '__main__':
    count = 0
    for person in dbinterface.collection.find({'headline': 'python', 'degrees': 'b.e', 'first_name': 'navaneeth', 'companies': 'sap'}):
        print person
        count+=1
    print count
