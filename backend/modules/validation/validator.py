def validate_copy(copy: dict) -> bool:
    if not copy:
        return False
    if len(copy.get("headline", "")) < 10:
        return False
    if len(copy.get("bullets", [])) < 5:
        return False
    if not copy.get("cta"):
        return False
    return True
