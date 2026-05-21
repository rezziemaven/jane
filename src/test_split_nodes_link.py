import unittest

from textnode import TextType, TextNode
from markdown_parser import split_nodes_link


class TestSplitNodesLink(unittest.TestCase):

    def test_split_link(self):
        """Should split one link from text"""
        node = TextNode(
            "This is text with [one simple link](https://one-simple-link.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode(
                    "one simple link",
                    TextType.LINK,
                    "https://one-simple-link.com",
                ),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        """Should split multiple links from text"""
        node = TextNode(
            "This is text with a [link](https://first-link.com) and [another link](https://www.second-link.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://first-link.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://www.second-link.org"),
            ],
            new_nodes,
        )

    def test_no_links(self):
        """Should leave text whole if there are no links to split"""

        node = TextNode("This string has no links to split", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This string has no links to split", TextType.TEXT)], new_nodes
        )

    def test_split_link_at_start_or_end(self):
        """Should split links at start or end of text"""
        node = TextNode(
            "[Here's a link](https://opening-link.com) at the start and a link [at the end](https://closing-link.com)!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here's a link", TextType.LINK, "https://opening-link.com"),
                TextNode(" at the start and a link ", TextType.TEXT),
                TextNode(
                    "at the end",
                    TextType.LINK,
                    "https://closing-link.com",
                ),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_adjacent_links(self):
        """Should split adjacent links"""
        node = TextNode(
            "Here are some links you might be interested in: [link one](https://link-one.com)[link two](https://link-two.net)[link three](https://link-three.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "Here are some links you might be interested in: ", TextType.TEXT
                ),
                TextNode(
                    "link one",
                    TextType.LINK,
                    "https://link-one.com",
                ),
                TextNode(
                    "link two",
                    TextType.LINK,
                    "https://link-two.net",
                ),
                TextNode(
                    "link three",
                    TextType.LINK,
                    "https://link-three.org",
                ),
            ],
            new_nodes,
        )

    def malformed_link_markdown(self):
        """Should ignore malformed link markdown and render as text"""
        node1 = TextNode(
            "This has a link with missing anchor text ![](/missing-anchor-text.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This has a link with [missing url]()",
            TextType.TEXT,
        )
        node3 = TextNode(
            "This has a link with [missing](/closing-parenthesis",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode(
                    "This has a link with missing anchor text ![](/missing-anchor-text.com)",
                    TextType.TEXT,
                ),
                TextNode(
                    "This has a link with ![missing url]()",
                    TextType.TEXT,
                ),
                TextNode(
                    "This has a link with [missing](/closing-parenthesis",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_ignore_non_links(self):
        """Should not split images or delimiters from text"""
        node = TextNode(
            "This is text with an ![image of trees](https://i.imgur.com/U2LJarL.jpeg) **and** a [random link](https://google.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ![image of trees](https://i.imgur.com/U2LJarL.jpeg) **and** a ",
                    TextType.TEXT,
                ),
                TextNode("random link", TextType.LINK, "https://google.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
