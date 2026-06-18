import re


# -----------------------------------
# 1. Keyword Detection
# -----------------------------------
def keyword_score(email):
    score = 0
    found_keywords = []

    phishing_keywords = [
        "urgent", "verify", "password", "login", "bank",
        "otp", "click", "claim", "prize", "suspended"
    ]

    email = email.lower()

    for word in phishing_keywords:
        if word in email:
            score += 10
            found_keywords.append(word)

    return score, found_keywords


# -----------------------------------
# 2. URL Detection
# -----------------------------------
def url_score(email):
    score = 0
    url_pattern = r'https?://\S+'
    urls = re.findall(url_pattern, email)

    if urls:
        score += 30

    return score, urls


# -----------------------------------
# 3. Suspicious Domain Check
# -----------------------------------
def suspicious_domain(urls):
    score = 0
    suspicious_extensions = [".xyz", ".ru", ".tk"]

    for url in urls:
        for ext in suspicious_extensions:
            if ext in url:
                score += 20

    return score


# -----------------------------------
# 4. IP URL Detection
# -----------------------------------
def ip_url_score(email):
    score = 0
    ip_pattern = r'https?://\d+\.\d+\.\d+\.\d+'

    if re.search(ip_pattern, email):
        score += 25

    return score


# -----------------------------------
# 5. Brand Spoof Detection
# -----------------------------------
def spoof_score(email):
    score = 0

    spoof_words = [
        "amaz0n",
        "paypa1",
        "g00gle",
        "micr0soft"
    ]

    email = email.lower()

    for word in spoof_words:
        if word in email:
            score += 30

    return score


# -----------------------------------
# 6. Too Many Subdomains
# -----------------------------------
def subdomain_score(urls):
    score = 0

    for url in urls:
        if url.count(".") > 3:
            score += 20

    return score


# -----------------------------------
# 7. Urgency Language
# -----------------------------------
def urgency_score(email):
    score = 0

    urgent_phrases = [
        "act now",
        "immediately",
        "limited time",
        "account locked",
        "verify now"
    ]

    email = email.lower()

    for phrase in urgent_phrases:
        if phrase in email:
            score += 15

    return score


# -----------------------------------
# 8. Final Detector
# -----------------------------------
def phishing_detector(email):
    total_score = 0
    reasons = []

    # Keyword detection
    k_score, keywords = keyword_score(email)
    total_score += k_score
    if keywords:
        reasons.append(f"Suspicious keywords found: {keywords}")

    # URL detection
    u_score, urls = url_score(email)
    total_score += u_score
    if urls:
        reasons.append(f"Suspicious URLs found: {urls}")

    # Suspicious domain
    d_score = suspicious_domain(urls)
    total_score += d_score
    if d_score > 0:
        reasons.append("Suspicious domain extension detected")

    # IP URL
    ip_score = ip_url_score(email)
    total_score += ip_score
    if ip_score > 0:
        reasons.append("IP-based URL detected")

    # Brand spoof
    spoof = spoof_score(email)
    total_score += spoof
    if spoof > 0:
        reasons.append("Brand spoofing detected")

    # Subdomain
    sub_score = subdomain_score(urls)
    total_score += sub_score
    if sub_score > 0:
        reasons.append("Too many subdomains detected")

    # Urgency
    urgency = urgency_score(email)
    total_score += urgency
    if urgency > 0:
        reasons.append("Urgent language detected")

    # Cap score at 100
    total_score = min(total_score, 100)

    return total_score, reasons


# -----------------------------------
# 9. Risk Level
# -----------------------------------
def risk_level(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


# -----------------------------------
# 10. Testing
# -----------------------------------
if __name__ == "__main__":
    email = """
    URGENT! Your Amaz0n account is locked.
    Act now and verify immediately.
    Click:
    http://192.168.1.1/login.verify.account.xyz
    """

    score, reasons = phishing_detector(email)

    print("Risk Score:", score)
    print("Risk Level:", risk_level(score))

    print("\nReasons:")
    for reason in reasons:
        print("-", reason)