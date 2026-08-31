import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_repr(self):
        node = LeafNode(
            "div", "This is a leaf.", {"id": "div_block", "class": "red_text"}
        )
        self.assertEqual(
            f"{node}",
            'LeafNode(div, This is a leaf., props: { id="div_block" class="red_text" })',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode("", "This has an empty tag.")
        self.assertEqual(node.to_html(), "This has an empty tag.")

    def test_leaf_to_html_no_tag_props(self):
        node = LeafNode(
            "",
            "This has an empty tag but with properties.",
            {"id": "sentence", "class": "no_tag"},
        )
        self.assertEqual(node.to_html(), "This has an empty tag but with properties.")

    def test_leaf_to_html_props(self):
        node = LeafNode(
            "span",
            "This thing has properties.",
            {"id": "span_area", "class": "red_text"},
        )
        self.assertEqual(
            node.to_html(),
            '<span id="span_area" class="red_text">This thing has properties.</span>',
        )


if __name__ == "__main__":
    unittest.main()
