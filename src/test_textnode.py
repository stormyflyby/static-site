import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("These are", TextType.CODE_TEXT)
        node2 = TextNode("Not equal", TextType.CODE_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Another text node", TextType.LINK)
        node2 = TextNode("Another text node", TextType.LINK, "https://url.com")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Yet another", TextType.LINK, "https://cool.yeah")
        node2 = TextNode("Yet another", TextType.LINK, "https://cool.yeah")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("String test time", TextType.ITALIC_TEXT)
        self.assertEqual(f"{node}", "TextNode(String test time, italic_text, None)")

    def test_repr_url(self):
        node = TextNode(
            "String test with url", TextType.IMAGE, "https://image.com/image.jpg"
        )
        self.assertEqual(
            f"{node}",
            "TextNode(String test with url, image, https://image.com/image.jpg)",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://google.com")

    def test_image(self):
        node = TextNode(
            "This is an image node", TextType.IMAGE, "https://site.com/image.jpg"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://site.com/image.jpg")
        self.assertEqual(html_node.props["alt"], "This is an image node")

    def test_link_no_url(self):
        node = TextNode("This node needs a URL", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_no_url(self):
        node = TextNode("This node needs a URL", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
