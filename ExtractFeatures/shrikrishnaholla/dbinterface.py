#!/usr/bin/python
"""This module acts as an interface between the database and the application"""
import profilefetcher
from pymongo import MongoClient
client = MongoClient()
db = client.linkedIngine_db_7       # Create/connect to a database with the name 'linkedIngine_db'
collection = db.linkedIngine_col_7  # Create/connect to a collection with the name 'linkedIngine_col'

def queryer(params, flag=True):
    """This method returns a list of all the profiles in the database that satisfy the parameters"""
    resultlist = list()
    for param, value in params.items():
        if type(value) == list:
            flag = False
            andlist = [{param: item} for item in value]
            params.pop(param)
            if params.has_key('$and'):
                params['$and'].extend(andlist)
            else:
                params['$and'] = andlist

    resultset = collection.find(params)
    if resultset.count() > 0:
        for person in resultset:
            resultlist.append(person)

    elif len(resultlist) == 0 and flag:
        if profilefetcher.google(params.values()):
            resultlist = queryer(params, False)

    else: # Suppose the parameters are given wrongly, we mustn't NOT return anything. Try best effort approach
        values = params.values()
        for value in values:
            for result in collection.find({'tags':value}): # The keyword sent as parameter may be present as tag
                resultlist.append(result)
    if len(resultlist) == 0: # if it's still empty, it means the user has given junk/unhelpful parameters
        resultlist = [{'error':'No result found. Please give another query or refine your parameters'}]

    return resultlist

if __name__ == '__main__':
    resultset = collection.find({'$and': [{'skills':'c'}, {'skills':'c++'}]})
    for result in resultset:
        print result['skills']