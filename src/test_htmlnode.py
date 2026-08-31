import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://google.com" target="_blank"'
        )

    def test_repr(self):
        child_node1 = HTMLNode()
        child_node2 = HTMLNode()
        children = [child_node1, child_node2]
        props = {"id": "node_with_children"}
        node = HTMLNode("i", "This is an HTML node", children, props)
        self.assertEqual(
            f"{node}",
            f'HTMLNode(i, This is an HTML node, [{child_node1}, {child_node2}], props: {{ id="node_with_children" }})',
        )

    def test_repr_empty(self):
        node = HTMLNode()
        self.assertEqual(f"{node}", "HTMLNode(None, None, None, props: { })")

    def test_to_html(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
