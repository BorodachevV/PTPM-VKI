"""Модуль веб-парсера для Hacker News (news.ycombinator.com)."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional


class ForumParser:
    """
    Парсер комментариев Hacker News.

    Структура страницы обсуждения:
        <tr class="athing comtr" id="50625926">
            ...
            <span class="comhead"><a href="user?id=xydone">xydone</a> ...</span>
            <div class="comment"><div class="commtext c00">Текст...</div></div>
        </tr>
    """

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    # Селекторы Hacker News
    COMMENT_ROW_SELECTOR = "tr.athing.comtr"
    USERNAME_SELECTOR = "span.comhead a[href^='user?id=']"
    MESSAGE_SELECTOR = "div.commtext"

    def __init__(self, headers: Optional[dict] = None, timeout: int = 15):
        self.headers = {**self.DEFAULT_HEADERS, **(headers or {})}
        self.timeout = timeout

    # ------------------------------------------------------------------ #
    #                          Загрузка HTML                             #
    # ------------------------------------------------------------------ #
    def fetch_html(self, url: str) -> str:
        """Скачивает HTML-страницу обсуждения Hacker News."""
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    # ------------------------------------------------------------------ #
    #                          Парсинг                                   #
    # ------------------------------------------------------------------ #
    def parse_html(self, html: str) -> List[Dict[str, Any]]:
        """Разбирает HTML страницы Hacker News и возвращает список комментариев."""
        soup = BeautifulSoup(html, "lxml")
        comments: List[Dict[str, Any]] = []

        for row in soup.select(self.COMMENT_ROW_SELECTOR):
            comment_id = self._extract_id(row)
            if comment_id is None:
                continue

            username_el = row.select_one(self.USERNAME_SELECTOR)
            message_el = row.select_one(self.MESSAGE_SELECTOR)
            if username_el is None or message_el is None:
                continue

            comments.append({
                "id": comment_id,
                "name": username_el.get_text(strip=True),
                "message": message_el.decode_contents().strip(),
            })

        return comments

    @staticmethod
    def _extract_id(row) -> Optional[int]:
        """Извлекает ID комментария из атрибута id тега <tr>."""
        raw = row.get("id")
        if raw is None:
            return None
        try:
            return int(str(raw).strip())
        except (TypeError, ValueError):
            return None

    def parse_page(self, url: str) -> List[Dict[str, Any]]:
        """Скачивает страницу Hacker News и сразу возвращает список комментариев."""
        return self.parse_html(self.fetch_html(url))

    # ------------------------------------------------------------------ #
    #                          Сохранение в БД                           #
    # ------------------------------------------------------------------ #
    def save_to_db(self, parsed_data: List[Dict[str, Any]], repository) -> Dict[str, int]:
        """Сохраняет комментарии через DatabaseRepository."""
        saved, skipped = 0, 0
        for item in parsed_data:
            try:
                repository.add(item["id"], item["name"], item["message"])
                saved += 1
            except ValueError:
                skipped += 1
        return {"saved": saved, "skipped": skipped}