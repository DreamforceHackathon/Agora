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
g = sf.Topic__c.describe()
#print g[u'fields']

@app.route('/')
def root():
    return render_template("index.html")
    
# returns the categories
@app.route('/agora/api/v1.0/categories', methods=['GET'])
def get_category():
    g = requests.get('https://na17.salesforce.com/services/data/v32.0/sobjects/')
    print g.content
    #return 'got category'
    #return r

# up to ten most recent topics in category, comes with its ID, name, body, should be in a json, output a json
@app.route('/apora/api/v1.0/topics/<string:category>', methods=['GET'])
def get_topics(category):
    return 'got topics'
    
# just get one topic object
@app.route('/agora/api/v1.0/topic/<int:topic_id>', methods=['GET'])
def get_topic(topic_id):
    return 'got topic'
    
# save this for last, but just get one post
@app.route('/agora/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    return 'got post'
    
# posts a new topic
@app.route('/agora/api/v1.0/topics', methods=['POST'])
def create_topic():
    if not request.json:
        abort(400)
    return 'created topic'
    
# posts a new post
@app.route('/agora/api/v1.0/posts', methods=['POST'])
def create_post():
    if not request.json:
        abort(400)
    return 'created post'
        
# upvote a post, will also need to update the uer's upvoted posts
@app.route('/agora/api/v1.0/upvote/<int:post_id>', methods=['POST'])
def upvote_post():
    return 'upvoted post'
    
# downvote a post, will also need to update the user's downvoted posts
@app.route('/agora/api/v1.0/downvote/<int:post_id>', methods=['POST'])
def downvote_post():
    return 'downvoted post'
    
    








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