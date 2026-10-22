import os
import json
import asyncio
import httpx

async def check_url(client, item, semaphore):
    url = item["url"].strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    async with semaphore:
        status_code = None
        error_msg = None
        try:
            resp = await client.get(url, headers=headers, follow_redirects=True, timeout=8.0)
            status_code = resp.status_code
            is_valid = status_code in [200, 201, 204, 301, 302, 307, 308, 403]
        except Exception as e:
            is_valid = False
            error_msg = str(e)

        return {
            "url": url,
            "status_code": status_code,
            "is_valid": is_valid,
            "error": error_msg,
            "role": item["role"],
            "title": item["title"]
        }

async def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    roles_dir = os.path.join(backend_dir, "data", "roles")

    all_items = []
    for fname in os.listdir(roles_dir):
        if fname.endswith(".json"):
            fpath = os.path.join(roles_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                role_data = json.load(f)

            role_name = role_data.get("role", fname)

            for src in role_data.get("sources", []):
                all_items.append({"role": role_name, "title": "Source URL", "url": src})

            for step in role_data.get("roadmap", []):
                for res in step.get("resources", []):
                    all_items.append({
                        "role": role_name,
                        "title": res.get("title", ""),
                        "url": res.get("url", "")
                    })

    # Deduplicate by URL
    seen_urls = set()
    unique_items = []
    for item in all_items:
        u = item["url"].strip()
        if u and u not in seen_urls:
            seen_urls.add(u)
            unique_items.append(item)

    print(f"Checking {len(unique_items)} unique URLs concurrently...")

    semaphore = asyncio.Semaphore(15)
    async with httpx.AsyncClient(verify=False) as client:
        tasks = [check_url(client, item, semaphore) for item in unique_items]
        results = await asyncio.gather(*tasks)

    failures = [r for r in results if not r["is_valid"] or (r["status_code"] and r["status_code"] >= 400 and r["status_code"] != 403)]

    print("=" * 70)
    print(f"Total checked: {len(results)} | Valid: {len(results) - len(failures)} | Failed: {len(failures)}")
    print("=" * 70)
    for f in failures:
        print(f"FAILED: [{f['status_code']}] {f['url']} ({f['role']} - {f['title']}) Error: {f['error']}")

    report_path = os.path.join(backend_dir, "data", "url_http_audit_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(results), "failures": failures, "all": results}, f, indent=2)
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    asyncio.run(main())
