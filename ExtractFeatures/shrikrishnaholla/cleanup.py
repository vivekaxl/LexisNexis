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

for skill in skills.keys():
    skills[skill] = list(set(skills[skill]))

filer = dict()
filer['web']                  = open('data/skills/web','w')
filer['mobile']               = open('data/skills/mobile','w')
filer['research']             = open('data/skills/research','w')
filer['management']           = open('data/skills/management','w')
filer['networks']             = open('data/skills/networks','w')
filer['software_engineering'] = open('data/skills/software_engineering','w')
filer['uncategorized']        = open('data/skills/uncategorized','w')

for category in skills.keys():
    for skill in skills[category]:
        filer[category].write(skill+'\n')

for category in filer.keys():
    filer[category].close()