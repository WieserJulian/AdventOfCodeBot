import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from src.utils.text_converter import convert_url_to_day_object, getTableTitle, getTableText, getDays, getDaysTitle, getDaysText, html_to_markdown

class TestTextConverter(unittest.TestCase):

    @patch('src.utils.text_converter.requests.get')
    def test_convert_url_to_day_object_valid_url(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = '<html><title>Test Title</title><main><p>Test Text</p></main></html>'
        mock_get.return_value = mock_response

        result = convert_url_to_day_object('http://example.com', 2023)
        self.assertIsNotNone(result)
        self.assertEqual(result.title, 'Test Title')
        self.assertEqual(result.text, 'Test Text')

    @patch('src.utils.text_converter.requests.get')
    def test_convert_url_to_day_object_invalid_url(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = convert_url_to_day_object('http://example.com', 2023)
        self.assertIsNone(result)

    def test_getTableTitle_with_title(self):
        soup = BeautifulSoup('<html><title>Test Title</title></html>', 'html.parser')
        result = getTableTitle(soup)
        self.assertEqual(result, 'Test Title')

    def test_getTableTitle_without_title(self):
        soup = BeautifulSoup('<html></html>', 'html.parser')
        result = getTableTitle(soup)
        self.assertIsNone(result)

    def test_getTableText_with_text(self):
        soup = BeautifulSoup('<html><main><p>Test Text</p></main></html>', 'html.parser')
        result = getTableText(soup)
        self.assertEqual(result, 'Test Text')

    def test_getTableText_without_text(self):
        soup = BeautifulSoup('<html><main></main></html>', 'html.parser')
        result = getTableText(soup)
        self.assertIsNone(result)

    @patch('src.utils.text_converter.requests.get')
    def test_getDays_with_days(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = '<html><main><a href="/2023/day/1"><span>1</span></a></main></html>'
        mock_get.return_value = mock_response

        soup = BeautifulSoup(mock_response.content, 'html.parser')
        result = getDays(soup, 'http://example.com', 2023)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].day_id, '202301')

    def test_getDays_without_days(self):
        soup = BeautifulSoup('<html><main></main></html>', 'html.parser')
        result = getDays(soup, 'http://example.com', 2023)
        self.assertEqual(len(result), 0)

    def test_getDaysTitle_with_title(self):
        soup = BeautifulSoup('<html><main><h2>Test Title</h2></main></html>', 'html.parser')
        result = getDaysTitle(soup)
        self.assertEqual(result, 'Test Title')

    def test_getDaysTitle_without_title(self):
        soup = BeautifulSoup('<html><main></main></html>', 'html.parser')
        result = getDaysTitle(soup)
        self.assertIsNone(result)

    def test_getDaysText_with_text(self):
        soup = BeautifulSoup('<html><main><p>Test Text</p><p></p></main></html>', 'html.parser')
        result = getDaysText(soup, 'http://example.com')
        self.assertEqual(result, 'Test Text')

    def test_getDaysText_without_text(self):
        soup = BeautifulSoup('<html><main></main></html>', 'html.parser')
        result = getDaysText(soup, 'http://example.com')
        self.assertEqual(result, '')

    def test_html_to_markdown_with_anchor(self):
        tag = BeautifulSoup('<a href="/test">Test Link</a>', 'html.parser').a
        result = html_to_markdown(tag, 'http://example.com')
        self.assertEqual(result, '[Test Link](http://example.com/test)')

    def test_html_to_markdown_with_code(self):
        tag = BeautifulSoup('<code>Test Code</code>', 'html.parser').code
        result = html_to_markdown(tag)
        self.assertEqual(result, '`Test Code`')

if __name__ == '__main__':
    unittest.main()