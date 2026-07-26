import os
from atproto import Client

USERNAME = os.environ.get('BSKY_HANDLE')
PASSWORD = os.environ.get('BSKY_PASSWORD')

def main():
    client = Client()
    client.login(USERNAME, PASSWORD)

    query = "#alexasks OR #alexask"
    print(f"Recherche en cours pour : {query}")
    
    try:
        data = client.app.bsky.feed.search_posts(params={'q': query, 'limit': 25})
        
        filename = "archive_posts.txt"
        
        existing_posts = set()
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                existing_posts = set(f.read().splitlines())

        new_count = 0
        # Utilisation de 'a+' pour créer le fichier s'il n'existe pas encore
        with open(filename, "a+", encoding="utf-8") as f:
            for post in data.posts:
                post_id = post.uri
                if post_id not in existing_posts:
                    author = post.author.handle
                    # Sécurisation du texte pour éviter les sauts de ligne intempestifs
                    text = post.record.text.replace("\n", " ") if post.record and post.record.text else ""
                    date = post.record.created_at if post.record else ""
                    
                    f.write(f"{post_id}|{date}|{author}|{text}\n")
                    existing_posts.add(post_id)
                    new_count += 1
                    print(f"Nouveau post trouvé de @{author} : {text[:50]}...")

        print(f"Mise à jour terminée. {new_count} nouveaux posts ajoutés à l'archive.")

    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")

if __name__ == "__main__":
    main()
