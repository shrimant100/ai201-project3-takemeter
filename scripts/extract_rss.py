"""Parse r/stocks RSS feeds and write 40 labeled rows to raw_posts.csv."""

from __future__ import annotations

import csv
import html
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ATOM = "{http://www.w3.org/2005/Atom}"

# 40 posts, 10 per label — primary-purpose labeling (see planning.md)
SELECTED: list[tuple[str, str]] = [
    # analysis — structured investment arguments
    ("1ud0ya3", "analysis"),
    ("1uczxy4", "analysis"),
    ("1ucylw6", "analysis"),
    ("1ucp36c", "analysis"),
    ("1ucmier", "analysis"),
    ("1ucdwhv", "analysis"),
    ("1ubjp1g", "analysis"),
    ("1uapovp", "analysis"),
    ("1uadg7n", "analysis"),
    ("1ubo4yf", "analysis"),
    # news_share — mainly sharing/summarizing news
    ("1ud4b4p", "news_share"),
    ("1ucvuqt", "news_share"),
    ("1ucn34p", "news_share"),
    ("1ucj1kk", "news_share"),
    ("1uca77q", "news_share"),
    ("1ub1qvj", "news_share"),
    ("1uaacua", "news_share"),
    ("1u9i1kz", "news_share"),
    ("1u98jt9", "news_share"),
    ("1uc1hwn", "news_share"),
    # question — seeking advice or community input
    ("1ucv4fr", "question"),
    ("1ucs046", "question"),
    ("1uclno1", "question"),
    ("1ucky2y", "question"),
    ("1uch4xu", "question"),
    ("1ucbhkk", "question"),
    ("1ucabem", "question"),
    ("1ubzl4l", "question"),
    ("1ubw0yf", "question"),
    ("1ubt7q2", "question"),
    # opinion — bare sentiment/predictions without structured reasoning
    ("1ucqxip", "opinion"),
    ("1uckw79", "opinion"),
    ("1uau2yz", "opinion"),
    ("1uaaasb", "opinion"),
    ("1u9j65a", "opinion"),
    ("1u9n6af", "opinion"),
    ("1u9z4z9", "opinion"),
    ("1u982fu", "opinion"),
    ("1u9llj7", "opinion"),
    ("1u9x42q", "opinion"),
]

SKIP_AUTHORS = {"AutoModerator"}
SKIP_TITLE_PATTERNS = [
    re.compile(r"Daily Discussion", re.I),
    re.compile(r"Weekend Discussion", re.I),
    re.compile(r"Weekly Thread on Meme Stocks", re.I),
    re.compile(r"Rate My Portfolio", re.I),
]

FEEDS = [
    ("https://www.reddit.com/r/stocks/new.rss", "reddit_new.rss"),
    ("https://www.reddit.com/r/stocks/new.rss?after=t3_1ubt7q2", "reddit_new_p2.rss"),
    ("https://www.reddit.com/r/stocks/new.rss?after=t3_1ua6bz3", "reddit_new_p3.rss"),
]


def strip_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_feed(path: Path) -> dict[str, dict]:
    posts: dict[str, dict] = {}
    root = ET.parse(path).getroot()
    for entry in root.findall(f"{ATOM}entry"):
        title = (entry.findtext(f"{ATOM}title") or "").strip()
        author_el = entry.find(f"{ATOM}author")
        author = (author_el.findtext(f"{ATOM}name") if author_el is not None else "") or ""
        if author in SKIP_AUTHORS:
            continue
        if any(p.search(title) for p in SKIP_TITLE_PATTERNS):
            continue

        post_id = (entry.findtext(f"{ATOM}id") or "").replace("t3_", "")
        link_el = entry.find(f"{ATOM}link")
        url = link_el.get("href") if link_el is not None else ""
        content = entry.findtext(f"{ATOM}content") or ""
        body = strip_html(content)
        body = re.split(r"\s+submitted by\s+", body, maxsplit=1)[0].strip()

        posts[post_id] = {
            "post_id": post_id,
            "title": title,
            "body": body,
            "source_url": url,
        }
    return posts


def ensure_feeds() -> None:
    for url, filename in FEEDS:
        path = DATA / filename
        if path.exists() and path.stat().st_size > 1000:
            continue
        subprocess.run(
            [
                "curl.exe",
                "-s",
                "-A",
                "TakeMeter/1.0 (CodePath AI201 research; contact shrimant100@gmail.com)",
                url,
                "-o",
                str(path),
            ],
            check=True,
        )


def csv_escape(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def main() -> None:
    ensure_feeds()
    posts: dict[str, dict] = {}
    for _, filename in FEEDS:
        path = DATA / filename
        if path.exists() and path.stat().st_size > 0:
            posts.update(parse_feed(path))

    missing = [pid for pid, _ in SELECTED if pid not in posts]
    if missing:
        raise SystemExit(f"Missing post IDs in RSS feeds: {missing}")

    out = DATA / "raw_posts.csv"
    rows = []
    for i, (post_id, label) in enumerate(SELECTED, start=1):
        post = posts[post_id]
        rows.append(
            {
                "id": i,
                "title": csv_escape(post["title"]),
                "body": csv_escape(post["body"]),
                "label": label,
                "source_url": post["source_url"],
                "notes": f"post_id={post_id}; collected via r/stocks RSS; review borderline labels",
            }
        )

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "title", "body", "label", "source_url", "notes"]
        )
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for _, label in SELECTED:
        counts[label] = counts.get(label, 0) + 1

    counts_path = DATA / "label_counts.csv"
    with counts_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["label", "target_count", "current_count"])
        writer.writeheader()
        for label in ["analysis", "question", "news_share", "opinion"]:
            writer.writerow(
                {"label": label, "target_count": 50, "current_count": counts[label]}
            )

    print(f"Wrote {len(rows)} posts to {out}")
    print("Label counts:", counts)


if __name__ == "__main__":
    main()
