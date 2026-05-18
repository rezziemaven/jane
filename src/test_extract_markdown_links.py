import unittest

from markdown_parser import extract_markdown_links


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_extract_markdown_image(self):
        """Should return a list of tuples for a link"""
        matches = extract_markdown_links(
            "[GitHub](https://github.com) is where people build software (apparently)."
        )
        self.assertListEqual([("GitHub", "https://github.com")], matches)

    def test_extract_multiple_links(self):
        """Should handle multiple links"""
        matches = extract_markdown_links(
            "This is text with a link to [Boot.dev](https://www.boot.dev) and to [YouTube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("Boot.dev", "https://www.boot.dev"),
                ("YouTube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_ignore_markdown_image(self):
        """Should not return tuples for an image"""
        matches = extract_markdown_links(
            "This is a ![random image](https://i.imgur.com/n0yLJZW.jpeg) while this is a [random link](https://www.wikipedia.org/)."
        )
        self.assertListEqual([("random link", "https://www.wikipedia.org/")], matches)


if __name__ == "__main__":
    unittest.main()
