"""Regression checks for the false article-length/review-completeness result."""
import unittest
from article_content import body_word_count, review_fingerprint

PAGE = '''<nav>outside words</nav><article class="article">
<header><h1>Title words</h1><p>Description words</p></header>
<aside><nav>sidebar words</nav></aside><div class="article-prose">
<section class="key-takeaways"><p>summary words</p></section>
<section><h2>A heading</h2><p>Four useful body words.</p></section>
<section class="sources"><p>reference words</p><a href="https://example.com/a">source</a></section>
</div></article><footer>footer words</footer>'''

class ArticleContentTests(unittest.TestCase):
    def test_counts_only_body(self):
        self.assertEqual(body_word_count(PAGE), 6)

    def test_more_furniture_does_not_inflate_count(self):
        self.assertEqual(body_word_count(PAGE.replace('sidebar words', 'padding ' * 2000)), 6)

    def test_source_or_body_changes_invalidate_review(self):
        for before, after in [('useful', 'unsupported'), ('example.com/a', 'example.com/b')]:
            self.assertNotEqual(review_fingerprint(PAGE), review_fingerprint(PAGE.replace(before, after)))

    def test_header_changes_do_not_invalidate_body_review(self):
        self.assertEqual(review_fingerprint(PAGE), review_fingerprint(PAGE.replace('Title words', 'New title')))

if __name__ == '__main__':
    unittest.main()
