from flask import Flask, request, jsonify
from extension import db, collection
from flask import render_template

app = Flask(__name__)

# Routes
@app.route('/')
def api_route():
    pull_requests_data = collection.find()
    return render_template('index.html', pull_requests=pull_requests_data)

@app.route('/api/data')
def get_data():
    pull_requests = collection.find()
    # Convert ObjectId to strings
    pull_requests = [{**pr, '_id': str(pr['_id'])} for pr in pull_requests]
    return jsonify(pull_requests)


@app.route('/webhook', methods=['POST'])
def github_receiver():
    print("Received a webhook request.")
    if request.headers['Content-Type'] == 'application/json':
        payload = request.json
        action = payload.get('action')
        author = payload.get('pull_request', {}).get('user', {}).get('login')
        if "pusher" in payload:
            ref = payload.get('ref')
            to_branch = ref.split('/')[-1]  # Extracting branch name from ref
            pushed_by = payload.get('pusher', {}).get('name')
            timestamp = payload.get('head_commit', {}).get('timestamp')
            collection.insert_one({
                'request_id':None,
                'author':pushed_by,
                'action':'push',
                'from_branch':None,
                'to_branch':to_branch,
                'timestamp':timestamp
            })
            
        elif action == 'opened':
            pull_request_id = payload.get('pull_request', {}).get('id')
            base_branch = payload.get('pull_request', {}).get('base', {}).get('ref')
            head_branch = payload.get('pull_request', {}).get('head', {}).get('ref')
            timestamp = payload.get('pull_request', {}).get('created_at')
        
            collection.insert_one({
                'request_id':pull_request_id,
                'author':author,
                'action':action,
                'from_branch':head_branch,
                'timestamp':timestamp
            })
    
        elif action == 'closed' and payload.get('pull_request', {}).get('merged'):
            merged_pr_id = payload.get('pull_request', {}).get('id')
            base_branch = payload.get('pull_request', {}).get('base', {}).get('ref')
            head_branch = payload.get('pull_request', {}).get('head', {}).get('ref')
            timestamp = payload.get('pull_request', {}).get('updated_at')
            collection.insert_one({
                'request_id':merged_pr_id,
                'author':author,
                'action':action,
                'from_branch':head_branch,  
                'to_branch':base_branch,
                'timestamp':timestamp
            })
        return jsonify({'message': 'Push event received successfully.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
