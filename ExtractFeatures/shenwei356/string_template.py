#!/usr/bin/env python3
from string import Template
import datetime

info_tpl = Template('''
Author : $author
Contact: $contact
Date   : $date
''')

info = {'author': "Wei Shen", 'contact': "shenwei356@gmail.com", 'date': datetime.date.today()}

print(info_tpl.substitute(info))