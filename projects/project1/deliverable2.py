import requests
import re
import textstat
import torch
import logging
import json
from bs4 import BeautifulSoup
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ArticleValidator:
    """A production-ready class to validate, analyze, and rate an article's credibility."""
    
    def __init__(self, moz_access_id=None, moz_secret_key=None):
        self.moz_access_id = moz_access_id
        self.moz_secret_key = moz_secret_key
        self.credibility_model_name = "jy46604790/Fake-News-Bert-Detect"  # Fixed model

        # Load Hugging Face Credibility Model
        try:
            logging.info(f"Loading Hugging Face model: {self.credibility_model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.credibility_model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.credibility_model_name)
        except Exception as e:
            logging.error(f"Failed to load Hugging Face model: {e}")
            self.tokenizer, self.model = None, None  # Fail gracefully

    def is_valid_url(self, url):
        """Checks if a URL is well-formed and not from a suspicious domain."""
        suspicious_tlds = ["xyz", "ru", "tk", "cn", "top"]
        regex = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
        
        if not re.match(regex, url) or any(url.endswith(f".{tld}") for tld in suspicious_tlds):
            logging.warning(f"Invalid or suspicious URL: {url}")
            return False
        return True

    def get_article_text(self, url):
        """Extracts article content from a given URL, handles request failures gracefully."""
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text() for p in paragraphs]).strip()
            
            if not text:
                logging.warning(f"No readable content found for URL: {url}")
                return None
            return text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch article content: {e}")
            return None

    def get_readability_score(self, text):
        """Computes the Flesch-Kincaid readability score."""
        return textstat.flesch_reading_ease(text) if text else 0

    def analyze_credibility(self, text):
        """Uses Hugging Face model to assess credibility, handles model failure."""
        if not self.model or not text:
            logging.warning("Skipping credibility analysis due to missing model or text.")
            return 0.5  # Neutral credibility if model fails

        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs).logits
            return torch.softmax(outputs, dim=1)[0][1].item()  # Probability of credible content
        except Exception as e:
            logging.error(f"Failed to analyze credibility: {e}")
            return 0.5  # Fail gracefully with a neutral score

    def calculate_relevance(self, query, article_text):
        """Computes cosine similarity between query and article text."""
        if not article_text:
            return 0
        
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform([query, article_text])
        return cosine_similarity(vectors[0], vectors[1])[0][0]

    def get_moz_domain_score(self, url):
        """Retrieves Moz Domain Authority score, handles API failure."""
        if not self.moz_access_id or not self.moz_secret_key:
            logging.warning("Moz API credentials missing. Skipping domain trust analysis.")
            return None

        try:
            response = requests.post(
                "https://lsapi.seomoz.com/v2/url_metrics",
                json={"targets": [url]},
                auth=(self.moz_access_id, self.moz_secret_key)
            )
            data = response.json()
            return data.get("results", [{}])[0].get("domain_authority", None)
        except Exception as e:
            logging.error(f"Failed to fetch Moz domain score: {e}")
            return None  # Fail gracefully

    def convert_score_to_rating(self, final_score):
        """Converts a 0-100 score into a 5-star rating system."""
        rating = round((final_score / 100) * 5)
        rating = max(1, min(rating, 5))  # Ensure rating is between 1 and 5
        stars = "⭐" * rating + "☆" * (5 - rating)

        explanations = {
            1: "The source is unreliable and likely misleading.",
            2: "The source has some credibility but contains potential misinformation.",
            3: "The source is moderately reliable but may have biases.",
            4: "The source is generally trustworthy with good readability.",
            5: "The source is highly credible, relevant, and well-structured."
        }
        
        return rating, stars, explanations.get(rating, "No explanation available.")

    def rate_url_content(self, url, query):
        """Rates a URL and its content based on credibility, trustworthiness, readability, and relevance."""
        if not self.is_valid_url(url):
            return {"url": url, "rating": 1, "icon": "⭐☆☆☆☆", "explanation": "Invalid or suspicious URL."}

        article_text = self.get_article_text(url)
        if not article_text:
            return {"url": url, "rating": 1, "icon": "⭐☆☆☆☆", "explanation": "No readable content found."}

        readability = self.get_readability_score(article_text)
        credibility_score = self.analyze_credibility(article_text)
        relevance_score = self.calculate_relevance(query, article_text)
        domain_trust = self.get_moz_domain_score(url)

        # Weighted Final Rating
        final_score = (
            (domain_trust or 0) * 0.4 +  # 40% weight for domain trust
            (readability / 100) * 0.2 +  # 20% weight for readability
            (relevance_score * 100) * 0.3 +  # 30% weight for relevance
            (credibility_score * 100) * 0.2  # 20% weight for credibility
        )

        # Convert to 5-star rating
        rating, icon, explanation = self.convert_score_to_rating(final_score)

        result = {
            "url": url,
            "domain_trust": domain_trust,
            "readability": readability,
            "relevance_score": relevance_score,
            "credibility_score": credibility_score,
            "final_rating": final_score,
            "rating": rating,
            "icon": icon,
            "explanation": explanation
        }

        # Save output to JSON
        with open("analysis_result.json", "w", encoding="utf-8") as json_file:
            json.dump(result, json_file, indent=4, ensure_ascii=False)

        print("✅ Analysis saved to analysis_result.json")
        return result


