def merge_receiver():
    if request.headers['Content-Type'] == 'application/json':
        payload = request.json
        action = payload.get('action')
        if action == 'closed' and payload.get('pull_request', {}).get('merged'):
            merged_pr_id = payload.get('pull_request', {}).get('id')
            merged_by = payload.get('pull_request', {}).get('merged_by', {}).get('login')
            base_branch = payload.get('pull_request', {}).get('base', {}).get('ref')
            head_branch = payload.get('pull_request', {}).get('head', {}).get('ref')
            timestamp = payload.get('pull_request', {}).get('updated_at')
            
            print("Pull Request {} merged by {} into {} at {}".format(merged_pr_id, merged_by, base_branch, timestamp))
            
        return jsonify({'message': 'Merge event received successfully.'}), 200