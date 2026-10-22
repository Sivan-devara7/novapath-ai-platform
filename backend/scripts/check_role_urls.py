import os
import json
import httpx
from typing import Dict, List, Any

def check_all_urls():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    roles_dir = os.path.join(backend_dir, "data", "roles")

    all_urls = []

    for fname in os.listdir(roles_dir):
        if fname.endswith(".json"):
            fpath = os.path.join(roles_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                role_data = json.load(f)

            role_name = role_data.get("role", fname)

            # Check sources
            for src in role_data.get("sources", []):
                all_urls.append({"role": role_name, "context": "source", "title": "Source URL", "url": src})

            # Check roadmap resources
            for step in role_data.get("roadmap", []):
                for res in step.get("resources", []):
                    all_urls.append({
                        "role": role_name,
                        "context": f"roadmap_step_{step.get('step')}",
                        "title": res.get("title", ""),
                        "url": res.get("url", "")
                    })

    print(f"Total URLs to check: {len(all_urls)}")
    print("=" * 70)

    # De-duplicate URLs for checking
    unique_urls = {}
    for item in all_urls:
        u = item["url"].strip()
        if u and u not in unique_urls:
            unique_urls[u] = []
        if u:
            unique_urls[u].append(item)

    print(f"Unique URLs to test: {len(unique_urls)}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    results = []
    failures = []

    client = httpx.Client(timeout=10.0, follow_redirects=True, headers=headers)

    for idx, (url, items) in enumerate(unique_urls.items(), 1):
        status_code = None
        error_msg = None
        try:
            resp = client.get(url)
            status_code = resp.status_code
            # Consider 200, 301, 302, 403 (Cloudflare protection often blocks automated requests with 403 but the URL is valid)
            is_valid = status_code in [200, 201, 204, 301, 302, 307, 308, 403]
        except Exception as e:
            is_valid = False
            error_msg = str(e)

        item_repr = items[0]
        res_info = {
            "url": url,
            "status_code": status_code,
            "is_valid": is_valid,
            "error": error_msg,
            "role": item_repr["role"],
            "title": item_repr["title"]
        }
        results.append(res_info)

        if not is_valid or (status_code and status_code >= 400 and status_code != 403):
            failures.append(res_info)
            print(f"[{idx:2d}/{len(unique_urls)}] FAIL ({status_code or error_msg}): {url}")
        else:
            print(f"[{idx:2d}/{len(unique_urls)}] OK ({status_code}): {url}")

    print("=" * 70)
    print(f"Total checked: {len(results)} | Successful: {len(results) - len(failures)} | Failures: {len(failures)}")
    if failures:
        print("\nList of failed URLs:")
        for f in failures:
            print(f"  - {f['role']} | {f['title']} | Status: {f['status_code']} | Error: {f['error']} | URL: {f['url']}")

    # Save results to a report file
    report_path = os.path.join(backend_dir, "data", "url_http_audit_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(results), "failures": failures, "all": results}, f, indent=2)

    print(f"Saved URL audit report to: {report_path}")

if __name__ == "__main__":
    check_all_urls()
