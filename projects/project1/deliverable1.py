
# Load Hugging Face Fake News Detector
MODEL_NAME = "microsoft/deberta-v3-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def is_valid_url(url):
    """Checks if URL is well-formed and not from a suspicious domain."""
    suspicious_tlds = ["xyz", "ru", "tk", "cn", "top"]
    regex = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    
    if not re.match(regex, url):
        return False
    if any(url.endswith(f".{tld}") for tld in suspicious_tlds):
        return False
    return True

def get_article_text(url):
    """Extracts article content from a given URL."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join([p.get_text() for p in paragraphs])
    except:
        return None

def get_readability_score(text):
    """Computes the Flesch-Kincaid readability score."""
    return textstat.flesch_reading_ease(text)

def check_fake_news(text):
    """Detects fake news using Hugging Face's transformer model."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs).logits
    score = torch.softmax(outputs, dim=1)[0][1].item()  # Probability of fake news
    return score  # Higher score means more likely to be fake

def calculate_relevance(query, article_text):
    """Computes cosine similarity between query and article text."""
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([query, article_text])
    similarity_score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return similarity_score

def get_moz_domain_score(url):
    """Retrieves Moz Domain Authority (DA) score. Requires Moz API key."""
    MOZ_API_URL = "https://lsapi.seomoz.com/v2/url_metrics"
    MOZ_ACCESS_ID = "your_moz_access_id"
    MOZ_SECRET_KEY = "your_moz_secret_key"
    
    try:
        response = requests.post(MOZ_API_URL, json={"targets": [url]}, auth=(MOZ_ACCESS_ID, MOZ_SECRET_KEY))
        data = response.json()
        return data["results"][0]["domain_authority"]
    except:
        return None

def rate_url_content(url, query):
    """Rates a URL and its content based on validity, relevance, trustworthiness, and readability."""
    if not is_valid_url(url):
        return {"url": url, "rating": "Invalid URL"}

    article_text = get_article_text(url)
    if not article_text:
        return {"url": url, "rating": "Content not found"}

    readability = get_readability_score(article_text)
    fake_news_score = check_fake_news(article_text)
    relevance_score = calculate_relevance(query, article_text)
    domain_trust = get_moz_domain_score(url)

    # Final Rating Calculation (Weighted)
    final_score = (
        (domain_trust if domain_trust else 0) * 0.4 +  # 40% weight
        (readability / 100) * 0.2 +  # 20% weight
        (relevance_score * 100) * 0.3 -  # 30% weight
        (fake_news_score * 100) * 0.1  # -10% weight for fake news probability
    )

    return {
        "url": url,
        "domain_trust": domain_trust,
        "readability": readability,
        "relevance_score": relevance_score,
        "fake_news_score": fake_news_score,
        "final_rating": final_score
    }
