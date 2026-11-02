"""Consistent editorial body extraction, excluding page furniture."""
from hashlib import sha256
from html import unescape
import re

def article_fragment(document):
    match = re.search(r'<article\b[^>]*class="[^"]*\barticle\b[^"]*"[^>]*>(.*?)</article>', document, re.I | re.S)
    if not match:
        raise ValueError('Article body missing')
    return match.group(1)

def review_content(document):
    content = article_fragment(document)
    return re.sub(r'<(header|aside|nav)\b[^>]*>.*?</\1>', '', content, flags=re.I | re.S)

def review_fingerprint(document):
    # Includes source links and their scope, but ignores shared site chrome.
    return sha256(review_content(document).encode()).hexdigest()

def body_text(document):
    content = review_content(document)
    content = re.sub(r'<section\b[^>]*class="(?:sources|related|key-takeaways|article-toc)"[^>]*>.*?</section>', '', content, flags=re.I | re.S)
    content = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', content, flags=re.I | re.S)
    return ' '.join(unescape(re.sub(r'<[^>]*>', ' ', content)).split())

def body_word_count(document):
    return len(re.findall(r"\b[\w’'-]+\b", body_text(document)))
