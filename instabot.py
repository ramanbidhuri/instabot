import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

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

        if user_info['meta']['code'] == 200: #HTTP 200 means transmission is OK

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
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'

    else:
        print 'Status code other than 200 received!'


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
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'There is no recent post!'

    else:
        print 'Status code other than 200 received!'

#method to get post ID of user
def get_post_id(insta_username):
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
            print 'There is no recent post of the user!'
            exit()

    else:
        print 'Status code other than 200 received!'
        exit()


#method to like a post by post ID
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {'access_token': APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like['meta']['code'] == 200: #HTTP 200 means transmission is OK
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


#method to comment on post by user
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {'access_token': APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200: #HTTP 200 means transmission is OK
        print 'Successfully added a new comment!'
    else:
        print 'Unable to add comment. Try again!'


#method to delete negative comments from post
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200: #HTTP 200 means transmission is OK

        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'

                else:
                    print 'Positive comment : %s\n' % (comment_text)

        else:
            print 'There are no existing comments on the post!'

    else:
        print 'Status code other than 200 received!'


def start_bot():
    while True:
        print '\n'
        print 'Welcome to instaBot!'
        print 'Your menu options are:'
        print 'a.Get your own details\n'
        print 'b.Get details of a user by username\n'
        print 'c.Get details of our post\n'
        print 'd.Get post of user by username\n'
        print 'e.Get a list of people who have liked the recent post of a user\n'
        print 'f.Like the recent post of a user\n'
        print 'g.Get a list of comments on the recent post of a user\n'
        print 'h.Make a comment on the recent post of a user\n'
        print 'i.Delete negative comments from the recent post of a user\n'
        print 'j.Exit'

        choice=raw_input('Enter you choice: ')
        if choice=='a':
            self_info()
        elif choice=='b':
            insta_username = raw_input('Enter the username of the user: ')
            get_user_info(insta_username)
        elif choice=='c':
            get_own_post()
        elif choice=='d':
            insta_username = raw_input('Enter the username of the user: ')
            get_users_post(insta_username)
        elif choice == 'e':
            insta_username = raw_input('Enter the username of the user: ')
            like_a_post(insta_username)
        elif choice == 'f':
            insta_username = raw_input('Enter the username of the user: ')
            like_a_post(insta_username)
        elif choice == 'g':
            insta_username = raw_input('Enter the username of the user: ')
            post_a_comment(insta_username)
        elif choice == 'h':
            insta_username = raw_input('Enter the username of the user: ')
            post_a_comment(insta_username)
        elif choice == 'i':
            insta_username = raw_input('Enter the username of the user: ')
            delete_negative_comment(insta_username)
        elif choice == 'j':
            exit()
        else:
            print 'wrong choice'
start_bot()