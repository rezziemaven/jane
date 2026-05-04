import unittest

from textnode import TextType, TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):

    def test_init(self):
        node = TextNode("Hello World", TextType.TEXT, "https://mysite.dev")
        self.assertEqual(node.text, "Hello World")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertEqual(node.url, "https://mysite.dev")

    def test_url_none(self):
        node = TextNode("This node has no url", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_text(self):
        """Should render text as a plain string"""
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_html_bold(self):
        """Should render bold text in a <b> tag"""
        node = TextNode("This is some bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is some bold text</b>")

    def test_html_italic(self):
        """Should render italic text in a <i> tag"""
        node = TextNode("This is some italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is some italic text</i>")

    def test_html_code(self):
        """Should render code text in a <code> tag"""
        node = TextNode("<p>Hello, World!</p>", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code><p>Hello, World!</p></code>")

    def test_html_link(self):
        """Should render text as a link"""
        node = TextNode(
            "Jane Austen: A Life", TextType.LINK, "https://janeaustens.house"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://janeaustens.house">Jane Austen: A Life</a>',
        )

    def test_html_link(self):
        """Should render an image with alt text"""
        node = TextNode("My House", TextType.IMAGE, "/jane-austen-house.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.to_html(),
            '<img alt="My House" src="/jane-austen-house.jpg">',
        )


if __name__ == "__main__":
    unittest.main()
