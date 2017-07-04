import requests

#Token Owner : ramanbidhuri
#Sandbox Users : khattarsakshi,insta.mriu.test.04,aanchal_arora_

APP_ACCESS_TOKEN = '1641251650.e268c6d.1782913bfb9d42a2b628f566725cc02e'
BASE_URL = 'https://api.instagram.com/v1/'


#method to get self information
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200: #HTTP 200 means transmission is OK
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'Number of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'Number of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'Number of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!' #HTTP 200 means transmission is OK


#method user ID by username
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200: #HTTP 200 means transmission is OK
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


#method to get user information by username
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    else:
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_info = requests.get(request_url).json()

        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                print 'Username: %s' % (user_info['data']['username'])
                print 'Number of followers: %s' % (user_info['data']['counts']['followed_by'])
                print 'Number of people you are following: %s' % (user_info['data']['counts']['follows'])
                print 'Number of posts: %s' % (user_info['data']['counts']['media'])
            else:
                print 'No data for this user!'
        else:
            print 'Status code other than 200 received!'


#method to get our post
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200: #HTTP 200 means transmission is OK
        if len(own_media['data']):
            return own_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
    return None


#method to get user post by username
def get_users_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200: #HTTP 200 means transmission is OK
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print "There is no recent post!"
    else:
        print 'Status code other than 200 received!'
    return None


def start_bot():
    while True:
        print '\n'
        print 'Welcome to instaBot!'
        print 'Your menu options are:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print 'c.Get details of our post\n'
        print 'd.Get post of user by username\n'
        print "e.Exit"

        choice=raw_input("Enter you choice: ")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice=="c":
            get_own_post()
        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            get_users_post(insta_username)
        elif choice=="e":
            exit()
        else:
            print "wrong choice"
start_bot()