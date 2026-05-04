import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_init(self):
        """Should render a HTMLNode correctly when initialized"""
        node = HTMLNode("h1", "Hello World!")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Hello World!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html_with_props(self):
        """Should return a properly formatted attribute string from the props provided"""
        node = HTMLNode(
            tag="a",
            value="Google",
            props={"href": "https://google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://google.com" target="_blank"'
        )

    def test_props_to_html_no_props(self):
        """Should return an empty attribute string when no props are provided"""
        node = HTMLNode(tag="p", value="The quick brown fox jumps over the lazy dog")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_style(self):
        """Should render inline CSS correctly"""
        node = HTMLNode(
            "p",
            "I am bold and beautiful",
            props={"style": {"color": "pink", "font-weight": "bold"}},
        )
        expected = f' style="color:pink; font-weight:bold;"'
        self.assertEqual(node.props_to_html(), expected)

    def test_raise_not_implemented(self):
        """Should raise a NotImplementedError when called directly on an HTMLNode"""
        node = HTMLNode(value="This will raise an error in a bit")
        self.assertRaises(NotImplementedError, node.to_html)
