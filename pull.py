def github_receiver():
    if request.headers['Content-Type'] == 'application/json':
        payload = request.json
        pull_request_id = payload.get('pull_request', {}).get('id')
        author = payload.get('pull_request', {}).get('user', {}).get('login')
        action = payload.get('action')
        base_branch = payload.get('pull_request', {}).get('base', {}).get('ref')
        head_branch = payload.get('pull_request', {}).get('head', {}).get('ref')
        timestamp = payload.get('pull_request', {}).get('created_at')
        
        print(pull_request_id, author, action, base_branch, head_branch, timestamp)
        
        return jsonify({'message': 'Received and stored GitHub event successfully.'}), 200