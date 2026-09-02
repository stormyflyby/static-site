import unittest

from extract_element import extract_markdown_images, extract_markdown_links


class TestExtractElement(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![ham sandwich](dj](https://i.imgur.com/fJRU9cs.jpeg) and ![something](https://i.imgur.com/f9i94Vk.jpeg()) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and [anakin](https://i.imgur.com/Usk1Ln9.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_no_images(self):
        text = "This is ordinary text."
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_images_no_text(self):
        text = ""
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_links(self):
        text = "This is text with ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [Google](https://google.com) and [Another link](https://link.com) and []this](https://restaurant.com) and [your machine](http://localhost()"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [
                ("Google", "https://google.com"),
                ("Another link", "https://link.com"),
            ],
        )

    def test_extract_markdown_no_links(self):
        text = "This is ordinary text."
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_links_no_text(self):
        text = ""
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
