import unittest

from markdown_parser import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_split_single_block(self):
        """Should split a simple block of text into a single block"""

        md = """This is a block of text."""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(["This is a block of text."], blocks)

    def test_split_markdown_blocks(self):
        """Should split blocks of text into markdown blocks"""

        md = """This is a **bolded** paragraph.

This is another paragraph with _italic_ text and `code` here.
This is the same paragraph on a new line.

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "This is a **bolded** paragraph.",
                "This is another paragraph with _italic_ text and `code` here.\nThis is the same paragraph on a new line.",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def strip_empty_newlines(self):
        """Should remove any empty newlines from the list of blocks"""

        md = """# This is a heading



This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
- This is another list item
- This is a third list item

"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a another list item\n- This is a third list item",
            ]
        )

    def test_no_markdown(self):
        """Should return an empty list if there is no markdown"""

        md = ""
        blocks = markdown_to_blocks(md)

        self.assertListEqual([], blocks)


if __name__ == "__main__":
    unittest.main()
