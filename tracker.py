import os
from atproto import Client

USERNAME = os.environ.get('BSKY_HANDLE')
PASSWORD = os.environ.get('BSKY_PASSWORD')

def main():
    client = Client()
    client.login(USERNAME, PASSWORD)

    query = "#alexasks OR #alexask"
    print(f"Recherche en cours pour : {query}")
    
    filename = "archive_posts.txt"
    
    existing_posts = set()
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            existing_posts = set(line.split('|')[0] for line in f.read().splitlines() if '|' in line)

    new_count = 0
    cursor = None

    try:
        while True:
            params = {'q': query, 'limit': 100}
            if cursor:
                params['cursor'] = cursor

            data = client.app.bsky.feed.search_posts(params=params)
            
            if not data.posts:
                break

            with open(filename, "a", encoding="utf-8") as f:
                for post in data.posts:
                    post_id = post.uri
                    if post_id not in existing_posts:
                        author = post.author.handle if post.author else "inconnu"
                        text = post.record.text.replace("\n", " ") if post.record and post.record.text else ""
                        date = post.record.created_at if post.record else ""
                        
                        f.write(f"{post_id}|{date}|{author}|{text}\n")
                        existing_posts.add(post_id)
                        new_count += 1

            if not data.cursor:
                break
            cursor = data.cursor

        print(f"Mise à jour terminée. {new_count} nouveaux posts ajoutés à l'archive.")

    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")

if __name__ == "__main__":
    main()
