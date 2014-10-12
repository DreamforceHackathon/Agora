# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 18:08:10 2014

@author: Glen
"""

#!flask/bin/python
import os
import requests
from flask import Flask, jsonify, abort, make_response, request, render_template
from simple_salesforce import Salesforce

app = Flask(__name__, static_url_path='')


API_TOKEN = 'grant_type=authorization_code&code=aPrx1RSrhEAk35g3vWVIj1w5s4jeUCttHF0qXEGouMqTKbDULbkwVD8NOiUI5Y5lnDdsZyJucw&client_id=3MVG9xOCXq4ID1uHzDUJaB8LxhY3TuCmiDJHrtblRlm0O69H7axRTz48UhHaIK7Tbjizj1FbVT1sWD6P992.I&client_secret=2117209309553996388&redirect_uri=https%3A%2F%2Flocalhost%2Foauth'
REQUEST_ENDPOINT = 'https://login.salesforce.com/services/oauth2/token'
payload = {'grant_type': 'password', 'client_id': '3MVG9xOCXq4ID1uHzDUJaB8LxhY3TuCmiDJHrtblRlm0O69H7axRTz48UhHaIK7Tbjizj1FbVT1sWD6P992.I', 'client_secret': '2117209309553996388', 'username': 'tlim007@ucr.edu', 'password' : '13791LOMeYeASGmMyXehAwMmCqqh6ZSk9'}
r = requests.post(REQUEST_ENDPOINT, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload)
ACCESS_TOKEN = eval(r.content)['access_token']

#sf = Salesforce(instance='https://na17.salesforce.com/', session_id=ACCESS_TOKEN)
sf = Salesforce(username='tlim007@ucr.edu', password='13791LOM', security_token='eYeASGmMyXehAwMmCqqh6ZSk9')
#g = sf.Topic__c.describe()
#print type(g)
#d = dict(g)
#print type(d)

listToDict = lambda lst: {i: lst[i] for i in range(len(lst))}

#print type(jsonify(g))
#print g[u'fields']

@app.route('/')
def root():
    return render_template("index.html")
    
# returns the categories
@app.route('/agora/api/v1.0/categories', methods=['GET'])
def get_category():
    #ls = {0: 'Local', 1: 'State', 2: 'National', 3: 'International'}
    categories = ['Local', 'State', 'National', 'International']
    return jsonify(categories=categories)

# up to ten most recent topics in category, comes with its ID, creation date, name, body, should be in a json, output a json
@app.route('/agora/api/v1.0/topics/<string:category>', methods=['GET'])
def get_topics(category):
    query = "SELECT Name, Topic_ID__c, CreatedDate, Topic_Body__c , Category__c FROM Topic__c WHERE Category__c = '%s' ORDER BY CreatedDate DESC" %category
    oDict = sf.query(query)
    return jsonify(topics=oDict['records'])
    
# just get one topic object, topic id, title, body, max 50 posts
@app.route('/agora/api/v1.0/topic/<string:topic_id>', methods=['GET'])
def get_topic(topic_id):
    topicQuery  = "SELECT Name, id, Topic_Body__c FROM Topic__c WHERE Topic_ID__c = '%s'" %topic_id
    topicODict = sf.query(topicQuery)
    
    ID = topicODict['records'][0]['Id']
        
    mainList = topicODict['records']
    
    postQuery = "SELECT Post_Body__c, CreatedDate, UpVote__c, DownVote__c, Netvalue__c, Post_User__c, id, Post_ID__c, Position__c FROM Post__c WHERE Topic_ID__c = '%s' ORDER BY Netvalue__c DESC" %ID
    postODict = sf.query(postQuery)
    
    postsList = postODict['records']
    mainList[0]['posts'] = postsList
    
    return jsonify(topic=mainList)
    
# save this for last, but just get one post
@app.route('/agora/api/v1.0/post/<string:post_id>', methods=['GET'])
def get_post(post_id):
    query = "SELECT Post_Body__c, CreatedDate, UpVote__c, DownVote__c, Username__c, Post_User__c, Id, Post_ID__c, Position__c FROM Post__c WHERE Post_ID__c= '%s'" %post_id
    oDict = sf.query(query)    
    return jsonify(post=oDict['records'])
    
# posts a new topic
@app.route('/agora/api/v1.0/topics', methods=['POST'])
def create_topic():
    if not request.json:
        abort(400)
    return 'created topic'
    
# posts a new post, also add that post to the contact's history
@app.route('/agora/api/v1.0/newpost', methods=['POST'])
def create_post():
    
    #return jsonify(request.json)
    
    if not request.json:
        abort(400)
        
    topic_id = request.json['Topic_ID__c'] #    'a00o0000003kzhR' # the long way 
    #post_id = ''
    user_id = request.json['Post_User__c']      #'003o000000BTVrI' #long one
    position = request.json['Position__c']      #'Against'
    body = request.json['Post_Body__c']                  #'test from local host'
    #name = topic_id + ' (arbitrary)'
    """
    
    topic_id = 'a00o0000003kzhR'
    user_id = '003o000000BTVrI'
    position = 'Against'
    body = 'test from local host'
    """
    
    return str(sf.Post__c.create({'Topic_ID__c': topic_id, 'Post_User__c': user_id, 'Position__c': position,'Post_Body__c': body}))

@app.route('/test', methods=['POST'])
def test():
    return request.json;
        
# upvote a post, will also need to update the uer's upvoted posts
# actually takes the short ID
@app.route('/agora/api/v1.0/upvote/', methods=['POST'])
def upvote_post():
    short_id = request.json['short ID']
    long_id = request.json['long ID']
    query = "SELECT UpVote__c, DownVote__c FROM Post__c WHERE Post_ID__c = '%s'" %short_id
    oDict = sf.query(query)
    #return jsonify(oDict)
    upvote = int(oDict['records'][0]['UpVote__c'])
    return str(sf.Post__c.update(long_id,{'UpVote__c': upvote+1}))
    
# downvote a post, will also need to update the user's downvoted posts
@app.route('/agora/api/v1.0/downvote/', methods=['POST'])
def downvote_post():
    short_id = request.json['short ID']
    long_id = request.json['long ID']
    query = "SELECT UpVote__c, DownVote__c FROM Post__c WHERE Post_ID__c = '%s'" %short_id
    oDict = sf.query(query)
    downvote = int(oDict['records'][0]['DownVote__c'])
    return str(sf.Post__c.update(long_id,{'DownVote__c': downvote+1}))
   
    








tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]



"""
 
@app.route('/')
def root():
    return 'Hello World'
"""
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})
    
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201






if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)