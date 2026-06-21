"""Text cleaning + TF-IDF feature extraction.

Upgraded per supervisor feedback (Week 3): adds Unicode NFKC normalization and a
phone-number token, alongside HTML stripping and URL/email tokenization.
"""
import re
import unicodedata
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
PHONE_RE = re.compile(r"(?:\+?\d[\d\-\(\)\s]{7,}\d)")
NON_ALPHA_RE = re.compile(r"[^a-z\s]")
WS_RE = re.compile(r"\s+")

DEFAULT_BOILERPLATE = {"from", "to", "cc", "subject", "sent", "re", "fwd"}


def clean_text(text, url_token="urltoken", email_token="emailtoken", phone_token="phonetoken"):
    """Lowercase, NFKC-normalize, strip HTML, tokenize URL/email/phone, normalize."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text)          # Unicode normalization
    text = text.lower()
    text = BeautifulSoup(text, "html.parser").get_text(" ")  # strip HTML
    text = URL_RE.sub(f" {url_token} ", text)
    text = EMAIL_RE.sub(f" {email_token} ", text)
    text = PHONE_RE.sub(f" {phone_token} ", text)
    text = NON_ALPHA_RE.sub(" ", text)                  # normalize special chars
    text = WS_RE.sub(" ", text).strip()                 # normalize whitespace
    return text


def combine_fields(df, fields=("subject", "body")):
    parts = [df[f].fillna("").astype(str) for f in fields if f in df.columns]
    out = parts[0]
    for p in parts[1:]:
        out = out + " " + p
    return out


def build_vectorizer(ngram_range=(1, 2), max_features=20000,
                     sublinear_tf=True, min_df=2, extra_stop_words=None):
    stop = list(ENGLISH_STOP_WORDS | set(extra_stop_words or []) | DEFAULT_BOILERPLATE)
    return TfidfVectorizer(ngram_range=tuple(ngram_range), max_features=max_features,
                           sublinear_tf=sublinear_tf, min_df=min_df, stop_words=stop)
