def log_article_creation(article_id: int):
    with open("notify.log", "a", encoding="utf-8") as f:
        f.write(f"Article {article_id} created.\n")
