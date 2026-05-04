import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):

    def test_no_children(self):
        """Should raise a ValueError that children are required"""
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag(self):
        """Should raise a ValueError that tag is required"""
        node = ParentNode(None, [LeafNode("p", "Hello, World")])
        self.assertRaises(ValueError, node.to_html)

    def test_children_leaf_only(self):
        """Should return nested list items within an unordered list"""
        children = [
            LeafNode("li", "Tomatoes"),
            LeafNode("li", "Cucumbers"),
            LeafNode("li", "Lettuce"),
        ]
        node = ParentNode("ul", children)
        self.assertEqual(
            node.to_html(),
            "<ul><li>Tomatoes</li><li>Cucumbers</li><li>Lettuce</li></ul>",
        )

    def test_children_mixed(self):
        """Should return a parent node with nested leaf and parent nodes"""
        p_children = [
            LeafNode(None, "I have "),
            LeafNode("span", "character", {"style": {"font-weight": "bold"}}),
            LeafNode(None, " and "),
            LeafNode(
                "span", "style!", {"style": {"font-style": "italic", "color": "orange"}}
            ),
        ]
        div_children = [
            LeafNode("p", "I'm regular text"),
            ParentNode("p", p_children),
        ]
        node = ParentNode("div", div_children)
        expected = '<div><p>I\'m regular text</p><p>I have <span style="font-weight:bold;">character</span> and <span style="color:orange; font-style:italic;">style!</span></p></div>'
        self.assertEqual(node.to_html(), expected)

    def test_parent_child_no_children(self):
        """Should raise a ValueError if nested parent has no children"""
        div_children = [
            LeafNode("p", "The below list is empty"),
            ParentNode("ol", None),
        ]
        node = ParentNode("div", div_children)
        self.assertRaises(ValueError, node.to_html)
