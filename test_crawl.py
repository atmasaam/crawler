import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data


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

    def test_getting_an_url(self):
        html_content = "<html><body><a href='https://crawler-test.com'>Go to Boot.dev</a><img src='/logo.png' alt='Boot.dev Logo' /></body></html>"
        base_url = "https://crawler-test.com"
        actual = get_urls_from_html(html_content, base_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_relative_urls(self):
        html_content = "<html><body><a href='/newsource'>Go to Boot.dev</a><img src='/logo.png' alt='Boot.dev Logo' /></body></html>"
        base_url = "https://crawler-test.com"
        actual = get_urls_from_html(html_content, base_url)
        expected = ["https://crawler-test.com/newsource"]
        self.assertEqual(actual, expected)

    def test_get_multiple_urls(self):
        html_content = "<html><body><a href='https://crawler-test.com'>Go to Boot.dev</a><a href='https://crawler-secondlink.com'>Go to Boot.dev</a><img src='/logo.png' alt='Boot.dev Logo' /></body></html>"
        base_url = "https://crawler-test.com"
        actual = get_urls_from_html(html_content, base_url)
        expected = ["https://crawler-test.com", "https://crawler-secondlink.com"]
        self.assertEqual(actual, expected)

    def test_get_multiple_type_urls(self):
        html_content = "<html><body><a href='/newpage'>Go to Boot.dev</a><a href='https://crawler-secondlink.com'>Go to Boot.dev</a><img src='/logo.png' alt='Boot.dev Logo' /></body></html>"
        base_url = "https://crawler-test.com"
        actual = get_urls_from_html(html_content, base_url)
        expected = ["https://crawler-test.com/newpage", "https://crawler-secondlink.com"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html(self):
        html_content = "<html><body><a href='https://crawler-secondlink.com'>Go to Boot.dev</a><img src='https://crawler-test.com/logo.png' alt='Boot.dev Logo' /></body></html>"
        base_url = "https://crawler-test.com"
        actual = get_images_from_html(html_content, base_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_norel_url(self):
        html_content = "<html><body><a href='https://crawler-secondlink.com'>Go to Boot.dev</a><img src='/logo.png' alt='Boot.dev Logo' /></body></html>"
        base_url = "https://crawler-test.com"
        actual = get_images_from_html(html_content, base_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_noattr(self):
        html_content = "<html><body><a href='https://crawler-secondlink.com'>Go to Boot.dev</a><img src='' alt='Boot.dev Logo' /></body></html>"
        base_url = "https://crawler-test.com"
        actual = get_images_from_html(html_content, base_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_extract_page_data(self):
        html_content = """  <html><body>
                            <h1>Test Title</h1>
                            <p>This is the first paragraph.</p>
                            <a href="/link1">Link 1</a>
                            <img src="/image1.jpg" alt="Image 1">
                            </body></html>
                        """
        page_url = "https://crawler-test.com"
        actual = extract_page_data(html_content, page_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_subheaders(self):
        html_content = """  <html><body>
                            <h2>Test Title</h2>
                            <p>This is the first paragraph.</p>
                            <a href="/link1">Link 1</a>
                            <img src="/image1.jpg" alt="Image 1">
                            </body></html>
                        """
        page_url = "https://crawler-test.com"
        actual = extract_page_data(html_content, page_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_externalimage(self):
            html_content = """  <html><body>
                                <h2>Test Title</h2>
                                <p>This is the first paragraph.</p>
                                <a href="/link1">Link 1</a>
                                <img src="https://boot.dev/image1.jpg" alt="Image 1">
                                </body></html>
                            """
            page_url = "https://crawler-test.com"
            actual = extract_page_data(html_content, page_url)
            expected = {
                "url": "https://crawler-test.com",
                "heading": "Test Title",
                "first_paragraph": "This is the first paragraph.",
                "outgoing_links": ["https://crawler-test.com/link1"],
                "image_urls": ["https://boot.dev/image1.jpg"]
            }
            self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
    