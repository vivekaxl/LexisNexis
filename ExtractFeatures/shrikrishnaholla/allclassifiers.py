import nltk

def words(sentence):
    tokenized_words = nltk.word_tokenize(sentence)
    returndict = dict()
    count = 0
    for word in tokenized_words:
        returndict[count] = word.lower()
        count += 1
    return returndict

def firstWord(sentence):
    tokenized_words = nltk.word_tokenize(sentence)
    return {'firstword': tokenized_words[0].lower()}

def midWord(sentence):
    tokenized_words = nltk.word_tokenize(sentence)
    return {'midword': tokenized_words[(0+len(tokenized_words))/2].lower()}

def lastWord(sentence):
    tokenized_words = nltk.word_tokenize(sentence)
    return {'lastword': tokenized_words[-1].lower()}

def getClassifier(skills, classifierMethod):
    skillset = getSkillSet(skills, classifierMethod)
    classifier = nltk.NaiveBayesClassifier.train(skillset)

    return classifier

def getSkillSet(skills, classifierMethod):
    web                  = [(classifierMethod(skill), 'web') for skill in skills['web']]
    mobile               = [(classifierMethod(skill), 'mobile') for skill in skills['mobile']]
    research             = [(classifierMethod(skill), 'research') for skill in skills['research']]
    management           = [(classifierMethod(skill), 'management') for skill in skills['management']]
    networks             = [(classifierMethod(skill), 'networks') for skill in skills['networks']]
    software_engineering = [(classifierMethod(skill), 'software_engineering') for skill in skills['software_engineering']]
    uncategorized        = [(classifierMethod(skill), 'uncategorized') for skill in skills['uncategorized']]

    return web + mobile + research + management + networks + software_engineering + uncategorized