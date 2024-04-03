from flask import Flask, request, jsonify

app = Flask(__name__)

# Routes
@app.route('/')
def api_route():
    return 'Welcome guys'

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
            print("{} pushed to {} on {}".format(pushed_by, to_branch, timestamp))
        elif action == 'opened':
            base_branch = payload.get('pull_request', {}).get('base', {}).get('ref')
            head_branch = payload.get('pull_request', {}).get('head', {}).get('ref')
            timestamp = payload.get('pull_request', {}).get('created_at')
            print("{author} submitted a pull request from {head_branch} to {base_branch} on {timestamp}".format(author=author, base_branch=base_branch, head_branch=head_branch, timestamp=timestamp))
        elif action == 'closed' and payload.get('pull_request', {}).get('merged'):
            base_branch = payload.get('pull_request', {}).get('base', {}).get('ref')
            head_branch = payload.get('pull_request', {}).get('head', {}).get('ref')
            timestamp = payload.get('pull_request', {}).get('updated_at')
            print("{author} marged branch {head_branch} to {base_branch} at {timestamp}".format(author=author, head_branch=head_branch,base_branch=base_branch,timestamp= timestamp))
        return jsonify({'message': 'Push event received successfully.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
