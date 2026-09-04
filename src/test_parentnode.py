import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode("i", [child_node], {"class": "green_text"})
        self.assertEqual(
            f"{parent_node}",
            'ParentNode(i, [LeafNode(b, child, props: { })], props: { class="green_text" })',
        )

    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("div", "child2")
        parent_node = ParentNode("head", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), "<head><span>child1</span><div>child2</div></head>"
        )

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("body", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("b", "This is a child.")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_properties(self):
        child_node = LeafNode("i", "This is a child.")
        parent_node = ParentNode(
            "div", [child_node], {"id": "parent", "class": "orange_text"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div id="parent" class="orange_text"><i>This is a child.</i></div>',
        )

    def test_to_html_child_with_properties(self):
        child_node = LeafNode("i", "This is a child.", {"id": "child"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), '<div><i id="child">This is a child.</i></div>'
        )

    def test_to_html_child_with_no_tag(self):
        child_node = LeafNode("", "This has no tag")
        parent_node = ParentNode("b", [child_node])
        self.assertEqual(parent_node.to_html(), "<b>This has no tag</b>")

    def test_to_html_child_with_no_value(self):
        child_node = LeafNode("span", None)
        parent_node = ParentNode("button", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()
