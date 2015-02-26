import urllib
import urllib.request
import http.cookiejar
import urllib.parse
import sys
import re
import base64
import json
import math

print('自动评论')
access_token = '2.00787Z_EVNDCKDafde730d76XfRlOC'

values = {'client_id':'2896650881',
          'client_secret':'7fbe938ff439d3d613fd6740481fa8c3',
          'grant_type':'authorization_code',
          'code':'715e6227e776be8e4fc7966d7fadfa04',
          'redirect_uri':'https://api.weibo.com/oauth2/default.html'}
'''mid->id'''
mymid = 'BrSr7g51Q'
def get_id(mid):
    url_mid = 'https://api.weibo.com/2/statuses/queryid.json'
    values = {'access_token':'2.00787Z_EVNDCKDafde730d76XfRlOC',
            'mid':mid,
              'isBase62':'1',
              'type':'1'}
    data = urllib.parse.urlencode(values)
    data = data.encode('UTF-8')
    url_t = 'https://api.weibo.com/2/statuses/queryid.json?access_token=2.00787Z_EVNDCKDafde730d76XfRlOC&mid=BrSr7g51Q&type=1&isBase62=1'
    url = 'https://api.weibo.com/2/statuses/queryid.json?access_token=2.00787Z_EVNDCKDafde730d76XfRlOC&type=1&isBase62=1&mid=' + mid
    html = urllib.request.urlopen(url)
    id = json.loads(html.read().decode('UTF-8'))
    print (id['id'])
    return id['id']




def reply(cid,id,user):
    values ={'access_token':'2.00787Z_EVNDCKDafde730d76XfRlOC',
             'cid':cid,
             'id':id,
             'comment':'你好！python %s 评论！：）' % user}
    url_reply = 'https://api.weibo.com/2/comments/reply.json'
    data = urllib.parse.urlencode(values)
    data =data.encode('UTF-8')
    url =urllib.request.Request(url_reply,data)
    html = urllib.request.urlopen(url)




'''通过id获取某条微博的所有评论信息'''
def show(id):
    url_show = 'https://api.weibo.com/2/comments/show.json'
    values = {'access_token':'2.00787Z_EVNDCKDafde730d76XfRlOC',
              'id':id}
    data = urllib.parse.urlencode(values)
    data = data.encode('UTF-8')
    url = 'https://api.weibo.com/2/comments/show.json?access_token=2.00787Z_EVNDCKDafde730d76XfRlOC&id=' + id
    html = urllib.request.urlopen(url)
    s = json.loads(html.read().decode('UTF-8'))
    j = s['total_number']
    
    for i in range(0,j-1):
        print(i)
        cid = s['comments'][i]['mid']
        print(cid)
        user = s['comments'][i]['user']['screen_name']
        reply(cid,id,user)



show(get_id(mymid))
