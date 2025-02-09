from deliverable2 import *

validator = ArticleValidator(moz_access_id="your_moz_access_id", moz_secret_key="your_moz_secret_key")
query = "What are the benefits of AI in healthcare?"
url = "https://www.mayoclinic.org/healthy-lifestyle/infant-and-toddler-health/expert-answers/air-travel-with-infant/faq-20058539"
result = validator.rate_url_content(url, query)
print(result)