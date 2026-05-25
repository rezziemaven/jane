import unittest

from textnode import TextType, TextNode
from markdown_parser import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):

    def test_simple_text(self):
        """Should split simple text into the correct nodes"""
        text = "This is **bolded text**"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bolded text", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_only_markdown(self):
        """Should split text that only contains markdown"""
        text = "_This is an italic sentence_"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is an italic sentence", TextType.ITALIC)], new_nodes
        )

    def test_split_all_types(self):
        """Should split text into all text types"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_ending_punctuation_marks(self):
        """Should split ending punctuation marks as text"""
        text = "Hello **World**!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("World", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_missing_matching_delimiter(self):
        """Should raise an exception if matching delimiter is missing"""
        text = "This should **raise an error ..."
        self.assertRaises(Exception, text_to_textnodes, text)

    def test_malformed_markdown(self):
        """Should raise an exception if text markdown is not formed correctly"""

        text = "**This _should not work**_"
        self.assertRaises(Exception, text_to_textnodes, text)

    def test_no_markdown(self):
        """Should return a single plain TextNode"""

        text = "This is some plain text!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is some plain text!", TextType.TEXT)], new_nodes
        )

    def test_no_text(self):
        """Should return an empty list"""

        text = ""
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([], new_nodes)


if __name__ == "__main__":
    unittest.main()
