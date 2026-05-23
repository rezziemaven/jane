import unittest

from textnode import TextType, TextNode
from markdown_parser import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_bold(self):
        """Should handle bold text"""
        node = TextNode(
            "This is text with a **bolded phrase** in the middle.", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_code(self):
        """Should handle code text"""
        node = TextNode("This is text with a `code block` word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_italic(self):
        """Should handle italic text"""
        node = TextNode("This is text with _emphasis_ for impact!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("emphasis", TextType.ITALIC),
                TextNode(" for impact!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple(self):
        """Should handle multiple instances of markdown"""
        """Should handle bold text"""
        node = TextNode(
            "**I like** bolding my text at the beginning **and the end!**",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("I like", TextType.BOLD),
                TextNode(" bolding my text at the beginning ", TextType.TEXT),
                TextNode("and the end!", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_not_split(self):
        """Should not split text if type is not text"""
        node1 = TextNode("I'm just a link", TextType.LINK, "https://google.com")
        node2 = TextNode("_I should be split!_ I like code.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("I'm just a link", TextType.LINK, "https://google.com"),
                TextNode("I should be split!", TextType.ITALIC),
                TextNode(" I like code.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_ending_punctuation_marks(self):
        """Should split ending punctuation marks as text"""
        node = TextNode("Hello **Jane**!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("Jane", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_delimiter(self):
        """Should leave text whole if no delimiter was found"""
        node = TextNode("This text should stay the same.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [TextNode("This text should stay the same.", TextType.TEXT)], new_nodes
        )

    def test_missing_matching_delimiter(self):
        """Should raise an exception if matching delimiter is missing"""
        node = TextNode("This should **raise an error ...", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
