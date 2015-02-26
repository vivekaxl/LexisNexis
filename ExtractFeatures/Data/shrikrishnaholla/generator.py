#!/usr/bin/python
"""This module is used to generate structured profiles by picking out random elements from predefined lists and stitching 
together values for various fields in a typical LinkedIn profile"""

from random import randint as ri
mail = ['gmail', 'yahoo', 'outlook']
place = ['Bangalore', 'Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Pune']
field = ['Software', 'Computer Science', 'Information Technology', 'Computers', 'Software Engineering']
position = ['Director', 'Section Head', 'Project Head', 'Team Leader', 'Software Engineer']
company = ['Microsoft', 'Google', 'Adobe', 'Infosys', 'Wipro', 'SAP', 'Mindtree', 'Cisco', 'Thoughtworks', 'IBM', 'McAfee', \
'Mozilla', 'Canonical', 'Novell', 'HP', 'Lenovo', 'Asus', 'Dell', 'Toshiba']
degree = ['BE', 'BTech', 'MS', 'MTech', 'PhD']
college = ['IIT', 'IISc', 'NIT', 'PESIT']
skillset = ['Python', 'C', 'C++', 'Java', 'Ruby', 'Scala', 'Erlang', 'PHP', 'HTML5', 'CSS3', 'MySQL', 'MongoDB',\
'cloud computing']

words = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Nam cursus. Morbi ut mi. Nullam enim leo, egestas id, condimentum at, laoreet mattis, massa. Sed eleifend nonummy diam. Praesent mauris ante, elementum et, bibendum at, posuere sit amet, nibh. Duis tincidunt lectus quis dui viverra vestibulum. Suspendisse vulputate aliquam dui. Nulla elementum dui ut augue. Aliquam vehicula mi at mauris. Maecenas placerat, nisl at consequat rhoncus, sem nunc gravida justo, quis eleifend arcu velit quis lacus. Morbi magna magna, tincidunt a, mattis non, imperdiet vitae, tellus. Sed odio est, auctor ac, sollicitudin in, consequat vitae, orci. Fusce id felis. Vivamus sollicitudin metus eget eros.
Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In posuere felis nec tortor. Pellentesque faucibus. Ut accumsan ultricies elit. Maecenas at justo id velit placerat molestie. Donec dictum lectus non odio. Cras a ante vitae enim iaculis aliquam. Mauris nunc quam, venenatis nec, euismod sit amet, egestas placerat, est. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Cras id elit. Integer quis urna. Ut ante enim, dapibus malesuada, fringilla eu, condimentum quis, tellus. Aenean porttitor eros vel dolor. Donec convallis pede venenatis nibh. Duis quam. Nam eget lacus. Aliquam erat volutpat. Quisque dignissim congue leo.
Mauris vel lacus vitae felis vestibulum volutpat. Etiam est nunc, venenatis in, tristique eu, imperdiet ac, nisl. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In iaculis facilisis massa. Etiam eu urna. Sed porta. Suspendisse quam leo, molestie sed, luctus quis, feugiat in, pede. Fusce tellus. Sed metus augue, convallis et, vehicula ut, pulvinar eu, ante. Integer orci tellus, tristique vitae, consequat nec, porta vel, lectus. Nulla sit amet diam. Duis non nunc. Nulla rhoncus dictum metus. Curabitur tristique mi condimentum orci. Phasellus pellentesque aliquam enim. Proin dui lectus, cursus eu, mattis laoreet, viverra sit amet, quam. Curabitur vel dolor ultrices ipsum dictum tristique. Praesent vitae lacus. Ut velit enim, vestibulum non, fermentum nec, hendrerit quis, leo. Pellentesque rutrum malesuada neque.
Nunc tempus felis vitae urna. Vivamus porttitor, neque at volutpat rutrum, purus nisi eleifend libero, a tempus libero lectus feugiat felis. Morbi diam mauris, viverra in, gravida eu, mattis in, ante. Morbi eget arcu. Morbi porta, libero id ullamcorper nonummy, nibh ligula pulvinar metus, eget consectetuer augue nisi quis lacus. Ut ac mi quis lacus mollis aliquam. Curabitur iaculis tempus eros. Curabitur vel mi sit amet magna malesuada ultrices. Ut nisi erat, fermentum vel, congue id, euismod in, elit. Fusce ultricies, orci ac feugiat suscipit, leo massa sodales velit, et scelerisque mi tortor at ipsum. Proin orci odio, commodo ac, gravida non, tristique vel, tellus. Pellentesque nibh libero, ultricies eu, sagittis non, mollis sed, justo. Praesent metus ipsum, pulvinar pulvinar, porta id, fringilla at, est.
Phasellus felis dolor, scelerisque a, tempus eget, lobortis id, libero. Donec scelerisque leo ac risus. Praesent sit amet est. In dictum, dolor eu dictum porttitor, enim felis viverra mi, eget luctus massa purus quis odio. Etiam nulla massa, pharetra facilisis, volutpat in, imperdiet sit amet, sem. Aliquam nec erat at purus cursus interdum. Vestibulum ligula augue, bibendum accumsan, vestibulum ut, commodo a, mi. Morbi ornare gravida elit. Integer congue, augue et malesuada iaculis, ipsum dui aliquet felis, at cursus magna nisl nec elit. Donec iaculis diam a nisi accumsan viverra. Duis sed tellus et tortor vestibulum gravida. Praesent elementum elit at tellus. Curabitur metus ipsum, luctus eu, malesuada ut, tincidunt sed, diam. Donec quis mi sed magna hendrerit accumsan. Suspendisse risus nibh, ultricies eu, volutpat non, condimentum hendrerit, augue. Etiam eleifend, metus vitae adipiscing semper, mauris ipsum iaculis elit, congue gravida elit mi egestas orci. Curabitur pede.
Maecenas aliquet velit vel turpis. Mauris neque metus, malesuada nec, ultricies sit amet, porttitor mattis, enim. In massa libero, interdum nec, interdum vel, blandit sed, nulla. In ullamcorper, est eget tempor cursus, neque mi consectetuer mi, a ultricies massa est sed nisl. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Proin nulla arcu, nonummy luctus, dictum eget, fermentum et, lorem. Nunc porta convallis pede."""
words = words.replace('.','')
words = words.replace(',','')
words = words.split()

def generate(number):
    """Generate profile data for creating test database"""
    profiles = dict()
    for i in xrange(0,number):
        fname = words[ri(0,len(words)-1)]

        lname = words[ri(0,len(words)-1)]

        uname = fname+'-'+lname+'/'+str(ri(0,999))+'/'+str(ri(0,999))+'/'+str(ri(0,999))+'/' # Typical public profile url
        # Public LinkedIn public profile link template

        email = fname+'.'+lname+'@'+mail[ri(0,len(mail)-1)]+'.com'
        locality = place[ri(0,len(place)-1)]
        industry = field[ri(0,len(field)-1)]
        current = position[ri(0,len(position)-1)] + ' at ' + company[ri(0,len(company)-1)]
        past = []
        for i in xrange(0,ri(0,5)): # Assuming at max 5 previous jobs
            past.append(position[ri(0,len(position)-1)] + ' at ' + company[ri(0,len(company)-1)])
        education = []
        for i in xrange(1,ri(1,3)): # Assuming at max 3 degrees
            education.append(degree[ri(0,len(degree)-1)] + ' at ' + college[ri(0,len(college)-1)])
        skills = []
        for i in xrange(0,ri(1,len(skillset)-1)):
            skills.append(skillset[ri(0,len(skillset)-1)])

        projectdescriptions = []
        for i in xrange(0,ri(0,3)):  # Assuming at max 3 major projects mentioned in the LinkedIn profile
            desc = ''
            for j in xrange(0,ri(20,100)):  # Assuming 20 -100 words in a project
                choice = ri(0,100)
                if choice % 10 == 0 and len(skills) >= 1:        # Approximately 10 out of 100 times, mention a skillset (To ease query testing)
                    desc += skills[ri(0,len(skills)-1)]+' '
                elif choice % 51 == 0 and len(past) >= 1:      # Approximately 20 in 100 times, mention the company the project was done in
                    desc += 'when I was working as ' + past[ri(0,len(past)-1)]+' '
                else: # filler words
                    desc += words[ri(0,len(words)-1)]+' '
            projectdescriptions.append(desc)

        profile = dict()
        details = dict()
        profile[uname] = details
        details['fname'] = fname
        details['lname'] = lname
        details['email'] = email
        details['locality'] = locality
        details['industry'] = industry
        details['current'] = current
        details['past'] = past
        details['education'] = education
        details['skills'] = skills
        details['project-descriptions'] = projectdescriptions
        details['experience'] = ri(0,20)

        profiles.update(profile)

    return profiles