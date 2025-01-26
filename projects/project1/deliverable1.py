

# Load Sentence Transformer model (optimized for Hugging Face deployment)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2").to(device)

# API KEYS (Replace with your own)
GOOGLE_FACT_CHECK_API_KEY = "YOUR_GOOGLE_FACT_CHECK_API_KEY"
NEWS_API_KEY = "YOUR_NEWS_API_KEY"

# Blacklist: URL Shorteners & Suspicious Keywords
shorteners = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "shorte.st"]
suspicious_keywords = ["free", "click", "win", "hack", "lottery"]

# Trusted Domains List
domain_weights = {
    "gov": 1.0, "edu": 1.0, "mil": 0.9, "int": 0.9, "org": 0.7,
    "researchgate.net": 0.8, "arxiv.org": 0.8, "sciencedirect.com": 0.9,
    "springer.com": 0.9, "nature.com": 1.0, "wikipedia.org": 0.5
}

### **🔹 Fetch Real-Time Trusted Sources**
def fetch_google_fact_check_sources():
    """Fetches latest fact-checked claims from Google Fact Check API"""
    try:
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?key={GOOGLE_FACT_CHECK_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [claim["text"] for claim in data.get("claims", [])[:5]]  # Get top 5 claims
        return []
    except Exception as e:
        print(f"Error fetching Google Fact Check claims: {e}")
        return []

def fetch_latest_news_headlines():
    """Fetches latest headlines from trusted news sources like Reuters, BBC, and AP"""
    try:
        url = f"https://newsapi.org/v2/top-headlines?sources=reuters,bbc-news,associated-press&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [article["title"] for article in data.get("articles", [])[:5]]  # Get top 5 headlines
        return []
    except Exception as e:
        print(f"Error fetching news headlines: {e}")
        return []

def fetch_wikipedia_summaries(topic="Artificial Intelligence"):
    """Fetches Wikipedia summaries for a given topic"""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [data.get("extract", "")]
        return []
    except Exception as e:
        print(f"Error fetching Wikipedia summaries: {e}")
        return []

def fetch_real_time_trusted_sources():
    """Combines multiple real-time sources"""
    sources = []
    sources.extend(fetch_google_fact_check_sources())
    sources.extend(fetch_latest_news_headlines())
    sources.extend(fetch_wikipedia_summaries())
    return sources if sources else ["No trusted sources available."]

### **🔹 Core URL Evaluation Function**
def evaluate_url_validity(url, user_prompt):
    """Evaluates a URL's credibility and checks if the content aligns with a user query."""
    try:
        # Extract domain info
        extracted = tldextract.extract(url)
        domain = f"{extracted.domain}.{extracted.suffix}"

        # Check for HTTPS
        is_https = url.startswith("https://")

        # Assign domain credibility score
        domain_score = next((domain_weights[d] for d in domain_weights if domain.endswith(d)), 0.5)

        # Check for suspicious patterns
        is_shortened = any(shortener in url for shortener in shorteners)
        has_suspicious_keywords = any(kw in url.lower() for kw in suspicious_keywords)

        # Fetch webpage content
        text_content = fetch_url_text(url)
        if text_content.startswith("Error:"):
            return 0, f"Error: Could not fetch webpage content ({text_content})"

        # Compare content similarity with trusted sources
        fact_check_similarity = analyze_content_similarity(text_content)

        # Compare article content with user query
        user_query_similarity = analyze_query_similarity(user_prompt, text_content)

        # Compute final score
        final_score = compute_final_score(
            is_https, domain_score, is_shortened, has_suspicious_keywords, fact_check_similarity, user_query_similarity
        )

        # Generate explanation
        explanation = generate_explanation(
            is_https, domain, is_shortened, has_suspicious_keywords, fact_check_similarity, user_query_similarity
        )

        return final_score, explanation

    except Exception as e:
        return 0, f"Error processing URL: {str(e)}"

### **🔹 Fetch Webpage Content (Using `newspaper3k`)**
def fetch_url_text(url):
    """Fetches and extracts text from a news article using newspaper3k."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text if article.text else "Error: No article content found."
    except Exception as e:
        return f"Error: {str(e)}"

### **🔹 Compare Webpage Content with Trusted Sources**
def analyze_content_similarity(text):
    """Compares webpage content with real-time trusted sources."""
    trusted_sources = fetch_real_time_trusted_sources()

    text_embedding = model.encode(text, convert_to_tensor=True)
    source_embeddings = model.encode(trusted_sources, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(text_embedding, source_embeddings)
    return similarities.max().item()  # Highest match

### **🔹 Compare User Prompt with Webpage Content**
def analyze_query_similarity(user_query, text):
    """Compares the user question/query with the webpage content to check relevance."""
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    text_embedding = model.encode(text, convert_to_tensor=True)

    similarity = util.pytorch_cos_sim(query_embedding, text_embedding).item()
    return similarity  # Between 0 and 1

### **🔹 Compute Final Credibility Score**
def compute_final_score(is_https, domain_score, is_shortened, has_suspicious_keywords, fact_check_similarity, user_query_similarity):
    """Computes final credibility score based on multiple factors."""
    score = domain_score
    if not is_https:
        score -= 0.2
    if is_shortened:
        score -= 0.4
    if has_suspicious_keywords:
        score -= 0.3

    # Combine fact-checking similarity & user query similarity
    score = (score + fact_check_similarity + user_query_similarity) / 3  # Weighted average

    return max(0, min(1, score))  # Ensure score is within [0,1] range

### **🔹 Generate Explanation**
def generate_explanation(is_https, domain, is_shortened, has_suspicious_keywords, fact_check_similarity, user_query_similarity):
    """Generates a readable explanation for the credibility score."""
    explanations = []
    explanations.append("✅ HTTPS Enabled" if is_https else "⚠️ Not using HTTPS (less secure)")
    explanations.append(f"🔎 Domain: {domain} - {domain_weights.get(domain, 'Moderately reliable')}")
    if is_shortened:
        explanations.append("❌ URL is shortened, hiding destination.")
    if has_suspicious_keywords:
        explanations.append("⚠️ Contains scam-like keywords.")

    explanations.append(f"📊 Content similarity to verified sources: {round(fact_check_similarity, 2)}")
    explanations.append(f"📝 Similarity to user query: {round(user_query_similarity, 2)}")

    return " ".join(explanations)

### **🔹 Example Usage**
test_url = "https://www.nytimes.com/2025/02/01/us/philadelphia-plane-crash.html"
user_prompt = "Did a plane crash happen in Philadelphia?"
score, explanation = evaluate_url_validity(test_url, user_prompt)
print(f"Score: {score}\nExplanation: {explanation}")
