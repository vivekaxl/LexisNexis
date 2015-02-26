import scraper
import categorizer

def computeSkillIndexes(profile, skills):
    """Compute skill index values"""
    skillindex = dict()
    for item in profile['skills']:
        skillFlag = False
        for category, topics in skills.items():
            if item in topics: # If the skill is already present in one of our lists
                skillindex[category] = skillindex.get(category, 0) + 100.0/len(profile['skills'])
                skillFlag = True
        if not skillFlag:
            # if not, get related skills from the relevant linkedin page
            category1,category2,category3,category4 = categorizer.categorize(item)
            catset = set([category1, category2, category3,category4])
            for cat in catset:
                skills[cat].append(item)
                skillindex[cat] = skillindex.get(cat, 0) + 100.0/len(profile['skills'])
                #writeback(cat, item)
            #relatedskills = scraper.extractRelatedSkills(item)
            #for relskill in relatedskills:
            #    for category, topics in skills.items():
            #        if relskill in topics:
            #            skillFlag = False
            #    else:
            #        # if none of the related skills are present in any of the lists,
            #        # go the extra mile and make a wild guess on which category it might belong to
            #       if not skillFlag:
            #            category1,category2,category3,category4 = categorizer.categorize(relskill)
            #            catset = set([category1, category2, category3,category4])
            #            print relskill, ':', catset
            #            for cat in catset:
            #                skills[cat].append(relskill)
            #                #writeback(cat, relskill)
    return skillindex

def writeback(category, skill):
    skillfile = open('data/skills/'+category, 'a')
    skillfile.write(skill+'\n')
    skillfile.close()
