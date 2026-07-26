os = __import__('os')
from atproto import Client, models

USERNAME = os.environ.get('BSKY_HANDLE')
PASSWORD = os.environ.get('BSKY_PASSWORD')
HOSTNAME = "bluesky-tracker.onrender.com"
FEED_SHORTNAME = "alexasks"
DISPLAY_NAME = "AlexAsks (Archive)"

client = Client()
client.login(USERNAME, PASSWORD)

feed_did = f"did:web:{HOSTNAME}"
response = client.com.atproto.repo.put_record(models.ComAtprotoRepoPutRecord.Data(
    repo=client.me.did,
    collection='app.bsky.feed.generator',
    rkey=FEED_SHORTNAME,
    record=models.AppBskyFeedGenerator.Record(
        did=feed_did,
        display_name=DISPLAY_NAME,
        created_at=client.get_current_time_iso()
    )
))

print(f"Flux publié avec succès ! URI : {response.uri}")
