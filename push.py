from flask import json
# to accept the request from github
from flask import request
from flask import Flask,jsonify

app = Flask(__name__)

# Routes
@app.route('/home')
def api_route():
    return 'Welcome guys'
@app.route('/webhook', methods =['POST'])
def github_receiver():
     if request.headers['Content-Type'] == 'application/json':
        payload = request.json
        ref = payload.get('ref')
        to_branch = ref.split('/')[-1]  # Extracting branch name from ref
        commits = payload.get('commits')
        pushed_by = payload.get('pusher', {}).get('name')
        timestamp = payload.get('head_commit', {}).get('timestamp')
        print("{} pushed to {} on {}".format(pushed_by, to_branch, timestamp))
        return jsonify({'message': 'Push event received successfully.'}), 200

        

if __name__ == '__main__':
    app.run(debug=True)