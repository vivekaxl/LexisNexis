#!/usr/bin/python
"""
To allow for more powerful querying, we have developed a SQL-like syntax for passing queries to the database.
Please follow the rules to get the optimum output.

####The syntax goes something like this:
return <returnvals> from <number> profiles whose [query parameters]

Example: "return email,locality,experience from 10 profiles whose [(email=gmail;or;email=yahoo);and;(locality=bangalore;or;locality=delhi);and;(experience<5;or;experience>10)]"

#####The available attributes are:
fname                => First Name
lname                => Last Name
email                => e-mail id 
locality             => Location 
industry             => field of work 
current              => current job description
past                 => Past jobs
experience           => Job experience (integer)
education            => Academic details
skills               => skillsets
project-descriptions => Description of listed projects

####Available operators:
=,<>                [contains, doesn't contain] for string values
!=,==,<=,>=,<,>     [not equals,equals,less than or equals, greater than or equals, less than, greater than] for integer values

####Special numbers
'*'   => Returns all fields. Ex: "return * from 5 profiles whose [past=adobe]"
'all' => Returns all profiles that satisfy the condition. Ex: "return skills from all profiles whose [experience>15]"

Note: '=' and '<>' operators are liberal; ie, you can search for a valid value with an invalid key and QuerySQL will try to return the best possible results
Ex: "return skills from 10 profiles whose [knowledge=python]"
return email,locality,experience from 10 profiles whose [(email=gmail;or;email=yahoo);and;(locality=bangalore;or;locality=delhi);and;(experience<5;or;experience>10)]
"""
from random import randint
from random import shuffle
from itertools import groupby
from datetime import datetime
import multiprocessing
import gc
def querystring(sqlstmt, all_profiles):
    """Takes a QuerySQL statement and a dictionary database of profiles as an input and returns a list of profiles as output"""
    fpart = sqlstmt[:sqlstmt.index('[')]

    returnvals = fpart[7:fpart.index('from')]
    return_fields = returnvals.split(',')   # To get the query elements
    return_fields = [field.strip() for field in return_fields]
    
    no_of_results = fpart[fpart.index('from')+5:fpart.index('profiles')]
    no_of_results = no_of_results.strip()
    if not no_of_results == 'all':
        no_of_results = int(no_of_results)     # 10

    # (email=gmail;or;email=yahoo);and;(locality=bangalore;or;locality=delhi);and;(experience<5;or;experience>10)
    qs = sqlstmt[sqlstmt.index('[')+1:sqlstmt.index(']')] # The actual query parameters
    resultset = list()
    
    if len(all_profiles.keys())>1000: # Utilize all available processors for fastest response time
        tasks = all_profiles.items()
        factor = (1.0/(multiprocessing.cpu_count()*int(0.01*len(tasks))))*len(tasks) # Each process needs to process just 100 profiles
        start = datetime.now()
        pool = multiprocessing.Pool()  # COOKBOOK: Create a pool of processes
        for worker in xrange(0,multiprocessing.cpu_count()*int(0.01*len(tasks))):
            pool.apply_async(parse,(qs,dict(tasks[int(worker*factor):int((worker+1)*factor)]),), callback=resultset.extend)
            # Asynchronously apply the method parse on a subset of the database. When the method returns with a list of the individual set of results, append it to a main list of results
        pool.close() # To inform that no more jobs need to be done
        pool.join()  # Wait for the children to finish execution
        end = datetime.now()
        print 'Finished querying', len(all_profiles.keys()), 'profiles in',
        print (str((end-start).seconds)+'.'+str((end-start).microseconds)), 'seconds'
        print 'Showing',no_of_results,'of', len(resultset),'matches to query'
    else:
        resultset = parse(qs, all_profiles) # all results

    shuffle(resultset) # Shuffle the results to increase the randomness of selection

    results = list()
    if len(resultset) > no_of_results: # If the number of actual results obtained are greater than number asked randomly select
        for x in xrange(0,no_of_results):
            results.append(resultset.pop(randint(0,len(resultset)-1)))
    else:                              # Otherwise, just show all there is
        for result in resultset:
            results.append(result)

    templist = list()
    if not return_fields[0] == '*':
        for profile in results:
            temprofile = dict()        # Create a temporary result profile where only the fields that are asked for are dumped
            for field in profile:
                if field in return_fields:
                    temprofile[field] = profile[field]
            templist.append(temprofile)
        results = templist

    gc.collect()

    return results

def parse(qstring, profiles):
    qstring = qstring.strip()         # Strip leading and trailing whitespaces
    qstring = qstring.strip(';')      # Strip stray ';' character to the left/right in qstring of recursively called statements
    if qstring[0] == '(' and qstring[-1] == ')' and qstring.find('(',1) == -1:
        qstring = qstring.strip('(')
        qstring = qstring.strip(')')  # removeinstances of "(query)"
    index = qstring.find(';and;')
    if qstring.find(';or;') != -1 and (index == -1 or index > qstring.find(';or;')): 
        index=qstring.find(';or;')    # if 'or' is present and comes before 'and'
    
    if qstring.find('(') > -1 and qstring.find('(') < index:
        ob = qstring.find('(')        # if open braces are present and first one comes before an 'and' or 'or'
        substr = qstring[ob+1:]
        cb=ob+1       # initialize closing braces
        count=0
        for char in substr:
            if char == '(':
                count += 1  # To handle nested braces
            elif char == ')':
                if count == 0:
                    break   # outermost nest
                else:
                    count -= 1
            cb+=1           # To get position of closing brace
        left = qstring[ob:cb+1]
        
        op = qstring[cb+2:]
        if op[:3].lower() == 'and':
            op = 'and'
        elif op[:2].lower() == 'or':
            op = 'or'
        elif op == '':
            cb = ob+1       # Reusing variable cb
            for char in substr:
                if char == '(':
                    break
                cb += 1
            cb -=1
            left= qstring[qstring.find(substr):substr.rfind(';',0,cb-1)+1]
            op = qstring[qstring.find(substr)+substr.rfind(';',0,cb-1)+1:substr.rfind(';',0,cb)+1]
            # Handled (q1;op;(q2))
            # ((q1);op;q2) to be handled
            print 'left:',left, 'op:',op, 'qstring: ', qstring, 'cb: ',substr[cb]

        else:
            print "Wrong operator", op
            print 'left:',left, 'op:',op, 'qstring: ', qstring
            raise ValueError
        right = qstring[qstring.find(';',cb+2)+1:]
        resultset = process(left,op,right,profiles)

    elif index > -1:  # no bracket-business on left side of operator
        left = qstring[:index]
        op = qstring[index+1:qstring.find(';',index+1)] # From left's index, till the first instance of ';' is found
        right = qstring[qstring.find(';', index+2):]    # From the next instance
        resultset = process(left,op,right,profiles)
    if index == -1:
        resultset = evaluate(qstring, profiles)         # Atomic statement. Ex: "locality=bangalore"

    return resultset

def process(left, op, right, profiles):
    """Process the QuerySQL statement. A statement enters this method as left part, a boolean operator and a right part.
    Based on whether the individual left and right parts are atomic or compound, either the substatements might be evaluated
    or they can be sent back to parse() for further processing of compound statements"""
    if left.find('(') != -1:
        resultset = parse(left, profiles) # The left portion is a compound statement
    else:
        resultset = evaluate(left,profiles)
    if right.find('(') == -1 and right.find(';and;') == -1 and right.find(';or;') == -1: # Atomic statement
        if op == 'and':
            resultdict = dict()
            for profile in resultset:
                resultdict[profile['email']] = profile # Dirty hack alert!! The profiles in resultset are stored without their unames, so email is made their primary key
            resultset = evaluate(right, resultdict)    # The results of left operation is the dataset for right operation, since in 'and', both have to be true

        elif op == 'or':
            resultset.extend(evaluate(right, profiles))
    else:
        if op == 'and':
            resultdict = dict()
            for profile in resultset:
                resultdict[profile['email']] = profile # Dirty hack alert!!
            resultset = parse(right, resultdict)
        elif op == 'or':
            resultset.extend(parse(right, profiles))

    return [k for k,v in groupby(sorted(resultset))]   # COOKBOOK: Remove duplicates efficiently from a list of unhashable objects

def evaluate(atomic, profiles):
    atomic = atomic.strip()     # Remove stray leading and trailing whitespaces and ';' characters
    atomic = atomic.strip(';')
    resultset = list()
    if atomic.find('<>') != -1:
        key,value = crumbs(atomic, '<>')
        if profiles[profiles.keys()[0]].has_key(key) and type(profiles[profiles.keys()[0]][key]) == str:
            resultset.extend(filterer('<>',value,profiles.values(), key))
        elif profiles[profiles.keys()[0]].has_key(key) and type(profiles[profiles.keys()[0]][key]) == list:
            for profile in profiles:
                flag = True
                # If the value of the key is a list, traverse through the list
                for element in profiles[profile][key]:
                    if element.lower().find(value.lower()) != -1:
                        # If the value associated with the key has the given value mentioned anywhere, take the benefit of doubt and eliminate it from consideration
                        flag = False
                        break
                if flag:
                    resultset.append(profiles[profile])
        elif not profiles[profiles.keys()[0]].has_key(key):
            for profile in profiles:
                flag = True # Assume that the profile doesn't contain the value
                for field in profiles[profile]:
                    if type(profiles[profile][field]) == str and profiles[profile][field].lower().find(value.lower()) != -1:
                        flag = False
                        break
                    elif type(profiles[profile][field]) == list:
                        for element in profiles[profile][field]:
                            if element.lower().find(value.lower()) != -1:
                                flag = False
                                break
                        if not flag:
                            break
                if flag:
                    resultset.append(profiles[profile])

    elif atomic.find('!=') != -1:
        key,value = crumbs(atomic, '!=')
        if profiles[profiles.keys()[0]].has_key(key):
            resultset.extend(filterer('!=',int(value),profiles.values(), key))

    elif atomic.find('<=') != -1:
        key,value = crumbs(atomic, '<=')
        if profiles[profiles.keys()[0]].has_key(key):
            resultset.extend(filterer('<=',int(value),profiles.values(), key))
        
    elif atomic.find('>=') != -1:
        key,value = crumbs(atomic, '>=')
        if profiles[profiles.keys()[0]].has_key(key):
            resultset.extend(filterer('>=',int(value),profiles.values(), key))

    elif atomic.find('==') != -1:
        key,value = crumbs(atomic, '==')
        if profiles[profiles.keys()[0]].has_key(key):
            resultset.extend(filterer('==',int(value),profiles.values(), key))

    elif atomic.find('<') != -1:
        key,value = crumbs(atomic, '<')
        if profiles[profiles.keys()[0]].has_key(key):
            resultset.extend(filterer('<',int(value),profiles.values(), key))

    elif atomic.find('>') != -1:
        key,value = crumbs(atomic, '>')
        if profiles[profiles.keys()[0]].has_key(key):
            resultset.extend(filterer('>',int(value),profiles.values(), key))

    elif atomic.find('=') != -1:
        key,value = crumbs(atomic, '=')
        if profiles[profiles.keys()[0]].has_key(key) and type(profiles[profiles.keys()[0]][key]) != list:
            resultset.extend(filterer('=',value,profiles.values(), key))
        elif profiles[profiles.keys()[0]].has_key(key) and type(profiles[profiles.keys()[0]][key]) == list:
            for profile in profiles:
                for element in profiles[profile][key]:
                    if element.lower().find(value.lower()) != -1:
                        resultset.append(profiles[profile])
                        break
        elif not profiles[profiles.keys()[0]].has_key(key): # Even if the profile doesn't have the key, (The user might have mistyped, or might want a special kind of value like geek=python)
            for profile in profiles: # instead of exiting with no results, try to figure out whether the value he expects is present anywhere at all within the profile.
                flag = False # Assume that the profile doesn't have the value anywhere
                for field in profiles[profile]:
                    if type(profiles[profile][field]) == str and profiles[profile][field].lower().find(value.lower()) != -1:
                        flag = True
                        break
                    elif type(profiles[profile][field]) == list:
                        for element in profiles[profile][field]:
                            if element.lower().find(value.lower()) != -1:
                                flag = True
                                break
                        if flag:
                            break
                if flag:
                    resultset.append(profiles[profile])

    return resultset

def filterer(op,val,profiles,key):
    if(op=='<>'):
        return filter(lambda x: x[key].lower().find(val.lower())==-1, profiles)
    elif(op=='!='):
        return filter(lambda x: x[key]!=val, profiles)
    elif(op=='<='):
        return filter(lambda x: x[key]<=val, profiles)
    elif(op=='>='):
        return filter(lambda x: x[key]>=val, profiles)
    elif(op=='=='):
        return filter(lambda x: x[key]==val, profiles)
    elif(op=='<'):
        return filter(lambda x: x[key]<val, profiles)
    elif(op=='>'):
        return filter(lambda x: x[key]>val, profiles)
    elif(op=='='):
        return filter(lambda x: x[key].lower().find(val.lower())!=-1,profiles)

def crumbs(stmt,op):
    key = stmt[:stmt.find(op)]
    value = stmt[stmt.find(op)+len(op):]
    return (key.strip(),value.strip())
