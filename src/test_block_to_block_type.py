import unittest

from markdown_parser import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_block(self):
        """Should return heading block type for heading level of 1-6"""

        h1 = """# This is heading level one text"""
        block_type1 = block_to_block_type(h1)
        self.assertEqual(BlockType.HEADING, block_type1)

        h2 = """## This is heading level two text"""
        block_type2 = block_to_block_type(h2)
        self.assertEqual(BlockType.HEADING, block_type2)

        h4 = """#### This is heading level four text"""
        block_type3 = block_to_block_type(h4)
        self.assertEqual(BlockType.HEADING, block_type3)

        h6 = """###### This is heading level six text"""
        block_type4 = block_to_block_type(h6)
        self.assertEqual(BlockType.HEADING, block_type4)

        """Should return paragraph type for wrong heading levels or malformed headings"""

        h7 = """####### This is heading level seven text"""
        block_type5 = block_to_block_type(h7)
        self.assertEqual(BlockType.PARAGRAPH, block_type5)

        malformed_h1 = """#This is malformed heading level one text"""
        block_type6 = block_to_block_type(malformed_h1)
        self.assertEqual(BlockType.PARAGRAPH, block_type6)

    def test_code_block(self):
        """Should return code block type for code block"""

        code_html = """```
<p>Hello World!</p>
```"""
        block_type1 = block_to_block_type(code_html)
        self.assertEqual(BlockType.CODE, block_type1)

        code_python = """```
print("Hello World!")
```"""
        block_type2 = block_to_block_type(code_python)
        self.assertEqual(BlockType.CODE, block_type2)

        """Should return paragraph type for malformed code block"""

        code_malformed1 = """``
<p>This block is malformed with a missing opening backtick</p>
```"""
        block_type3 = block_to_block_type(code_malformed1)
        self.assertEqual(BlockType.PARAGRAPH, block_type3)

        code_malformed2 = """```
<p>This block is malformed with an extra closing backtick</p>
````"""
        block_type4 = block_to_block_type(code_malformed2)
        self.assertEqual(BlockType.PARAGRAPH, block_type4)

        code_malformed3 = "``` \n<p>This block has extra whitespace in opening backtick sequence</p>\n```"
        block_type5 = block_to_block_type(code_malformed3)
        self.assertEqual(BlockType.PARAGRAPH, block_type5)

    def test_quote_block(self):
        """Should return quote block type for quote block"""

        quote = """>This is a quote
> And another quote
>So help me God"""

        block_type1 = block_to_block_type(quote)
        self.assertEqual(BlockType.QUOTE, block_type1)

        """Should return paragraph type for malformed quote block"""
        quote_malformed1 = """ >This is a malformed quote
> With starting
>Whitespace"""

        block_type2 = block_to_block_type(quote_malformed1)
        self.assertEqual(BlockType.PARAGRAPH, block_type2)

        quote_malformed2 = """>This is a malformed quote
> With trailing
>Newline
"""

        block_type3 = block_to_block_type(quote_malformed2)
        self.assertEqual(BlockType.PARAGRAPH, block_type3)

        quote_malformed3 = """> This is a malformed quote
>  With two spaces after this quote
>Instead of one or zero"""

        block_type4 = block_to_block_type(quote_malformed3)
        self.assertEqual(BlockType.PARAGRAPH, block_type4)

    def test_unordered_block(self):
        """Should return unordered_list block type for unordered block"""

        ul = """- This is the first item
- This is the second item
- This is the third item"""

        block_type1 = block_to_block_type(ul)
        self.assertEqual(BlockType.UNORDERED, block_type1)

        """Should return paragraph type for malformed unordered block"""
        ul_malformed1 = """-This is a malformed list item
- This is a second item
- This is a third item"""

        block_type2 = block_to_block_type(ul_malformed1)
        self.assertEqual(BlockType.PARAGRAPH, block_type2)

        ul_malformed2 = """-   This is a malformed list item
- This is a second item
- This is a third item"""

        block_type3 = block_to_block_type(ul_malformed2)
        self.assertEqual(BlockType.PARAGRAPH, block_type3)

        ul_malformed3 = """- This is the first list item
This is the second malformed list item
- This is the third list item"""

        block_type4 = block_to_block_type(ul_malformed3)
        self.assertEqual(BlockType.PARAGRAPH, block_type4)

    def test_ordered_block(self):
        """Should return ordered_list block type for ordered block"""

        ol = """1. This is the first item
2. This is the second item
3. This is the third item"""

        block_type1 = block_to_block_type(ol)
        self.assertEqual(BlockType.ORDERED, block_type1)

        """Should return paragraph type for malformed ordered block"""
        ol_malformed1 = """1.This is a malformed list item
2. This is a second item
3. This is a third item"""

        block_type2 = block_to_block_type(ol_malformed1)
        self.assertEqual(BlockType.PARAGRAPH, block_type2)

        ol_malformed2 = """1. This is the first item
1. This is the second item
2. This is the third item"""

        block_type3 = block_to_block_type(ol_malformed2)
        self.assertEqual(BlockType.PARAGRAPH, block_type3)

        ol_malformed3 = """1. This is the first list item
2.  This is the second malformed list item
3. This is the third list item"""

        block_type4 = block_to_block_type(ol_malformed3)
        self.assertEqual(BlockType.PARAGRAPH, block_type4)


if __name__ == "__main__":
    unittest.main()
