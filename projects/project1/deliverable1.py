

# Load Sentence Transformer Model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2").to(device)

# API Key for Google Fact Check (Replace with your own)
GOOGLE_FACT_CHECK_API_KEY = "YOUR_GOOGLE_FACT_CHECK_API_KEY"

# Trusted domains for different categories
trusted_domain_categories = {
    "travel": ["tsa.gov", "faa.gov", "iata.org", "nyc.gov", "transportation.gov"],
    "health": ["cdc.gov", "who.int", "nih.gov", "fda.gov"],
    "finance": ["federalreserve.gov", "sec.gov", "imf.org"],
    "science": ["nasa.gov", "mit.edu", "nature.com"],
}

### **🔹 Step 1: Identify Relevant Category Based on User Prompt**
def detect_category(user_prompt):
    """Dynamically assigns a category based on the user's question."""
    keyword_map = {
        "travel": ["airport", "flight", "airline", "visa", "trip"],
        "health": ["disease", "covid", "medicine", "symptoms", "treatment"],
        "finance": ["se", "nasa", "technology", "physics", "climate"],
    }

    for category, keywords in keyword_map.items():
        if any(keyword in user_prompt.lower() for keyword in keywords):
            return category
    return "general"

### **🔹 Step 2: Check Domain Credibility Based on Category**
def check_domain_credibility(url, category):
    """Rates a domain's credibility dynamically based on its category."""
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"

    trusted_domains = trusted_domain_categories.get(category, [])
    
    if domain in trusted_domains:
        return 1.0, f"✅ Highly credible source: {domain}"
    elif "travel" in domain or "leisure" in domain:
        return 0.6, f"⚠️ Source is a travel site ({domain}), may not be fully authoritative."
    else:
        return 0.3, f"❌ Unverified source: {domain}, cross-check with official sources."

### **🔹 Step 3: Fetch Article Content Dynamically**
def fetch_url_text(url):
    """Fetches and extracts text from a given URL using BeautifulSoup."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Error fetching page."

        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except requests.exceptions.RequestException:
        return "Error fetching page."

### **🔹 Step 4: Generate Dynamic Trusted Reference Texts**
def get_dynamic_trusted_sources(category):
    """Returns dynamically selected reference text for similarity comparison."""
    reference_texts = {
        "travel": [
            "The TSA and FAA regulate air travel and airport security.",
            "JFK, LaGuardia, and Newark are the main airports serving NYC.",
            "Official NYC airport website provides information on best airport choices.",
        ],
        "health": [
            "The CDC and WHO provide guidelines on disease prevention.",
            "COVID-19 vaccines have been approved by the FDA.",
            "Medical research from NIH supports evidence-based treatments.",
        ],
        "finance": [
            "The Federal Reserve regulates monetary policy in the U.S.",
            "Investment markets are monitored by the SEC and IMF.",
            "The IRS provides guidelines on tax regulations.",
        ],
        "science": [
            "NASA conducts space exploration and scientific research.",
            "Climate change research is supported by MIT and NOAA.",
            "AI advancements are published in Nature and Science journals.",
        ],
    }
    return reference_texts.get(category, ["No reference texts available for this category."])

### **🔹 Step 5: Compare Against Trusted Sources**
def compare_text_similarity(input_text, reference_texts):
    """Compares text similarity against known reliable sources."""
    input_embedding = model.encode(input_text, convert_to_tensor=True)
    reference_embeddings = model.encode(reference_texts, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(input_embedding, reference_embeddings)
    return similarities.max().item()  # Highest match

### **🔹 Step 6: Fact-Check User Query Against Google Fact Check API**
def check_fact_claim(query):
    """Searches Google Fact Check API for prior fact-checked claims."""
    try:
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={GOOGLE_FACT_CHECK_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "claims" in data and len(data["claims"]) > 0:
                return 1.0, f"✅ This information has been fact-checked: {data['claims'][0]['text']}"
        return 0.5, "⚠️ No fact-checks found for this claim."
    except Exception as e:
        return 0.3, f"❌ Error checking fact: {str(e)}"

### **🔹 Step 7: Compute Overall Validity Score**
def evaluate_article_validity(url, user_prompt):
    """Evaluates an article’s credibility based on category, content, and fact-checking."""
    # Detect category dynamically
    category = detect_category(user_prompt)

    # Check domain credibility
    domain_score, domain_explanation = check_domain_credibility(url, category)

    # Fetch article content
    article_text = fetch_url_text(url)
    if article_text.startswith("Error"):
        return 0, f"❌ Error fetching article content: {article_text}"

    # Compare with dynamically selected reference texts
    reference_texts = get_dynamic_trusted_sources(category)
    similarity_score = compare_text_similarity(article_text, reference_texts)

    # Fact-check user query
    fact_check_score, fact_check_explanation = check_fact_claim(user_prompt)

    # Compute final credibility score
    final_score = (domain_score + similarity_score + fact_check_score) / 3

    # Generate explanation
    explanation = (
        f"🔍 Category: {category}\n"
        f"🔎 Domain Check: {domain_explanation}\n"
        f"📊 Content Similarity: {round(similarity_score, 2)} (with trusted sources in {category})\n"
        f"✅ Fact Check Score: {round(fact_check_score, 2)} - {fact_check_explanation}\n"
        f"⭐ Final Credibility Score: {round(final_score, 2)}"
    )

    return final_score, explanation

### **🔹 Example Usage**
test_url = "https://www.travelandleisure.com/airlines-airports/new-york-city-airports"
user_query = "What is the best airport to use when flying into NYC?"
score, explanation = evaluate_article_validity(test_url, user_query)

print(f"Score: {score}\nExplanation:\n{explanation}")
