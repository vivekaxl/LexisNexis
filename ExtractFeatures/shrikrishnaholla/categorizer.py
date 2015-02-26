import nltk
import allclassifiers

skills = dict()
skills['web']                  = open('data/skills/web', 'r').readlines()
skills['mobile']               = open('data/skills/mobile', 'r').readlines()
skills['research']             = open('data/skills/research', 'r').readlines()
skills['management']           = open('data/skills/management', 'r').readlines()
skills['networks']             = open('data/skills/networks', 'r').readlines()
skills['software_engineering'] = open('data/skills/software_engineering', 'r').readlines()
skills['uncategorized']        = open('data/skills/uncategorized', 'r').readlines()

for skill in skills.keys():
    skills[skill] = [value.strip('\n') for value in skills[skill]]

classifier1 = allclassifiers.getClassifier(skills, allclassifiers.words)
classifier2 = allclassifiers.getClassifier(skills, allclassifiers.firstWord)
classifier3 = allclassifiers.getClassifier(skills, allclassifiers.midWord)
classifier4 = allclassifiers.getClassifier(skills, allclassifiers.lastWord)

def categorize(uncategorizedskill):
    wordclassification      = classifier1.classify(allclassifiers.words(uncategorizedskill))
    firstWordClassification = classifier2.classify(allclassifiers.firstWord(uncategorizedskill))
    midWordClassification   = classifier3.classify(allclassifiers.midWord(uncategorizedskill))
    lastWordClassification  = classifier4.classify(allclassifiers.lastWord(uncategorizedskill))
    return (wordclassification, firstWordClassification, midWordClassification, lastWordClassification)

if __name__ == '__main__':
    print categorize(raw_input('Enter a skill: '))
    #categorizedskills = dict()
    #for skill in skills['uncategorized']:
    #    category = categorize(skill)
    #    print skill, ':', category
        #categorizedskills[category] = categorizedskills.get(category, []) + [skill]
    #import skillregressor
    #for key, value in categorizedskills.items():
    #    skillregressor.writeback(key, value)

    #for skill1 in skills.keys():
    #    for skill2 in skills.keys():
    #        if skill1 != skill2:
    #            print skill1, '\t',skill2, '\n', '='*100
    #            print [skill for skill in skills[skill1] if skill in skills[skill2]]
