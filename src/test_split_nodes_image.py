import unittest

from textnode import TextType, TextNode
from markdown_parser import split_nodes_image


class TestSplitNodesImage(unittest.TestCase):

    def test_split_image(self):
        """Should split one image from text"""
        node = TextNode(
            "This is text with ![one simple image](https://i.imgur.com/zjjcJKZ.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode(
                    "one simple image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        """Should split multiple images from text"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_images(self):
        """Should leave text whole if there are no images to split"""

        node = TextNode("This string has no images to split", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This string has no images to split", TextType.TEXT)], new_nodes
        )

    def test_split_image_at_start_or_end(self):
        """Should split images at start or end of text"""
        node = TextNode(
            "![An image](https://i.imgur.com/ngMyRTg.jpeg) a day keeps the ![imgur mafia away](https://i.imgur.com/8p2WElK.jpeg).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "An image", TextType.IMAGE, "https://i.imgur.com/ngMyRTg.jpeg"
                ),
                TextNode(" a day keeps the ", TextType.TEXT),
                TextNode(
                    "imgur mafia away",
                    TextType.IMAGE,
                    "https://i.imgur.com/8p2WElK.jpeg",
                ),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_adjacent_images(self):
        """Should split adjacent images"""
        node = TextNode(
            "Here are some cat images you might like: ![image one](https://i.imgur.com/OJxQr7d.jpeg)![image two](https://i.imgur.com/0fRPKcs.png)![image three](https://i.imgur.com/nb3O889.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here are some cat images you might like: ", TextType.TEXT),
                TextNode(
                    "image one",
                    TextType.IMAGE,
                    "https://i.imgur.com/OJxQr7d.jpeg",
                ),
                TextNode(
                    "image two",
                    TextType.IMAGE,
                    "https://i.imgur.com/0fRPKcs.png",
                ),
                TextNode(
                    "image three",
                    TextType.IMAGE,
                    "https://i.imgur.com/nb3O889.jpeg",
                ),
            ],
            new_nodes,
        )

    def malformed_image_markdown(self):
        """Should ignore malformed image markdown and render as text"""
        node1 = TextNode(
            "This is text with an image with missing alt text ![](/missing-alt-text.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with an image with ![missing url]()",
            TextType.TEXT,
        )
        node3 = TextNode(
            "This is text with an image with ![missing](/closing-parenthesis",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an image with missing alt text ![](/missing-alt-text.png)",
                    TextType.TEXT,
                ),
                TextNode(
                    "This is text with an image with ![missing url]()",
                    TextType.TEXT,
                ),
                TextNode(
                    "This is text with an image with ![missing](/closing-parenthesis",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_ignore_non_images(self):
        """Should not split links or delimiters from text"""
        node = TextNode(
            "This is text with an ![image of trees](https://i.imgur.com/U2LJarL.jpeg) **and** a [random link](https://google.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image of trees", TextType.IMAGE, "https://i.imgur.com/U2LJarL.jpeg"
                ),
                TextNode(
                    " **and** a [random link](https://google.com).", TextType.TEXT
                ),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
