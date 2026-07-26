import os
from atproto import Client, models

USERNAME = os.environ.get('BSKY_HANDLE')
PASSWORD = os.environ.get('BSKY_PASSWORD')
HOSTNAME = "bluesky-tracker.onrender.com"
FEED_SHORTNAME = "alexasks2"
DISPLAY_NAME = "AlexAsks"

client = Client(base_url='https://bsky.social')

try:
    print("Connexion à Bluesky en cours...")
    client.login(USERNAME, PASSWORD)
    
    print("Publication du flux sur le serveur externe...")
    response = client.com.atproto.repo.put_record(models.ComAtprotoRepoPutRecord.Data(
        repo=client.me.did,
        collection='app.bsky.feed.generator',
        rkey=FEED_SHORTNAME,
        record=models.AppBskyFeedGenerator.Record(
            did=f"did:web:{HOSTNAME}",
            display_name=DISPLAY_NAME,
            created_at=client.get_current_time_iso()
        )
    ))
    print(f"Flux publié avec succès ! URI : {response.uri}")

except Exception as e:
    print(f"Erreur lors de la publication : {e}")
    raise e
