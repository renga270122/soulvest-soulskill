import argparse
import json
import os
import sys
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright


VIEWPORTS = [
    ("mobile", {"width": 390, "height": 844}),
    ("tablet", {"width": 768, "height": 1024}),
    ("laptop", {"width": 1366, "height": 768}),
    ("desktop", {"width": 1920, "height": 1080}),
]


def _normalize_base_url(url: str) -> str:
    return url.rstrip("/")


def _join_url(base_url: str, path: str) -> str:
    if not path:
        return base_url
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{base_url}{path}"


def run_device_checks(base_url: str, paths: list[str], output_dir: str) -> int:
    os.makedirs(output_dir, exist_ok=True)
    run_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for viewport_name, viewport in VIEWPORTS:
                for path in paths:
                    page_url = _join_url(base_url, path)
                    context = browser.new_context(viewport=viewport)
                    page = context.new_page()

                    try:
                        page.goto(page_url, wait_until="domcontentloaded", timeout=30000)
                        page.wait_for_timeout(1200)

                        metrics = page.evaluate(
                            """
                            () => ({
                              scrollWidth: document.documentElement.scrollWidth,
                              innerWidth: window.innerWidth,
                              hasMain: !!document.querySelector('[data-testid="stAppViewContainer"]'),
                              buttonCount: document.querySelectorAll('button').length,
                              bodyText: (document.body?.innerText || '').slice(0, 400)
                            })
                            """
                        )

                        has_overflow = metrics["scrollWidth"] > metrics["innerWidth"] + 2
                        has_ui = bool(metrics["hasMain"]) or (metrics["buttonCount"] > 0)

                        filename = f"{viewport_name}_{path.strip('/').replace('/', '_') or 'root'}.png"
                        screenshot_path = os.path.join(output_dir, filename)
                        page.screenshot(path=screenshot_path, full_page=True)

                        run_results.append(
                            {
                                "viewport": viewport_name,
                                "path": path,
                                "url": page_url,
                                "status": "PASS" if (not has_overflow and has_ui) else "FAIL",
                                "has_horizontal_overflow": has_overflow,
                                "ui_detected": has_ui,
                                "metrics": metrics,
                                "screenshot": screenshot_path,
                            }
                        )
                    except Exception as exc:
                        run_results.append(
                            {
                                "viewport": viewport_name,
                                "path": path,
                                "url": page_url,
                                "status": "FAIL",
                                "error": str(exc),
                            }
                        )
                    finally:
                        context.close()
        finally:
            browser.close()

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "base_url": base_url,
        "paths": paths,
        "results": run_results,
        "pass_count": sum(1 for r in run_results if r["status"] == "PASS"),
        "fail_count": sum(1 for r in run_results if r["status"] == "FAIL"),
    }

    report_file = os.path.join(output_dir, "device_qa_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n=== Device QA Report ===")
    for item in run_results:
        line = f"{item['status']}: {item['viewport']} {item['path']}"
        if item.get("has_horizontal_overflow"):
            line += " | horizontal overflow detected"
        if item.get("error"):
            line += f" | error: {item['error']}"
        print(line)

    print(f"\nReport saved: {report_file}")
    print(f"Screenshots dir: {output_dir}")
    print(f"PASS: {summary['pass_count']} | FAIL: {summary['fail_count']}")

    return 0 if summary["fail_count"] == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run responsive device QA checks with Playwright.")
    parser.add_argument("--url", default="http://127.0.0.1:8501", help="Base URL of the running app")
    parser.add_argument(
        "--paths",
        nargs="+",
        default=["/"],
        help="Paths to validate (for Streamlit, root path is usually enough)",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts/device_qa",
        help="Directory to store screenshots and JSON report",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = _normalize_base_url(args.url)

    try:
        return run_device_checks(base_url, args.paths, args.output_dir)
    except Exception as exc:
        print("Device QA runner failed.")
        print(str(exc))
        print("If this is the first run, install browser binaries with: playwright install chromium")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
