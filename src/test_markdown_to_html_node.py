import unittest

from markdown_parser import markdown_to_html_node

# from htmlnode import ParentNode


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraphs(self):
        """Should return a single div with paragraph elements"""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        """Should return a div with a child pre element that contains a code element with the text unaltered"""
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
>This is a quote.
> This is another quote _with italics_!
> This is a third quote...
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote. This is another quote <i>with italics</i>! This is a third quote...</blockquote></div>",
        )

    def test_heading(self):
        md = """
# This is the main heading

## This is a subheading **with bolded text!**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is the main heading</h1><h2>This is a subheading <b>with bolded text!</b></h2></div>",
        )

    def test_unordered_block(self):
        """Should return a div with a ul element with li items"""
        md = """
- This is a list item
- This is another list item
- This is a third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list item</li><li>This is another list item</li><li>This is a third item</li></ul></div>",
        )

    def test_ordered_block(self):
        """Should return a div with an ol element with li items"""
        md = """
1. This is a list item
2. This is another list item
3. This is a third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list item</li><li>This is another list item</li><li>This is a third item</li></ol></div>",
        )

    def test_mixed_blocks(self):
        """Should return a div with a mix different elements inside"""
        md = """
# This is a heading

This is a **bolded** paragraph.

This is another paragraph with _italic_ text and `code` here.
This is the same paragraph on a new line.

- This is a list
- with items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is a <b>bolded</b> paragraph.</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here. This is the same paragraph on a new line.</p><ul><li>This is a list</li><li>with items</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()
