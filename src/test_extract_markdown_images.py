import unittest

from markdown_parser import extract_markdown_images


class TestExtractMarkdownImages(unittest.TestCase):

    def test_extract_markdown_image(self):
        """Should return a list of tuples for an image"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        """Should handle multiple images"""
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)."
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_ignore_markdown_link(self):
        """Should not return tuples for a link"""
        matches = extract_markdown_images(
            "This is text with an ![image of trees](https://i.imgur.com/U2LJarL.jpeg) and a [random link](https://google.com)."
        )
        self.assertListEqual(
            [("image of trees", "https://i.imgur.com/U2LJarL.jpeg")], matches
        )


if __name__ == "__main__":
    unittest.main()
