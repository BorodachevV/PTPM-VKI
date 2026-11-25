"""Тесты для ForumParser (Hacker News) с моком реального ответа."""
import unittest
from unittest.mock import patch, Mock

from src.parser import ForumParser
from src.database import DatabaseRepository


# Реальный фрагмент HTML-страницы Hacker News (сокращён для читаемости)
# Взято с https://news.ycombinator.com/item?id=50624497
HN_HTML_SNIPPET = """
<html><body><table>
<tr class="athing comtr" id="50625926">
  <td><table><tr>
    <td class="default">
      <span class="comhead">
        <a href="user?id=xydone">xydone</a>
        <span class="age">...</span>
      </span>
      <div class="comment">
        <div class="commtext c00">
          How could it be that you like the human aspect that AI has allowed you to focus on?
        </div>
      </div>
    </td>
  </tr></table></td>
</tr>
<tr class="athing comtr" id="50625824">
  <td><table><tr>
    <td class="default">
      <span class="comhead">
        <a href="user?id=amosj">amosj</a>
      </span>
      <div class="comment">
        <div class="commtext c00">
          Thank you for saying it like it is. <b>JavaScript</b> is such a curse...
        </div>
      </div>
    </td>
  </tr></table></td>
</tr>
<tr class="athing comtr" id="50626102">
  <td><table><tr>
    <td class="default">
      <span class="comhead">
        <a href="user?id=lukan">lukan</a>
      </span>
      <div class="comment">
        <div class="commtext c00">
          What a blast from the past. <p>Javascript is ugly, but simple...</p>
        </div>
      </div>
    </td>
  </tr></table></td>
</tr>
</table></body></html>
"""


class TestForumParser(unittest.TestCase):

    def setUp(self):
        self.parser = ForumParser()

    # ---------- Тест 1: парсинг HTML с реальной структурой HN ---------- #
    def test_parse_html_extracts_comments(self):
        comments = self.parser.parse_html(HN_HTML_SNIPPET)

        self.assertEqual(len(comments), 3)
        ids = [c["id"] for c in comments]
        self.assertEqual(ids, [50625926, 50625824, 50626102])

        first = comments[0]
        self.assertEqual(first["name"], "xydone")
        self.assertIn("human aspect", first["message"])

    # ---------- Тест 2: сохранение внутренней HTML-разметки ----------- #
    def test_parse_html_preserves_inner_html(self):
        comments = self.parser.parse_html(HN_HTML_SNIPPET)
        amosj = next(c for c in comments if c["name"] == "amosj")
        self.assertIn("<b>JavaScript</b>", amosj["message"])

        lukan = next(c for c in comments if c["name"] == "lukan")
        self.assertIn("<p>", lukan["message"])

    # ---------- Тест 3: parse_page вызывает requests с заголовками ----- #
    @patch("src.parser.requests.get")
    def test_parse_page_uses_headers_and_parses(self, mock_get):
        mock_resp = Mock()
        mock_resp.text = HN_HTML_SNIPPET
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        comments = self.parser.parse_page("https://news.ycombinator.com/item?id=50624497")

        # Проверяем, что заголовки действительно передаются
        _, kwargs = mock_get.call_args
        self.assertIn("User-Agent", kwargs["headers"])
        self.assertIn("Mozilla", kwargs["headers"]["User-Agent"])

        self.assertEqual(len(comments), 3)

    # ---------- Тест 4: save_to_db и пропуск дубликатов --------------- #
    def test_save_to_db(self):
        repo = DatabaseRepository(":memory:")
        try:
            comments = self.parser.parse_html(HN_HTML_SNIPPET)
            stats = self.parser.save_to_db(comments, repo)
            self.assertEqual(stats["saved"], 3)
            self.assertEqual(stats["skipped"], 0)

            # Повторное сохранение — все 3 пропускаются как дубликаты
            stats2 = self.parser.save_to_db(comments, repo)
            self.assertEqual(stats2["saved"], 0)
            self.assertEqual(stats2["skipped"], 3)

            self.assertEqual(repo.get_by_id(50625926)["name"], "xydone")
        finally:
            repo.close()

    # ---------- Тест 5: некорректные строки игнорируются --------------- #
    def test_parse_html_skips_invalid_rows(self):
        broken_html = """
        <table>
            <tr class="athing comtr" id="not-a-number">
                <td><span class="comhead"><a href="user?id=bad">bad</a></span>
                    <div class="commtext">x</div></td>
            </tr>
            <tr class="athing comtr" id="123">
                <!-- нет username -->
                <td><div class="commtext">only message</div></td>
            </tr>
        </table>
        """
        comments = self.parser.parse_html(broken_html)
        self.assertEqual(comments, [])


if __name__ == "__main__":
    unittest.main()