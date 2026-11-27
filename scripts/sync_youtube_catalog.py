#!/usr/bin/env python3
"""Refresh sources/youtube/video-id.json from the book's YouTube channel list.

Channel ids come from chapters/_07.1-youtube-xml-feeds.qmd. For each channel
the script lists the Videos and Live tabs with yt-dlp --flat-playlist. It does
not request the Shorts tab, and it drops /shorts/ URLs, #shorts titles, and
premieres that have not aired.

IBM Technology is the exception: only videos that are clearly about AI are
added. A title that matches the AI patterns is included. A title that is only
ambiguous (GPU, knowledge graph, digital worker, and the other patterns in
AMBIGUOUS) is decided from the watch-page description. A bare #AI hashtag or a
"Learn about watsonx" link does not count. Watson Orchestrate does, including
the watsonorchestrate hashtag. Any other IBM title is excluded, including
general cloud, cybersecurity, quantum, mainframes, networking, and business.
Watson Query is excluded unless the rest of the title is clearly about AI.
"Featuring Mixture of Experts" is the name of a show, so that phrase alone
does not count as the model architecture.

Every other channel keeps all of its non-Short videos and past live streams.

Existing catalog rows are left as they are, including the sample row.
New rows use the same keys, in the same order, with null transcript and summary.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE = Path.home() / ".cache" / "ai-book-youtube-catalog"
CHANNEL_QMD = ROOT / "chapters" / "_07.1-youtube-xml-feeds.qmd"
CATALOG_PATH = ROOT / "sources" / "youtube" / "video-id.json"
IBM_CHANNEL_ID = "UCKWaEZ-_VweaEx1j62do_vQ"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
CHANNEL_LINK = re.compile(
    r"\[([^\]]+)\]\(https://www\.youtube\.com/feeds/videos\.xml\?channel_id=([A-Za-z0-9_-]+)\)"
)
PLAYER_CLIENTS = (None, "web", "android", "ios", "tv", "mweb")
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# Title (or, for an ambiguous title, description) matches when the video is
# clearly about AI: LLMs and generative AI, agents and agentic engineering,
# RAG, prompt engineering, classical and deep learning, training and inference,
# AI governance and safety, vector databases, or MCP.
STRONG = re.compile(
    r"(?ix)"
    r"\bA\.I\.?\b"
    r"| \bAI\b"
    r"| artificial\ intelligence"
    r"| artificial\ (?:super|general)\ intelligence"
    r"| \bAGI\b | \bASI\b | superalignment"
    r"| \bLLMs?\b | large\ language\ models? | \blanguage\ models?\b"
    r"| \bGPTs?\b | \bChatGPT\b | \bClaude\b | \bGemini\b | \bGrok\b"
    r"| \bLLaMAs?\b | \bLlama\b | \bMistral\b | \bMixtral\b | \bGranite\b"
    r"| watsonx | \bWatsons?\b"
    r"| \bgenerative\b | \bgenAI\b | \bgen[\s-]?AI\b"
    r"| machine\ learning | deep\ learning | neural\ (?:net|network)s?"
    r"| \bNLP\b | natural\ language | computer\ vision"
    r"| foundation\ models?"
    r"| \bRAG\b | retrieval[-\s]augmented"
    r"| prompt\ engineering | \bprompting\b | prompt\ (?:injection|tuning)"
    r"| \bagentic\b"
    r"| model\ context\ protocol | \bMCPs?\b"
    r"| vector\ (?:database|db|search) | \bembeddings?\b"
    r"| fine-?tun | \binstructlab\b"
    r"| \bMLOps\b | \bAIOps\b | \bModelOps\b"
    r"| responsible\ AI | AI\ ethics | AI\ governance | AI\ safety"
    r"| trustworthy\ AI | explainable\ AI | \bXAI\b"
    r"| hallucinat"
    r"| \bpytorch\b | \btensorflow\b | \bkeras\b"
    r"| \bSLMs?\b | \bchatbots?\b | \bRoboChat\b"
    r"| \bOpenAI\b | \bAnthropic\b | \bDeepSeek\b | \bPerplexity\b"
    r"| stable\ diffusion | diffusion\ models? | \btransformers?\b"
    r"| \bmultimodal\b"
    r"| speech\ recognition | speech\ to\ text | text\ to\ speech"
    r"| recommender | recommendation\ (?:system|engine|model)"
    r"| anomaly\ detection | \bdeepfakes?\b | deep\ faking | synthetic\ data"
    r"| \bAutoAI\b | hugging\ ?face | \blangchain\b | \bollama\b | \bvllm\b"
    r"| \bBERT\b | \bGANs?\b"
    r"| reinforcement\ learning | supervised\ learning | unsupervised\ learning"
    r"| \bRLHF\b | \bLoRA\b | \bQLoRA\b"
    r"| few-?shot | zero-?shot | chain[-\s]of[-\s]thought"
    r"| \bcognitive\b | \bML\b | \bCopilot\b"
    r"| open[-\s]weight | \bGLMs?\b"
    r"| \bOpenClaw\b | \bClawdbot\b | \bMoltbook\b"
    r"| \bPromptware\b | \bWormGPT\b | \bSearchGPT\b"
    r"| Apple\ Intelligence | \bAlphaFold\b | \bFrontierMath\b"
    r"| \bKNNs?\b | k-?nearest\ neighbou?r | mixture\ of\ experts"
    r"| sentiment\ analysis | bag\ of\ words | \bstemming\b | \blemmatiz"
    r"| back[-\s]?propagation | kolmogorov[-\s]arnold | \bKANs?\b"
    r"| InspectorRAGet | \bKubeflow\b | data\ science"
    r"| \bMLPs?\b | multilayer\ perceptron | gradient\ descent"
    r"| overfitting | underfitting | predictive\ models?"
    r"| text\ mining | data\ mining | autoencoders? | boltzmann"
    r"| random\ forest | \bLSTMs?\b"
    r"| \bOCRs?\b | optical\ character\ recognition"
    r"| text-to-sql | shadow\ agents | vibe\ ?coding | \bdistillation\b"
    r"| mechanistic\ interpretability | \bFMTI\b | \bSam\ Altman\b"
    r"| Thinking\ Machines | Muse\ Spark | NVIDIA\ DIGITS | context\ bombing"
    r"| intelligent\ document | intelligent\ remediation"
    r"| exploratory\ data\ analysis | face\ mask\ detection"
    r"| \bKimi\b | agent\ platform | open-source\ agents"
    r"| watson\s*orchestrate"
)

# Titles that are not clearly AI and not clearly off-topic. The description
# decides these. Everything else on IBM Technology that missed STRONG is excluded.
AMBIGUOUS = re.compile(
    r"(?ix)"
    r"digital\ workers?"
    r"| \bgpus?\b"
    r"| knowledge\ graphs?"
    r"| hyperautomation"
    r"| intelligent\ automation"
    r"| intelligent\ workflows?"
    r"| virtual\ assistants?"
    r"| time\ series\ analysis"
    r"| computers\ program\ computers"
    r"| automated\ code\ repair"
    r"| humanoid"
    r"| \bAP2\b"
    r"| mayflower"
    r"| watson\ data\ platform"
    r"| knowledge\ catalog"
    r"| featuring\ mixture\ of\ experts"
    r"| document\ processing"
    r"| body\ temperature"
)
WATSON_QUERY = re.compile(r"(?i)watson\ query")
WATSON_WORD = re.compile(r"(?i)watsons?")
# Watson-branded data products. The brand alone is not an AI signal.
WEAK_WATSON = re.compile(r"(?i)watson\ data\ platform|knowledge\ catalog")
FEATURING_MOE = re.compile(r"(?i)featuring\ mixture\ of\ experts")
BOILERPLATE = re.compile(
    r"(?i)AI news moves fast|monthly newsletter|sign up for|subscribe to"
)
SHORTS_TITLE = re.compile(r"(?i)#shorts|\bshorts\b")


def reject_symlink(path: Path) -> None:
    if path.is_symlink():
        raise SystemExit(f"refusing symlink in the youtube cache: {path}")


def read_cache_text(path: Path) -> str:
    reject_symlink(path)
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    with os.fdopen(fd, "r", encoding="utf-8") as handle:
        return handle.read()


def write_cache_text(path: Path, text: str) -> None:
    """Write a cache file without following a symlink planted at that path."""
    reject_symlink(path)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)


def prepare_cache(path: Path) -> Path:
    """Create a private cache directory owned by the current user.

    A predictable directory under shared /tmp can be created first by another
    local user. Reusing that directory would follow their symlinks or trust
    their playlist files. Refuse a symlink and any directory this user does
    not own.
    """
    path = path.expanduser()
    if path.is_symlink():
        raise SystemExit(f"refusing symlink cache dir: {path}")
    path.mkdir(parents=True, mode=0o700, exist_ok=True)
    if path.is_symlink() or not path.is_dir():
        raise SystemExit(f"cache path is not a directory: {path}")
    info = path.stat()
    if info.st_uid != os.getuid():
        raise SystemExit(f"cache dir is not owned by the current user: {path}")
    os.chmod(path, 0o700)
    return path


def slugify(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()


def read_channels(path: Path) -> list[tuple[str, str]]:
    found = CHANNEL_LINK.findall(path.read_text())
    if len(found) < 5:
        raise SystemExit(f"expected channel links in {path}, found {len(found)}")
    return found


def yt_dlp_bin() -> str:
    found = shutil.which("yt-dlp")
    if found:
        return found
    local = Path.home() / ".local" / "bin" / "yt-dlp"
    if local.exists():
        return str(local)
    raise SystemExit("yt-dlp is not installed")


def classify_title(title: str) -> str:
    """Return include, exclude, or ambiguous for an IBM Technology title."""
    without_watson = WATSON_WORD.sub("", title)
    if WATSON_QUERY.search(title) and not STRONG.search(without_watson):
        return "exclude"
    if WEAK_WATSON.search(title) and not STRONG.search(without_watson):
        return "ambiguous"
    if STRONG.search(FEATURING_MOE.sub("", title)):
        return "include"
    if AMBIGUOUS.search(title) or WEAK_WATSON.search(title):
        return "ambiguous"
    return "exclude"


def strip_boilerplate(description: str) -> str:
    kept = []
    for line in description.splitlines():
        if BOILERPLATE.search(line):
            continue
        kept.append(line)
    text = "\n".join(kept)
    return re.sub(r"https?://\S+", " ", text)


def description_is_ai(description: str) -> bool:
    """True when the description, not a CTA or a bare #AI tag, is about AI."""
    text = strip_boilerplate(description)
    text = re.sub(r"(?i)#AI\b", " ", text)
    lines = []
    for line in text.splitlines():
        if re.match(r"(?i)\s*learn about watsonx\b", line.strip()):
            continue
        lines.append(line)
    return bool(STRONG.search("\n".join(lines)))


def json_string_at(html: str, marker: str) -> str | None:
    start = html.find(marker)
    if start < 0:
        return None
    i = start + len(marker)
    raw: list[str] = []
    while i < len(html):
        char = html[i]
        if char == "\\":
            raw.append(html[i : i + 2])
            i += 2
            continue
        if char == '"':
            break
        raw.append(char)
        i += 1
    try:
        return json.loads('"' + "".join(raw) + '"')
    except json.JSONDecodeError:
        return None


def fetch_description(video_id: str, cache: Path, pause: float) -> str | None:
    dest = cache / f"{video_id}.txt"
    if dest.is_symlink():
        raise SystemExit(f"refusing symlink in the youtube cache: {dest}")
    if dest.exists():
        text = read_cache_text(dest)
        return None if text == "" else text
    url = f"https://www.youtube.com/watch?v={video_id}"
    last_error = "no description in watch page"
    for attempt in range(4):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                html = response.read().decode("utf-8", "replace")
            text = json_string_at(html, '"attributedDescription":{"content":"')
            if text is None:
                text = json_string_at(html, '"shortDescription":"')
            if text is not None:
                write_cache_text(dest, text)
                time.sleep(pause)
                return text
            last_error = "watch page had no description"
        except Exception as exc:  # noqa: BLE001 - network errors are reported, not fatal
            last_error = str(exc)
        time.sleep(min(30, 2**attempt))
    write_cache_text(cache / f"{video_id}.err", last_error)
    write_cache_text(dest, "")
    return None


def fetch_length_seconds(video_id: str) -> int | None:
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8", "replace")
    except Exception:
        return None
    match = re.search(r'"lengthSeconds":"(\d+)"', html)
    if not match:
        return None
    return int(match.group(1))


def load_playlist(path: Path) -> list[dict]:
    data = json.loads(read_cache_text(path))
    entries = []
    for entry in data.get("entries") or []:
        if not entry:
            continue
        video_id = str(entry.get("id") or "")
        title = (entry.get("title") or "").replace("\xa0", " ").replace("\n", " ").strip()
        url = entry.get("url") or ""
        if not ID_RE.match(video_id):
            entries.append({"skip": "bad-id", "id": video_id, "title": title})
            continue
        if "/shorts/" in url or SHORTS_TITLE.search(title):
            entries.append({"skip": "short", "id": video_id, "title": title})
            continue
        if entry.get("live_status") == "is_upcoming":
            entries.append({"skip": "upcoming", "id": video_id, "title": title})
            continue
        if not title:
            entries.append({"skip": "no-title", "id": video_id, "title": title})
            continue
        entries.append(
            {
                "id": video_id,
                "title": title,
                "duration": entry.get("duration"),
                "live_status": entry.get("live_status"),
            }
        )
    return entries


def fetch_tab(url: str, dest: Path, pause: float) -> None:
    if dest.is_symlink():
        raise SystemExit(f"refusing symlink in the youtube cache: {dest}")
    if dest.exists() and dest.stat().st_size > 20:
        return
    binary = yt_dlp_bin()
    last = ""
    for attempt, client in enumerate(PLAYER_CLIENTS):
        command = [
            binary,
            "--flat-playlist",
            "-J",
            "--ignore-errors",
            "--no-warnings",
            "--sleep-requests",
            str(pause),
            "--retries",
            "3",
            "--extractor-retries",
            "3",
            "--socket-timeout",
            "30",
        ]
        if client:
            command.extend(["--extractor-args", f"youtube:player_client={client}"])
        command.append(url)
        print(f"fetch {url} client={client or 'default'}", flush=True)
        proc = subprocess.run(command, capture_output=True, text=True)
        blob = (proc.stderr or "") + (proc.stdout or "")
        last = blob[-2000:]
        if proc.returncode == 0 and (proc.stdout or "").strip().startswith("{"):
            write_cache_text(dest, proc.stdout)
            return
        if re.search(r"does not have|no videos|This channel has no|playlist does not exist", blob, re.I):
            write_cache_text(dest, json.dumps({"entries": [], "note": "empty tab"}))
            return
        time.sleep(min(60, 2**attempt))
    write_cache_text(dest, json.dumps({"entries": [], "error": last}))


def catalog_dump(entries: list[dict]) -> str:
    parts = [json.dumps(entry, indent=2, ensure_ascii=False) for entry in entries]
    return "[\n" + ",\n".join(parts) + "\n]"


def self_check() -> None:
    cases = {
        "What is Kubernetes?": "exclude",
        "What is a VPN?": "exclude",
        "What Is Quantization? How AI Models Get Smaller & Faster": "include",
        "What is Retrieval-Augmented Generation (RAG)?": "include",
        "IBM Cloud Now: IBM Watson Query, Netezza, and IBM Cloud Satellite + Alibaba Cloud": "exclude",
        "What is a Knowledge Graph?": "ambiguous",
        "What is Watson Data Platform?": "ambiguous",
        "IBM Watson Knowledge Catalog (formerly Data Catalog)": "ambiguous",
        "GPUs: Explained": "ambiguous",
        "What is Mixture of Experts?": "include",
        "Is open source safe? Featuring Mixture of Experts": "ambiguous",
        "What is the K-Nearest Neighbor (KNN) Algorithm?": "include",
        "Introducing IBM AI Academy": "include",
    }
    if description_is_ai("Learn about watsonx:\n\nMartin explains time series analysis.\n#arima #pandas"):
        raise SystemExit("time series CTA should not count as AI")
    if description_is_ai("Alex explains what a GPU is.\n#GPU #HPC #AI"):
        raise SystemExit("a bare #AI hashtag should not count as AI")
    if not description_is_ai("AI-powered virtual assistants keep customers happy.\n#chatbot"):
        raise SystemExit("virtual assistants description should count as AI")
    if not description_is_ai("Jon discusses digital workers.\n#digitalworker #watsonorchestrate"):
        raise SystemExit("Watson Orchestrate digital workers should count as AI")
    for title, expected in cases.items():
        got = classify_title(title)
        if got != expected:
            raise SystemExit(f"classifier self-check failed for {title!r}: {got} != {expected}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--pause", type=float, default=1.0, help="seconds between YouTube requests")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    self_check()

    cache = prepare_cache(args.cache_dir)
    desc_cache = prepare_cache(cache / "descriptions")

    channels = read_channels(CHANNEL_QMD)
    catalog = json.loads(CATALOG_PATH.read_text())
    existing_ids = [entry["video_id"] for entry in catalog]
    if len(existing_ids) != len(set(existing_ids)):
        raise SystemExit("existing catalog has duplicate video ids")
    known = set(existing_ids)

    report_channels = []
    new_entries: list[dict] = []
    seen = set(known)
    ibm_excluded: list[dict] = []
    ibm_ambiguous: list[dict] = []
    failures: list[str] = []
    kept_short_duration: list[dict] = []

    for name, channel_id in channels:
        slug = slugify(name)
        tab_entries: list[dict] = []
        tab_counts = {}
        for tab in ("videos", "streams"):
            dest = cache / f"{slug}.{tab}.json"
            url = f"https://www.youtube.com/channel/{channel_id}/{tab}"
            if not dest.exists():
                fetch_tab(url, dest, args.pause)
                time.sleep(args.pause)
            raw = json.loads(read_cache_text(dest))
            if raw.get("error"):
                failures.append(f"{name} {tab}: {raw['error'][:180]}")
            parsed = load_playlist(dest)
            tab_counts[tab] = {
                "listed": len(parsed),
                "skipped_short": sum(1 for item in parsed if item.get("skip") == "short"),
                "skipped_upcoming": sum(1 for item in parsed if item.get("skip") == "upcoming"),
                "skipped_other": sum(1 for item in parsed if item.get("skip") in {"bad-id", "no-title"}),
            }
            tab_entries.extend(item for item in parsed if "skip" not in item)

        existing = 0
        added = 0
        included = 0
        excluded = 0
        counted_existing: set[str] = set()

        def resolve_ibm(item: dict) -> str:
            decision = classify_title(item["title"])
            if decision != "ambiguous":
                return decision
            description = fetch_description(item["id"], desc_cache, args.pause)
            if description is None:
                decision = "unresolved"
                failures.append(f"IBM description unavailable for {item['id']}: {item['title']}")
            elif description_is_ai(description):
                decision = "include"
            else:
                decision = "exclude"
            ibm_ambiguous.append({**item, "decision": decision})
            return decision

        for item in tab_entries:
            video_id = item["id"]
            if video_id in known:
                if video_id in counted_existing:
                    continue
                counted_existing.add(video_id)
                existing += 1
                if channel_id == IBM_CHANNEL_ID:
                    decision = resolve_ibm(item)
                    if decision == "include":
                        included += 1
                    else:
                        excluded += 1
                        ibm_excluded.append({**item, "decision": decision, "kept_existing": True})
                continue
            if video_id in seen:
                continue
            if channel_id == IBM_CHANNEL_ID:
                decision = resolve_ibm(item)
                if decision != "include":
                    excluded += 1
                    ibm_excluded.append({**item, "decision": decision})
                    seen.add(video_id)
                    continue
                included += 1
            duration = item.get("duration")
            if isinstance(duration, (int, float)) and duration <= 60:
                kept_short_duration.append({"channel": name, **item})
            new_entries.append(
                {
                    "video_id": video_id,
                    "title": item["title"],
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "transcript": None,
                    "summary": None,
                }
            )
            seen.add(video_id)
            added += 1
        report_channels.append(
            {
                "channel": name,
                "channel_id": channel_id,
                "existing": existing,
                "added": added,
                "total": existing + added,
                "tabs": tab_counts,
                "ibm_included": included if channel_id == IBM_CHANNEL_ID else None,
                "ibm_excluded": excluded if channel_id == IBM_CHANNEL_ID else None,
            }
        )
        print(
            f"{name}: existing={existing} added={added} total={existing + added}",
            flush=True,
        )

    merged = catalog + new_entries
    ids = [entry["video_id"] for entry in merged]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate video id in merged catalog")
    if any(not ID_RE.match(video_id) for video_id in ids):
        raise SystemExit("invalid video id in merged catalog")
    for entry in new_entries:
        if list(entry.keys()) != ["video_id", "title", "url", "transcript", "summary"]:
            raise SystemExit("new entry keys drifted from the catalog template")

    # Pre-existing rows that are not on these Videos/Live tabs. Durations already
    # seen on those tabs are long-form. Probe the rest so Shorts can be noted.
    on_tabs = set()
    for name, _channel_id in channels:
        slug = slugify(name)
        for tab in ("videos", "streams"):
            path = cache / f"{slug}.{tab}.json"
            if path.exists():
                for item in load_playlist(path):
                    if "skip" not in item:
                        on_tabs.add(item["id"])
    preexisting_shorts = []
    preexisting_unknown = []
    for entry in catalog:
        video_id = entry["video_id"]
        if video_id in on_tabs:
            continue
        if "/shorts/" in entry.get("url", ""):
            preexisting_shorts.append({**entry, "reason": "shorts url"})
            continue
        length = fetch_length_seconds(video_id)
        time.sleep(args.pause)
        if length is None:
            preexisting_unknown.append(video_id)
        elif length <= 60:
            preexisting_shorts.append({**entry, "duration": length, "reason": "duration<=60"})

    text = catalog_dump(merged)
    json.loads(text)
    if not args.dry_run:
        CATALOG_PATH.write_text(text)
    report = {
        "catalog_before": len(catalog),
        "catalog_after": len(merged),
        "added": len(new_entries),
        "bytes": len(text.encode()),
        "channels": report_channels,
        "ibm_ambiguous": ibm_ambiguous,
        "kept_short_duration": kept_short_duration,
        "preexisting_shorts": preexisting_shorts,
        "preexisting_duration_unknown": preexisting_unknown,
        "failures": failures,
        "dry_run": args.dry_run,
    }
    write_cache_text(cache / "report.json", json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps({k: report[k] for k in ("catalog_before", "catalog_after", "added", "bytes")}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
