import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = ["free", "win", "winner", "prize", "congratulations", "click here", "exclusive", "act now",
    "risk-free", "limited time", "urgent", "offer", "money-back", "guarantee", "100% free",
    "you’ve been selected", "no cost", "special promotion", "cash bonus", "this won’t last",
    "order now", "easy money", "get paid", "lowest price", "work from home", "be your own boss",
    "financial freedom", "cheap", "save big", "call now", "extra income", "hidden charges",
    "investment", "no strings attached", "instant", "double your income", "pre-approved",
    "no obligation", "why pay more?", "unsecured", "access now", "zero cost", "lose weight fast",
    "miracle", "cure", "viagra", "buy now", "hot deal", "great offer", "act immediately"]
KNOWN_SENDERS = ["no-reply@google.com", "notifications@github.com", "newsletter@nytimes.com", "no-reply@accounts.spotify.com", "info@linkedin.com", "updates@medium.com", "no-reply@apple.com", "security@facebookmail.com", "orders@amazon.com", "support@microsoft.com", "chefe234@gmail.com", "eduardocarlos345674@gmail.com"]

def extract_links(text):
    return re.findall(r"http[s]?://\S+", text)

def is_malicious_link(url):
    parsed = urlparse(url)
    score = 0
    if re.search(r"\d{1,3}(\.\d{1,3}){3}", parsed.netloc):  # IP-based URL
        score += 2
    if "@" in url or "%" in url:
        score += 1
    if parsed.scheme == "http":
        score += 1
    if url.count('.') > 3:
        score += 1
    if any(tld in parsed.netloc for tld in [".tk", ".xyz", ".top", ".cn"]):
        score += 2
    return score

def extract_features(email_text, sender):
    email_text = email_text.lower()
    num_suspicious_words = sum(word in email_text for word in SUSPICIOUS_WORDS)
    
    urls = extract_links(email_text)
    num_links = len(urls)
    malicious_score = sum(is_malicious_link(url) for url in urls)
    
    unknown_sender = 0 if sender in KNOWN_SENDERS else 1

    return [num_suspicious_words, num_links, unknown_sender, malicious_score]