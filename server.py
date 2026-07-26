import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/.well-known/atproto-did', methods=['GET'])
def atproto_did():
    publisher_did = os.environ.get('PUBLISHER_DID', 'did:plc:due764fs3onxetsxab2jdnrw')
    return publisher_did, 200, {'Content-Type': 'text/plain'}

@app.route('/xrpc/app.bsky.feed.getFeedSkeleton', methods=['GET'])
def get_feed_skeleton():
    feed = []
    if os.path.exists("archive_posts.txt"):
        with open("archive_posts.txt", "r", encoding="utf-8") as f:
            for line in f.read().splitlines():
                if '|' in line:
                    post_uri = line.split('|')[0].strip()
                    if post_uri.startswith('at://'):
                        feed.append({"post": post_uri})
    
    return jsonify({"feed": feed[:100]})

@app.route('/xrpc/app.bsky.feed.describeFeedGenerator', methods=['GET'])
def describe_feed_generator():
    hostname = request.host
    publisher_did = os.environ.get('PUBLISHER_DID', 'did:plc:due764fs3onxetsxab2jdnrw')
    return jsonify({
        "encoding": "application/json",
        "body": {
            "uri": f"at://{publisher_did}/app.bsky.feed.generator/alexasks",
            "feeds": [{"uri": f"at://{publisher_did}/app.bsky.feed.generator/alexasks"}]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
