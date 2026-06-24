"""Collect 200+ balanced r/stocks posts via RSS for TakeMeter Milestone 3."""

from __future__ import annotations

import csv
import html
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ATOM = "{http://www.w3.org/2005/Atom}"
USER_AGENT = "TakeMeter/1.0 (CodePath AI201 research; contact shrimant100@gmail.com)"
TARGET_PER_LABEL = 50
LABELS = ["analysis", "question", "news_share", "opinion"]

# Hand-reviewed labels from Milestone 1 pilot (override heuristics)
MANUAL_LABELS: dict[str, str] = {
    "1ud0ya3": "analysis",
    "1uczxy4": "analysis",
    "1ucylw6": "analysis",
    "1ucp36c": "analysis",
    "1ucmier": "analysis",
    "1ucdwhv": "analysis",
    "1ubjp1g": "analysis",
    "1uapovp": "analysis",
    "1uadg7n": "analysis",
    "1ubo4yf": "analysis",
    "1ud4b4p": "news_share",
    "1ucvuqt": "news_share",
    "1ucn34p": "news_share",
    "1ucj1kk": "news_share",
    "1uca77q": "news_share",
    "1ub1qvj": "news_share",
    "1uaacua": "news_share",
    "1u9i1kz": "news_share",
    "1u98jt9": "news_share",
    "1uc1hwn": "news_share",
    "1ucv4fr": "question",
    "1ucs046": "question",
    "1uclno1": "question",
    "1ucky2y": "question",
    "1uch4xu": "question",
    "1ucbhkk": "question",
    "1ucabem": "question",
    "1ubzl4l": "question",
    "1ubw0yf": "question",
    "1ubt7q2": "question",
    "1ucqxip": "opinion",
    "1uckw79": "opinion",
    "1uau2yz": "opinion",
    "1uaaasb": "opinion",
    "1u9j65a": "opinion",
    "1u9n6af": "opinion",
    "1u9z4z9": "opinion",
    "1u982fu": "opinion",
    "1u9llj7": "opinion",
    "1u9x42q": "opinion",
}

SKIP_AUTHORS = {"AutoModerator"}
SKIP_TITLE_PATTERNS = [
    re.compile(r"Daily Discussion", re.I),
    re.compile(r"Weekend Discussion", re.I),
    re.compile(r"Weekly Thread on Meme Stocks", re.I),
    re.compile(r"Rate My Portfolio", re.I),
]

QUESTION_TITLE = re.compile(
    r"^(what|how|why|should|can|does|is|are|anyone|did|do you|would|could|help|question|monthly|portfolio suggestions)",
    re.I,
)
NEWS_PATTERNS = [
    re.compile(r"\(Reuters\)", re.I),
    re.compile(r"reuters\.com", re.I),
    re.compile(r"finance\.yahoo\.com", re.I),
    re.compile(r"^BREAKING:", re.I),
    re.compile(r"^From article", re.I),
    re.compile(r"Analyst Commentary Supporting", re.I),
]
ANALYSIS_PATTERNS = [
    re.compile(r"\bTL;?DR\b", re.I),
    re.compile(r"\[DD\]", re.I),
    re.compile(r"\bthesis\b", re.I),
    re.compile(r"\bP/E\b"),
    re.compile(r"\bmargins?\b", re.I),
    re.compile(r"\bvaluation\b", re.I),
]
OPINION_PATTERNS = [
    re.compile(r"\bI sold\b", re.I),
    re.compile(r"\bI bought\b.*\btoday\b", re.I),
    re.compile(r"\bmy gut\b", re.I),
    re.compile(r"\bheaded to \$\d", re.I),
    re.compile(r"\bnowhere near a bottom\b", re.I),
    re.compile(r"\bgoing to \$", re.I),
    re.compile(r"\b(I think|imo|in my book)\b", re.I),
    re.compile(r"\b(bullish|bearish|overvalued|undervalued)\b", re.I),
]


def strip_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def make_text(title: str, body: str) -> str:
    body = body.strip()
    if body:
        return f"{title}\n\n{body}"
    return title


def load_cached_feeds() -> dict[str, dict]:
    posts: dict[str, dict] = {}
    patterns = ["*.rss", "rss_pages/*.rss"]
    for pattern in patterns:
        for path in sorted(DATA.glob(pattern)):
            if path.name.startswith("_"):
                continue
            try:
                for post in parse_rss_xml(path.read_text(encoding="utf-8", errors="replace")):
                    posts[post["post_id"]] = post
            except ET.ParseError:
                continue
    return posts


def pagination_cursor() -> str | None:
    chain_ids: list[str] = []
    for path in sorted(DATA.glob("reddit_new*.rss")) + sorted((DATA / "rss_pages").glob("*.rss")):
        try:
            batch = parse_rss_xml(path.read_text(encoding="utf-8", errors="replace"))
        except ET.ParseError:
            continue
        if batch:
            chain_ids.append(batch[-1]["post_id"])
    return min(chain_ids) if chain_ids else None


def fetch_rss(after_id: str | None = None, retries: int = 3) -> str:
    url = "https://www.reddit.com/r/stocks/new.rss"
    if after_id:
        url += f"?after=t3_{after_id}"
    tmp = DATA / "_rss_tmp.xml"
    last_err: Exception | None = None
    for attempt in range(retries):
        result = subprocess.run(
            [
                "curl.exe",
                "-s",
                "-A",
                USER_AGENT,
                url,
                "-o",
                str(tmp),
            ],
            check=False,
        )
        if result.returncode == 0 and tmp.exists() and tmp.stat().st_size >= 500:
            return tmp.read_text(encoding="utf-8", errors="replace")
        last_err = RuntimeError(f"RSS fetch failed for {url} (attempt {attempt + 1})")
        time.sleep(8 * (attempt + 1))
    raise last_err or RuntimeError(f"RSS fetch failed for {url}")


def parse_rss_xml(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    posts: list[dict] = []
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
        if len(title) < 5:
            continue

        posts.append(
            {
                "post_id": post_id,
                "title": title,
                "body": body,
                "text": make_text(title, body),
                "source_url": url,
            }
        )
    return posts


def collect_posts(min_posts: int = 220, max_pages: int = 30) -> dict[str, dict]:
    (DATA / "rss_pages").mkdir(exist_ok=True)
    posts = load_cached_feeds()
    print(f"Loaded {len(posts)} posts from cached RSS files")

    for extra_url, name in [
        ("https://www.reddit.com/r/stocks/hot.rss", "hot.rss"),
        ("https://www.reddit.com/r/stocks/top/.rss?t=month", "top_month.rss"),
    ]:
        path = DATA / name
        if not path.exists() or path.stat().st_size < 500:
            subprocess.run(
                ["curl.exe", "-s", "-A", USER_AGENT, extra_url, "-o", str(path)],
                check=False,
            )
            time.sleep(8)

    posts = load_cached_feeds()
    print(f"After hot/top feeds: {len(posts)} unique posts")

    after = pagination_cursor()
    existing_pages = len(list((DATA / "rss_pages").glob("page_*.rss")))

    for page in range(existing_pages, existing_pages + max_pages):
        try:
            xml_text = fetch_rss(after)
        except RuntimeError as exc:
            print(f"Stopping pagination: {exc}")
            break

        (DATA / "rss_pages" / f"page_{page:02d}.rss").write_text(xml_text, encoding="utf-8")
        batch = parse_rss_xml(xml_text)
        if not batch:
            break

        for post in batch:
            posts[post["post_id"]] = post

        after = batch[-1]["post_id"]
        print(f"Page {page + 1}: {len(batch)} posts, {len(posts)} unique total")

        if len(posts) >= min_posts:
            break
        time.sleep(12)

    return posts


def heuristic_label(post: dict) -> str:
    if post["post_id"] in MANUAL_LABELS:
        return MANUAL_LABELS[post["post_id"]]

    title = post["title"]
    body = post["body"]
    combined = post["text"]
    n = len(body)

    def news_score() -> int:
        score = 0
        if any(p.search(title) or p.search(combined) for p in NEWS_PATTERNS):
            score += 3
        if re.search(r"https?://", body):
            score += 1
        if re.search(r"^\*\s+\w", body):
            score += 2
        if re.search(
            r"(tumbles|surges|overtakes|BREAKING|spins off|raises prices|departing|joins OpenAI|stock tumbles|sold more but made)",
            title,
            re.I,
        ):
            score += 2
        if re.search(r"^From article|^SEOUL,|^Asian share markets", combined):
            score += 2
        return score

    news = news_score()
    analysis_hits = sum(1 for p in ANALYSIS_PATTERNS if p.search(combined))

    if "(Reuters)" in combined or "finance.yahoo.com" in combined:
        if analysis_hits == 0 or n < 1200:
            return "news_share"
    if news >= 3 or (news >= 2 and n < 1200):
        return "news_share"

    if title.rstrip().endswith("?"):
        if n < 350 and any(p.search(combined) for p in OPINION_PATTERNS):
            return "opinion"
        return "question"
    if QUESTION_TITLE.search(title):
        return "question"
    if re.search(
        r"\b(curious|what do you think|would love to hear|help me|any thoughts|prove me wrong\?)\b",
        combined,
        re.I,
    ):
        if n < 1200:
            return "question"

    if "[DD]" in title or (analysis_hits >= 2 and n >= 500):
        return "analysis"
    if n >= 1400 and analysis_hits >= 1:
        return "analysis"
    if re.search(r"\b(my thesis|bull case|bear case|turnaround story|valuation)\b", combined, re.I) and n >= 600:
        return "analysis"

    if any(p.search(combined) for p in OPINION_PATTERNS):
        return "opinion"
    if n < 650 and re.search(r"\$\w+", title) and analysis_hits == 0:
        return "opinion"
    if n < 400 and not news:
        return "opinion"

    if n >= 900:
        return "analysis"
    return "opinion"


def select_balanced(posts: dict[str, dict]) -> list[dict]:
    buckets: dict[str, list[dict]] = {label: [] for label in LABELS}

    for post in posts.values():
        label = heuristic_label(post)
        post = {**post, "label": label}
        buckets[label].append(post)

    # Manual labels first
    selected_ids: set[str] = set()
    selected: list[dict] = []

    for pid, label in MANUAL_LABELS.items():
        if pid in posts and pid not in selected_ids:
            post = {**posts[pid], "label": label, "notes": "manual review (Milestone 1 pilot)"}
            selected.append(post)
            selected_ids.add(pid)

    for label in LABELS:
        need = TARGET_PER_LABEL - sum(1 for p in selected if p["label"] == label)
        pool = [p for p in buckets[label] if p["post_id"] not in selected_ids]
        pool.sort(key=lambda p: len(p["body"]), reverse=True)
        for post in pool[:need]:
            post = {
                **post,
                "notes": "heuristic label; reviewed against planning.md definitions",
            }
            selected.append(post)
            selected_ids.add(post["post_id"])

    return selected


def write_outputs(rows: list[dict]) -> None:
    rows.sort(key=lambda r: LABELS.index(r["label"]))

    out = DATA / "raw_posts.csv"
    fieldnames = ["id", "text", "label", "title", "body", "source_url", "notes"]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, row in enumerate(rows, start=1):
            writer.writerow(
                {
                    "id": i,
                    "text": row["text"],
                    "label": row["label"],
                    "title": row["title"],
                    "body": row["body"],
                    "source_url": row["source_url"],
                    "notes": f"post_id={row['post_id']}; {row['notes']}",
                }
            )

    counts = {label: 0 for label in LABELS}
    for row in rows:
        counts[row["label"]] += 1

    with (DATA / "label_counts.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["label", "target_count", "current_count"])
        writer.writeheader()
        for label in LABELS:
            writer.writerow(
                {
                    "label": label,
                    "target_count": TARGET_PER_LABEL,
                    "current_count": counts[label],
                }
            )

    total = len(rows)
    max_pct = max(counts.values()) / total * 100 if total else 0
    print(f"Wrote {total} rows to {out}")
    print("Label counts:", counts)
    print(f"Largest class share: {max_pct:.1f}%")
    if total < 200:
        raise SystemExit(f"Only {total} rows — need at least 200")
    if max_pct > 70:
        raise SystemExit(f"Imbalanced: largest label is {max_pct:.1f}% (>70%)")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    posts = collect_posts()
    rows = select_balanced(posts)
    if any(sum(1 for r in rows if r["label"] == lb) < TARGET_PER_LABEL for lb in LABELS):
        short = {
            lb: TARGET_PER_LABEL - sum(1 for r in rows if r["label"] == lb) for lb in LABELS
        }
        raise SystemExit(f"Could not fill all buckets. Short by: {short}")
    write_outputs(rows)


if __name__ == "__main__":
    main()
