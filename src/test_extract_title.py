import unittest

from markdown_parser import extract_title

# from htmlnode import ParentNode


class TestExtractTitle(unittest.TestCase):

    def test_title(self):
        """Should return a title if found"""
        md = """
# This is a heading

## This is a subheading

This is a paragraph with _italic_ text and `code` here

#ThisIsAHashtag

"""

        title = extract_title(md)
        self.assertEqual(
            title,
            "This is a heading",
        )

    def test_title_not_found(self):
        """Should return an exception if title not found"""
        md = """
## This is a subheading

This is a paragraph with _italic_ text and `code` here

#ThisIsAHashtag

"""

        self.assertRaises(Exception, extract_title, md)


if __name__ == "__main__":
    unittest.main()
