import unittest

from extract_title import extract_title


class TestExtactTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts"""
        title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")

    def test_extract_title_end(self):
        md = """
## Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

#      Blog posts
# Second title"""
        title = extract_title(md)
        self.assertEqual(title, "Blog posts")

    def test_extract_title_no_title(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien"""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_empty(self):
        md = ""
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
