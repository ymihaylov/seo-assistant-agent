def score_result(s: dict):
    t = s.get("title", "") or ""

    return {
        "title_length_ok": len(t) <= 60,
    }
