import unittest

from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode(
            "This is a node with a `code` block in it.", TextType.PLAIN_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected_text = ["This is a node with a ", "code", " block in it."]
        expected_types = [TextType.PLAIN_TEXT, TextType.CODE_TEXT, TextType.PLAIN_TEXT]
        self.assertEqual(len(new_nodes), 3)
        for i in range(3):
            self.assertEqual(new_nodes[i].text_type, expected_types[i])
            self.assertEqual(new_nodes[i].text, expected_text[i])

    def test_split_nodes_delimiter_at_beginning(self):
        node = TextNode("**Bold text** is amazing.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected_text = ["Bold text", " is amazing."]
        expected_types = [TextType.BOLD_TEXT, TextType.PLAIN_TEXT]
        self.assertEqual(len(new_nodes), 2)
        for i in range(2):
            self.assertEqual(new_nodes[i].text_type, expected_types[i])
            self.assertEqual(new_nodes[i].text, expected_text[i])

    def test_split_nodes_delimiter_at_end(self):
        node = TextNode("Bring on the _italic text._", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        expected_text = ["Bring on the ", "italic text."]
        expected_types = [TextType.PLAIN_TEXT, TextType.ITALIC_TEXT]
        self.assertEqual(len(new_nodes), 2)
        for i in range(2):
            self.assertEqual(new_nodes[i].text_type, expected_types[i])
            self.assertEqual(new_nodes[i].text, expected_text[i])

    def test_split_nodes_url(self):
        node = TextNode("Bring on the _italic text._", TextType.PLAIN_TEXT)
        url_node = TextNode("Google", TextType.LINK, "https://google.com")
        new_nodes = split_nodes_delimiter([node, url_node], "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Bring on the ", TextType.PLAIN_TEXT),
                TextNode("italic text.", TextType.ITALIC_TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
            ],
        )

    def test_repeated_split_nodes(self):
        node = TextNode(
            "**Bold** and _italic_ are **bo**_th_ together _in here._",
            TextType.PLAIN_TEXT,
        )
        bold_separated = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(bold_separated, "_", TextType.ITALIC_TEXT)
        expected_text = [
            "Bold",
            " and ",
            "italic",
            " are ",
            "bo",
            "th",
            " together ",
            "in here.",
        ]
        expected_types = [
            TextType.BOLD_TEXT,
            TextType.PLAIN_TEXT,
            TextType.ITALIC_TEXT,
            TextType.PLAIN_TEXT,
            TextType.BOLD_TEXT,
            TextType.ITALIC_TEXT,
            TextType.PLAIN_TEXT,
            TextType.ITALIC_TEXT,
        ]
        self.assertEqual(len(new_nodes), 8)
        for i in range(8):
            self.assertEqual(new_nodes[i].text_type, expected_types[i])
            self.assertEqual(new_nodes[i].text, expected_text[i])

    def test_split_nodes_empty_delimiter(self):
        node = TextNode("There is some **bold** text here.", TextType.PLAIN_TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "", TextType.BOLD_TEXT)

    def test_split_nodes_missing_closing_delimiter(self):
        node = TextNode("_Lots_ and _lots_ of _italic text.", TextType.PLAIN_TEXT)
        with self.assertRaises(SyntaxError):
            split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)

    def test_split_nodes_no_delimiter_appearance(self):
        node = TextNode("Where are the delimiters?", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[0].text, "Where are the delimiters?")

    def test_split_nodes_no_text_nodes(self):
        self.assertEqual(len(split_nodes_delimiter([], "_", TextType.ITALIC_TEXT)), 0)

    def test_split_image(self):
        node = TextNode(
            "There are ![two](images) and [one](link) sitting around ![in](here)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("There are ", TextType.PLAIN_TEXT),
                TextNode("two", TextType.IMAGE, "images"),
                TextNode(" and [one](link) sitting around ", TextType.PLAIN_TEXT),
                TextNode("in", TextType.IMAGE, "here"),
            ],
        )

    def test_split_image_at_beginning(self):
        node = TextNode(
            "![There is an image](at the start) of ![thi(s)]([string]), ![you]](see)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("There is an image", TextType.IMAGE, "at the start"),
                TextNode(" of ", TextType.PLAIN_TEXT),
                TextNode("thi(s)", TextType.IMAGE, "[string]"),
                TextNode(", ![you]](see)", TextType.PLAIN_TEXT),
            ],
        )

    def test_split_image_dup(self):
        node = TextNode(
            "What? ![Two](images), the same ![Two](images) are here.",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("What? ", TextType.PLAIN_TEXT),
                TextNode("Two", TextType.IMAGE, "images"),
                TextNode(", the same ", TextType.PLAIN_TEXT),
                TextNode("Two", TextType.IMAGE, "images"),
                TextNode(" are here.", TextType.PLAIN_TEXT),
            ],
        )

    def test_split_image_url(self):
        node = TextNode("Gimme the ![good](stuff)", TextType.PLAIN_TEXT)
        url_node = TextNode("Google", TextType.LINK, "https://google.com")
        new_nodes = split_nodes_image([node, url_node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Gimme the ", TextType.PLAIN_TEXT),
                TextNode("good", TextType.IMAGE, "stuff"),
                TextNode("Google", TextType.LINK, "https://google.com"),
            ],
        )

    def test_split_no_image(self):
        node = TextNode("Nothing special here", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes, [TextNode("Nothing special here", TextType.PLAIN_TEXT)]
        )

    def test_split_image_no_nodes(self):
        self.assertListEqual(split_nodes_image([]), [])

    def test_split_link(self):
        node = TextNode(
            "There are [two](links) and ![one](image) sitting around [in](here)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("There are ", TextType.PLAIN_TEXT),
                TextNode("two", TextType.LINK, "links"),
                TextNode(" and ![one](image) sitting around ", TextType.PLAIN_TEXT),
                TextNode("in", TextType.LINK, "here"),
            ],
        )

    def test_split_link_at_beginning(self):
        node = TextNode(
            "[There is a link](at the start) of [thi(s)]([string]), [you]](see)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("There is a link", TextType.LINK, "at the start"),
                TextNode(" of ", TextType.PLAIN_TEXT),
                TextNode("thi(s)", TextType.LINK, "[string]"),
                TextNode(", [you]](see)", TextType.PLAIN_TEXT),
            ],
        )

    def test_split_link_dup(self):
        node = TextNode(
            "What? [Two](links), the same [Two](links) are here.",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("What? ", TextType.PLAIN_TEXT),
                TextNode("Two", TextType.LINK, "links"),
                TextNode(", the same ", TextType.PLAIN_TEXT),
                TextNode("Two", TextType.LINK, "links"),
                TextNode(" are here.", TextType.PLAIN_TEXT),
            ],
        )

    def test_split_link_url(self):
        node = TextNode("Gimme the [good](stuff)", TextType.PLAIN_TEXT)
        url_node = TextNode("Google", TextType.LINK, "https://google.com")
        new_nodes = split_nodes_link([node, url_node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Gimme the ", TextType.PLAIN_TEXT),
                TextNode("good", TextType.LINK, "stuff"),
                TextNode("Google", TextType.LINK, "https://google.com"),
            ],
        )

    def test_split_no_link(self):
        node = TextNode("Nothing special here", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes, [TextNode("Nothing special here", TextType.PLAIN_TEXT)]
        )

    def test_split_link_no_nodes(self):
        self.assertListEqual(split_nodes_link([]), [])


if __name__ == "__main__":
    unittest.main()
