"""Демонстрация пайплайна на реальной странице Hacker News."""
from src.database import DatabaseRepository
from src.parser import ForumParser


def main():
    # Реальная ссылка на обсуждение Hacker News
    url = "https://news.ycombinator.com/item?id=50624497"

    repo = DatabaseRepository("hn_comments.db")
    parser = ForumParser()

    print(f"Парсим: {url}")
    try:
        comments = parser.parse_page(url)
    except Exception as exc:
        print(f"Не удалось загрузить страницу: {exc}")
        repo.close()
        return

    print(f"Найдено комментариев: {len(comments)}")
    for c in comments[:5]:  # показываем первые 5
        print(f"  #{c['id']} — {c['name']}: {c['message'][:80]}...")

    stats = parser.save_to_db(comments, repo)
    print(f"\nСохранено: {stats['saved']}, пропущено (дубликаты): {stats['skipped']}")

    # Пример чтения из БД
    if comments:
        first_id = comments[0]["id"]
        row = repo.get_by_id(first_id)
        print(f"\nИз БД по ID {first_id}: {row['name']}")

    repo.close()


if __name__ == "__main__":
    main()