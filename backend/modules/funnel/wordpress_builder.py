import requests
from requests.auth import HTTPBasicAuth
from backend.core.config import WP_URL, WP_USER, WP_PASS

AUTH = HTTPBasicAuth(WP_USER, WP_PASS)

def create_page(title: str, content: str) -> dict:
    url = f"{WP_URL}/wp-json/wp/v2/pages"
    r = requests.post(url, json={"title": title, "content": content, "status": "publish"}, auth=AUTH)
    r.raise_for_status()
    return r.json()

def build_landing_page_html(copy: dict) -> str:
    bullets_html = "".join(f"<li>{b}</li>" for b in copy.get("bullets", []))
    faq_html = "".join(
        f"<h3>{item.get('q','')}</h3><p>{item.get('a','')}</p>"
        for item in copy.get("faq", [])
    )
    h = copy.get("headline", "")
    s = copy.get("subheadline", "")
    st = copy.get("story", "")
    cta = copy.get("cta", "Buy Now")
    return (
        '<div class="sales-page">'
        f"<h1>{h}</h1><h2>{s}</h2><p>{st}</p>"
        f"<ul>{bullets_html}</ul>"
        f'<a class="cta-button" href="#order">{cta}</a>'
        '<div class="faq"><h2>Frequently Asked Questions</h2>'
        f"{faq_html}</div></div>"
    )

def build_funnel(copy: dict, data: dict) -> dict:
    name   = data.get("niche", "Product")
    price  = data.get("price", "")
    target = data.get("target", "")
    landing  = create_page(f"{name} - Landing Page", build_landing_page_html(copy))
    checkout = create_page(f"{name} - Checkout", f"<h1>Order {name}</h1><p>Price: {price}</p>")
    upsell   = create_page(f"{name} - Upsell",   f"<h1>Special Offer for {target}</h1>")
    return {
        "landing_page_id": landing.get("id"),
        "checkout_id":     checkout.get("id"),
        "upsell_id":       upsell.get("id"),
        "url":             landing.get("link", "")
    }
