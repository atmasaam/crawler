import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_already_normalized(self):
        input_url = "www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_another_subdomain(self):
        input_url = "https://apps.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "apps.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_file_in_domain(self):
        input_url = "https://www.boot.dev/blog/path.html"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path.html"
        self.assertEqual(actual, expected)

    def test_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normal_http(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_h1_tag(self):
        html_string = "<h1>Test</h1>"
        actual = get_heading_from_html(html_string)
        expected = "Test"
        self.assertEqual(actual, expected)

    def test_h2_with_h1(self):
        html_string = "<h1>Test</h1><h2>Not</h2>"
        actual = get_heading_from_html(html_string)
        expected = "Test"
        self.assertEqual(actual, expected)
    
    def test_h2_only(self):
        html_string = "<h2>Not</h2>"
        actual = get_heading_from_html(html_string)
        expected = "Not"
        self.assertEqual(actual, expected)

    def test_empty(self):
        html_string = "<p> Hello World! </p>"
        actual = get_heading_from_html(html_string)
        expected = ""
        self.assertEqual(actual, expected)
    
    def test_paragraph(self):
        html_string = "<html><body><h1>Hello World</h1> <p>This is a paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(html_string)
        expected = "This is a paragraph."
        self.assertEqual(actual, expected)

    def test_no_paragraph(self):
        html_string = "<html><body><h1>Hello World</h1> <div>This is a paragraph.</div></body></html>"
        actual = get_first_paragraph_from_html(html_string)
        expected = ""
        self.assertEqual(actual, expected)

    def test_more_paragraphs(self):
        html_string = "<html><body><h1>Hello World</h1><p>This is the first paragraph.</p> <p>This is the second paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(html_string)
        expected = "This is the first paragraph."
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
    