# coding=utf-8
import json
import time

import requests
import random
from datetime import datetime
headers = {
    'app_version': '9.0.0',
    'platform': 'ios',
    "content-type": "application/json",
    "User-agent": "Tinder/9.0.0 (iPhone; iOS 10.3.2; Scale/2.00)",
}
backup_headers = {
    "User-agent": "Tinder/9.0.0 (iPhone; iOS 10.3.2; Scale/2.00)",
    'app_version': '9.0.0',
    'platform': 'ios',
    "content-type": "application/json",
    
}
apiUrl='http://trafficstandard.com/api/message/tinder'
botId =input('enter your bot id :')
profile_id=input('enter your bot profile id :')

host = 'https://api.gotinder.com'
def tinderLastUpdate(need):
    url = apiUrl + '/updatetime/'+botId+'/'+nowtime
    
    req = requests.get(url)
    try:
        tinderLastTime = req.json()
        return tinderLastTime[need]
    except Exception as e:
        print(e)
        return {"error": "Something wrong. in trafficstandard.com."}


def tinderGetMessage(matchInfoForMessage):
    url = apiUrl+'/'+matchInfoForMessage["profileId"]+'/'+matchInfoForMessage["lastlogin"]+'/'+matchInfoForMessage["body"]
    #/28/lastlogin/body
    req = requests.get(url)
    try:
        retundata = req.json()
        return retundata
    except Exception as e:
        print(e)
        return {"error": "Something wrong. in trafficstandard.com. for new message"}



def tinderGetAuthToken(matchInfoForMessage):
    url = apiUrl+'/token/'+botId
    req = requests.get(url,)
    try:
        retundata = req.json()
        return retundata
    except Exception as e:
        print(e)
        return {"error": "Something wrong. in trafficstandard.com. for new message"}



def get_auth_token(fb_auth_token, fb_user_id):
    if "error" in fb_auth_token:
        return {"error": "could not retrieve fb_auth_token"}
    if "error" in fb_user_id:
        return {"error": "could not retrieve fb_user_id"}
    url = host + '/auth'
    req = requests.post(url,
                        headers=backup_headers,
                        data=json.dumps(
                            {'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
                        )
    try:
        tinder_auth_token = req.json()["token"]
        backup_headers.update({"X-Auth-Token": tinder_auth_token})
        print("You have been successfully authorized!")
        return tinder_auth_token
    except Exception as e:
        print(e)
        return {"error": "Something went wrong. Sorry, but we could not authorize you."}
# auth_tokens =get_auth_token('', '111866143039284')
token =input('giv me your token :')
backup_headers.update({"X-Auth-Token": token})

#auth_token =get_auth_token(config.fb_access_token, config.fb_user_id)
#print(auth_token)
# def authverif():
#     res = get_auth_token(config.fb_access_token, config.fb_user_id)
#     if "error" in res:
#         return False
#     return True

#print('authverify')
#print(authverif())
def get_recommendations():
    '''
    Returns a list of users that you can swipe on
    '''
    try:
        r = requests.get('https://api.gotinder.com/user/recs', headers=backup_headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting recomendations:", e)


def get_updates(last_activity_date=""):
    '''
    Returns all updates since the given activity date.
    The last activity date is defaulted at the beginning of time.
    Format for last_activity_date: "2017-07-09T10:28:13.392Z"
    https://api.gotinder.com/updates?is_boosting=false&boost_cursor=0
    '''
    try:
        url = host + "/updates"
        r = requests.post(url,
                          headers=backup_headers,
                          data=json.dumps({"last_activity_date": last_activity_date}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting updates:", e)


def get_self():
    '''
    Returns your own profile data
    '''
    try:
        url = host + '/profile'
        r = requests.get(url, headers=backup_headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your data:", e)


def change_preferences(**kwargs):
    '''
    ex: change_preferences(age_filter_min=30, gender=0)
    kwargs: a dictionary - whose keys become separate keyword arguments and the values become values of these arguments
    age_filter_min: 18..46
    age_filter_max: 22..55
    age_filter_min <= age_filter_max - 4
    gender: 0 == seeking males, 1 == seeking females
    distance_filter: 1..100
    discoverable: true | false
    {"photo_optimizer_enabled":false}
    '''
    try:
        url = host + '/profile'
        r = requests.post(url, headers=backup_headers, data=json.dumps(kwargs))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not change your preferences:", e)


def get_meta():
    '''
    Returns meta data on yourself. Including the following keys:
    ['globals', 'client_resources', 'versions', 'purchases',
    'status', 'groups', 'products', 'rating', 'tutorials',
    'travel', 'notifications', 'user']
    '''
    try:
        url = host + '/meta'
        r = requests.get(url, headers=backup_headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your metadata:", e)


def update_location(lat, lon):
    '''
    Updates your location to the given float inputs
    Note: Requires a passport / Tinder Plus
    '''
    try:
        url = host + '/passport/user/travel'
        r = requests.post(url, headers=backup_headers, data=json.dumps({"lat": lat, "lon": lon}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)

def reset_real_location():
    try:
        url = host + '/passport/user/reset'
        r = requests.post(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)


def get_recs_v2():
    '''
    This works more consistently then the normal get_recommendations becuase it seeems to check new location
    '''
    try:
        url = host + '/v2/recs/core?locale=en-US'
        r = requests.get(url, headers=backup_headers)
        return r.json()
    except Exception as e:
        print('excepted'+e)
def set_webprofileusername(username):
    '''
    Sets the username for the webprofile: https://www.gotinder.com/@YOURUSERNAME
    '''
    try:
        url = host + '/profile/username'
        r = requests.put(url, headers=backup_headers,
                         data=json.dumps({"username": username}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not set webprofile username:", e)

def reset_webprofileusername(username):
    '''
    Resets the username for the webprofile
    '''
    try:
        url = host + '/profile/username'
        r = requests.delete(url, headers=backup_headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not delete webprofile username:", e)

def get_person(userid):
    '''
    Gets a user's profile via their id
    '''
    try:
        url = host + '/user/%s' % userid
        r = requests.get(url, headers=backup_headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get that person:", e)


def send_msg(match_id, msg):
    try:
        url = host + '/user/matches/%s' % match_id
        r = requests.post(url, headers=backup_headers,
                          data=json.dumps({"message": msg}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not send your message:", e)


def superlike(person_id):
    try:
        url = host + '/like/%s/super' % person_id
        r = requests.post(url, headers=backup_headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not superlike:", e)


def like(person_id,datas):
    try:
        url = host + '/like/%s' % person_id
#         json.dumps(
        r = requests.post(url, headers=backup_headers, data=json.dumps(datas))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not like:", e)


def dislike(person_id):
    try:
        url = host + '/pass/%s' % person_id
        r = requests.get(url, headers=backup_headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not dislike:", e)


def report(person_id, cause, explanation=''):
    '''
    There are three options for cause:
        0 : Other and requires an explanation
        1 : Feels like spam and no explanation
        4 : Inappropriate Photos and no explanation
    '''
    try:
        url = host + '/report/%s' % person_id
        r = requests.post(url, headers=backup_headers, data={
                          "cause": cause, "text": explanation})
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not report:", e)


def match_info(match_id):
    try:
        url = host + '/matches/%s' % match_id
        r = requests.get(url, headers=backup_headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your match info:", e)

def all_matches():
    try:
        url = host + '/v2/matches'
        r = requests.get(url, headers=backup_headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your match info:", e)

def see_friends():
    try:
        url = host + '/group/friends'
        r = requests.get(url, headers=backup_headers)
        return r.json()['results']
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your Facebook friends:", e)

def set_profile_location():
    try:
        url = host + '/user/ping '
        datas = {'lat':'36.859894','lon':'-117.310645'}
        r = requests.post(url, data = json.dumps(datas),headers=backup_headers)
        
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your Facebook friends:", e)

           
            
def all_new_update():
    update_message =get_updates(tinderLastUpdate('last_updates'))
    
    for update in update_message['matches']:
        
        match_id = update['_id']
        message = update['messages'];
        if len(message)==1:
            lastMessasge=message[0]
            tinderUserMessage = lastMessasge['message']
        elif len(message) == 2:
            lastMessasge=message[1]
            tinderUserMessage = lastMessasge['message']
        elif len(message) == 0:
            tinderUserMessage = 'new user'
        else:
            lastMessasge=message[-1]
            tinderUserMessage = lastMessasge['message']
        matchInfoForMessage ={'lastlogin':match_id,
                              'profileId':profile_id,
                              'body':tinderUserMessage
                              }
        m_text =tinderGetMessage(matchInfoForMessage)
       
        
        #64d73ebf-9665-4996-b845-06a0db6b5731
        print('message body')
        print(m_text)
        if type(m_text)==dict:
            if 'body' in m_text:
                
                time.sleep(random.randint(10,30))
                print(send_msg(match_id, m_text['body']))
                
                print('sent messagse')
            print('not find body')
            
             
            
        
            
        
        #runtime
for x in range(0, 100):
    nowtime =datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+"Z"
    finds =get_recs_v2()
    if 'error' in finds:
        
        
        print(finds['error'])
        sleep_time = random.randint(80,100)
        time.sleep(sleep_time)
        break
    else:
        
        print(tinderLastUpdate('last_updates'))
        finduser=finds['data']['results']
        for find in finduser:
            sleep_time = random.randint(1,5)
            time.sleep(sleep_time)
            
            print(sleep_time)
            print(nowtime)
            if find["type"] == 'user':
                
                user_id =find['user']['_id']
                photo_id = find['user']['photos'][0]['id']
                user_s_number = find['s_number']
                c_hash =find['content_hash']
                   
                t_json_data={"photoId": photo_id,"content_hash": c_hash,"s_number": user_s_number}
                likeOrDislike = random.randint(1,4)
                Dislike = random.randint(1,2)
                print('like or dislike' +str(likeOrDislike))
                print('dislike' +str(Dislike))
                if  likeOrDislike==Dislike:
                    print('dislike')
                    #dislike
                    
                    dislike(user_id)
                    all_new_update()
                    
                else:
                    print('like code')
                    #like
                    likecode =like(user_id, t_json_data)
                    print(likecode)
                    all_new_update()
                     
                      
                 
            else:
                print('1')
        
            
    
    
    
input('your bot off?')

  
