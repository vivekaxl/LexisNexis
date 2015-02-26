#!/usr/bin/python
import dbinterface
import re
import skillindexer

bestenggcolleges = open('data/bestcolleges.engg').readlines()
bestbcolleges    = open('data/bestcolleges.b').readlines()

bestenggcolleges.reverse()
bestbcolleges.reverse()

bestenggcolleges = [college.strip('\n') for college in bestenggcolleges]
bestbcolleges = [college.strip('\n') for college in bestbcolleges]

skills = dict()

def readSkillsFromFiles():
    """Read already learnt skills from the files"""
    skills['web']                  = open('data/skills/web', 'r').readlines()
    skills['mobile']               = open('data/skills/mobile', 'r').readlines()
    skills['research']             = open('data/skills/research', 'r').readlines()
    skills['management']           = open('data/skills/management', 'r').readlines()
    skills['networks']             = open('data/skills/networks', 'r').readlines()
    skills['software_engineering'] = open('data/skills/software_engineering', 'r').readlines()
    skills['uncategorized']        = open('data/skills/uncategorized', 'r').readlines()

readSkillsFromFiles()

for skill in skills.keys():
    skills[skill] = [item.strip('\n') for item in skills[skill]]

def computeIndexes():
    """Compute index values on ALL profiles in the database
    [TODO]: Allow computation on a selective portion of the database"""
    for profile in dbinterface.collection.find():
        totalexperience = 0
        totaleducation  = 0
        # The value for experience will just be the decimal value of total number of years worked
        for experience in profile['experience']:
            if type(experience) == dict:
                totalexperience += experience.get('years', 0)
                totalexperience += 0.01 * (experience.get('months', 0) * 8.33) # = 100/12

        # Value for education will be based on the ranking of the college
        # The rankings have been obtained from a website
        # Higher ranking == greater value
        for college in profile['colleges']:
            for bestenggcollege in bestenggcolleges:
                if re.search(college, bestenggcollege):
                    totaleducation += bestenggcolleges.index(bestenggcollege)+1
            for bestbcollege in bestbcolleges:
                if re.search(college, bestbcollege):
                    totaleducation += bestbcolleges.index(bestbcollege)+1

        # Compute skill indexes
        skillindex = skillindexer.computeSkillIndexes(profile, skills)
        for skill in skills.keys():
            if skill not in skillindex.keys():
                skillindex[skill] = 0
        readSkillsFromFiles()
        dbinterface.collection.update({'public_profile_url':profile['public_profile_url']},
                                        {'$set': {
                                                    'experienceindex': totalexperience,
                                                    'educationindex' : totaleducation,
                                                    'management'     : skillindex.get('management',0),
                                                    'mobile'         : skillindex.get('mobile',0),
                                                    'networks'       : skillindex.get('networks',0),
                                                    'research'       : skillindex.get('research',0),
                                        'software_engineering' : skillindex.get('software_engineering',0),
                                                    'testing'        : skillindex.get('testing',0),
                                                    'web'            : skillindex.get('web',0)
                                                  }})

if __name__ == '__main__':
    indexer()