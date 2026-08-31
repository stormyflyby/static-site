import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
