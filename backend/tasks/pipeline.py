from backend.tasks.celery_app import celery
from backend.modules.scraper.scraper import scrape_page
from backend.modules.extractor.extractor import extract_structure
from backend.modules.ai_copy.template_engine import generate_copy_from_template
from backend.modules.ai_copy.generator import generate_copy
from backend.modules.validation.validator import validate_copy
from backend.modules.creatives.generator import generate_creative
from backend.modules.funnel.wordpress_builder import build_funnel
from backend.modules.ads.meta_ads import create_full_campaign
from backend.utils.logger import log

@celery.task(bind=True)
def start_pipeline(self, data):
    log(f"Pipeline started for: {data.get('product_url')}")

    self.update_state(state="PROGRESS", meta={"step": "scraping", "pct": 10})
    html = scrape_page(data["product_url"])

    self.update_state(state="PROGRESS", meta={"step": "extracting", "pct": 25})
    structure = extract_structure(html)

    self.update_state(state="PROGRESS", meta={"step": "generating_copy", "pct": 40})
    context = {
        "benefit": structure.get("headline", "achieve your goals"),
        "target":  data.get("target", "people"),
        "pain":    "wasting time",
        "timeframe": "30 days"
    }
    copy = generate_copy_from_template(context)

    self.update_state(state="PROGRESS", meta={"step": "validating", "pct": 55})
    if not validate_copy(copy):
        log("Template copy failed — calling Claude...")
        copy = generate_copy(structure)

    self.update_state(state="PROGRESS", meta={"step": "building_funnel", "pct": 65})
    funnel = build_funnel(copy, data)

    self.update_state(state="PROGRESS", meta={"step": "generating_creative", "pct": 80})
    creative_prompt = f"{data.get('niche')} product for {data.get('target')}, {copy.get('headline','')}"
    creative_path = generate_creative(creative_prompt)

    self.update_state(state="PROGRESS", meta={"step": "creating_ads", "pct": 92})
    product_name = f"{data.get('niche', 'Product')} - {data.get('country', 'BR')}"
    ads = create_full_campaign(product_name, funnel.get("url", ""), creative_path)

    log("Pipeline complete")
    return {
        "status": "complete",
        "copy": copy,
        "funnel": funnel,
        "ads": ads,
        "creative": creative_path
    }
