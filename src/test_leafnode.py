import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_init(self):
        node = LeafNode("h1", value="Hello World!")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Hello World!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Google", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Google</a>')

    def test_leaf_to_html_text(self):
        node = LeafNode(None, "This is some plain text")
        self.assertEqual(node.to_html(), "This is some plain text")
