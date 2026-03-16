import random

COPY_TEMPLATES = {
    "headline": [
        "How {target} can finally {benefit}",
        "The simple way to {benefit} without {pain}",
        "Discover how to {benefit} in {timeframe}",
        "{benefit}: the new method for {target}",
        "Why thousands of {target} are choosing this to {benefit}",
        "Stop struggling with {pain}. Start {benefit} today.",
        "The proven system to {benefit} — even if you have no experience"
    ],
    "subheadline": [
        "A proven method to help you {benefit} starting today.",
        "Created for {target} who want to {benefit} faster.",
        "The step-by-step approach anyone can use.",
        "No complicated tools. Just results.",
        "Join thousands of {target} who already transformed their results."
    ],
    "cta": [
        "Start Now", "Get Instant Access", "Try It Today",
        "Unlock The Method", "Download Now", "Yes, I Want This", "Get Started Now"
    ],
    "bullets": [
        "Works even if you are a complete beginner",
        "Step-by-step system, nothing is left out",
        "Tested and proven by thousands of {target}",
        "Get results in as little as {timeframe}",
        "100% money-back guarantee",
        "No prior experience needed",
        "Works for {target} of any background",
        "Easy to follow, even with a busy schedule"
    ]
}

def fill(template: str, ctx: dict) -> str:
    for k, v in ctx.items():
        template = template.replace("{" + k + "}", str(v))
    return template

def generate_copy_from_template(context: dict) -> dict:
    headline    = fill(random.choice(COPY_TEMPLATES["headline"]),    context)
    subheadline = fill(random.choice(COPY_TEMPLATES["subheadline"]), context)
    cta         = fill(random.choice(COPY_TEMPLATES["cta"]),         context)
    bullets     = [fill(b, context) for b in random.sample(COPY_TEMPLATES["bullets"], 5)]
    return {
        "headline":    headline,
        "subheadline": subheadline,
        "bullets":     bullets,
        "cta":         cta,
        "story": f"Discover how {context.get('target','people')} are achieving {context.get('benefit','amazing results')} with this simple method.",
        "faq": [
            {"q": "Who is this for?",           "a": f"Designed specifically for {context.get('target','anyone')}."},
            {"q": "How fast will I see results?","a": f"Most users see results within {context.get('timeframe','30 days')}."},
            {"q": "Is there a guarantee?",       "a": "Yes, we offer a 30-day money-back guarantee."}
        ]
    }
