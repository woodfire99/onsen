import sys

if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else ""
    if task == "scraper_main":
        import onsen_scraper;
    elif task == "scraper_latlng":
        import latlng_scraper;
    elif task == "scraper_photo":
        import photo_scraper;
    elif task == "txt":
        import txt_to_csv;
    elif task == "gpd":
        import to_gpd;
    elif task == "gml_coast":
        import to_gml_coastline;
    elif task == "save_detail":
        import save_html_detail;
    elif task == "scraper_detail_card":
        import detail_scraper_card;
    elif task == "scraper_detail_hist":
        import detail_scraper_history;
    elif task == "save_review":
        import save_html_detail_review;
    elif task == "scraper_detail_around":
        import detail_scraper_around;
    elif task == "api_JSONL":
        import api_jsonl;
    else:
        print("Usage: script [access|temp]")