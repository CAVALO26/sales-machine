import requests
from backend.core.config import META_ACCESS_TOKEN, META_AD_ACCOUNT

BASE = "https://graph.facebook.com/v19.0"

def create_campaign(name: str) -> str:
    r = requests.post(f"{BASE}/act_{META_AD_ACCOUNT}/campaigns", data={
        "name": name, "objective": "OUTCOME_TRAFFIC",
        "status": "PAUSED", "access_token": META_ACCESS_TOKEN
    })
    r.raise_for_status()
    return r.json()["id"]

def create_adset(campaign_id: str, page_url: str) -> str:
    r = requests.post(f"{BASE}/act_{META_AD_ACCOUNT}/adsets", data={
        "name": "Adset - Auto", "campaign_id": campaign_id,
        "daily_budget": 500, "billing_event": "IMPRESSIONS",
        "optimization_goal": "LINK_CLICKS", "status": "PAUSED",
        "targeting": '{"geo_locations":{"countries":["BR"]}}',
        "access_token": META_ACCESS_TOKEN
    })
    r.raise_for_status()
    return r.json()["id"]

def create_full_campaign(name: str, page_url: str, creative_path: str) -> dict:
    campaign_id = create_campaign(name)
    adset_id    = create_adset(campaign_id, page_url)
    return {"campaign_id": campaign_id, "adset_id": adset_id, "status": "PAUSED - ready to activate"}
