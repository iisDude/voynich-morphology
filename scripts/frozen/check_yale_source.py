"""Probe public Yale catalogue/IIIF sources, saving only project-local evidence."""
from common import OUT, write_json
import concurrent.futures
import urllib.request
import urllib.error
import json

URLS = [
    "https://collections.library.yale.edu/iiif/2002046/manifest",
    "https://collections.library.yale.edu/iiif/2/1006076/info.json",
    "https://collections.library.yale.edu/catalog/2002046",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Voynich structural research; public image provenance check"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            data = response.read(10 * 1024 * 1024)
            mime = response.headers.get("Content-Type", "")
            result = dict(url=url, status=response.status, content_type=mime, bytes=len(data))
            if "json" in mime or url.endswith("manifest"):
                try:
                    result["json"] = json.loads(data)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    result["text_preview"] = data[:500].decode("utf-8", errors="replace")
            else:
                result["text_preview"] = data[:500].decode("utf-8", errors="replace")
            return result
    except Exception as error:
        return dict(url=url, error=str(error))


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fetch, URLS))
    write_json(OUT / "data/source/yale_source_probe.json", results)
    for result in results:
        small = {k: v for k, v in result.items() if k not in ["json", "text_preview"]}
        if "json" in result:
            small["json_keys"] = list(result["json"])[:12]
            if "width" in result["json"]:
                small["width"] = result["json"]["width"]
                small["height"] = result["json"]["height"]
        print(small, flush=True)


if __name__ == "__main__":
    main()
