import unittest

from splitnodes import split_nodes_delimiter
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


if __name__ == "__main__":
    unittest.main()
