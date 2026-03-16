from bs4 import BeautifulSoup

def extract_structure(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    h1 = soup.find("h1")
    data["headline"] = h1.get_text(strip=True) if h1 else ""

    h2 = soup.find("h2")
    data["subheadline"] = h2.get_text(strip=True) if h2 else ""

    bullets = [li.get_text(strip=True) for li in soup.find_all("li") if len(li.get_text(strip=True)) > 20]
    data["bullets"] = bullets[:10]

    ctas = [
        btn.get_text(strip=True)
        for btn in soup.find_all(["button", "a"])
        if any(w in btn.get_text(strip=True).lower() for w in ["buy","start","download","access","get","order","comprar","acessar"])
    ]
    data["cta"] = ctas[0] if ctas else "Get Access Now"

    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 50]
    data["story"] = " ".join(paragraphs[:3])

    faq = []
    for q in soup.find_all(["h3", "strong"]):
        text = q.get_text(strip=True)
        if "?" in text:
            answer = q.find_next("p")
            if answer:
                faq.append({"q": text, "a": answer.get_text(strip=True)})
            if len(faq) >= 3:
                break
    data["faq"] = faq

    return data
