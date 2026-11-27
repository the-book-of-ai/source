#!/usr/bin/env python3
"""Turn a WebVTT caption file into timestamped transcript paragraphs.

YouTube automatic captions repeat a growing line across overlapping cues.
Each cue is the current on-screen window, not a new sentence, so the same
words appear again in the next cue. This script keeps each word once, then
groups the remaining speech into paragraphs of about 20-45 seconds.

Write the markdown only. Leave the raw VTT in a temp directory.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


TAG_RE = re.compile(r"<[^>]+>")
TIMESTAMP_RE = re.compile(
    r"(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})"
)


def parse_timestamp(value: str) -> float:
    match = TIMESTAMP_RE.search(value.strip())
    if not match:
        raise ValueError(f"not a VTT timestamp: {value!r}")
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    millis = int(match.group(4))
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def clean_cue(text: str) -> str:
    """Drop literal WebVTT tags, then escape the cue for Markdown.

    Tags such as ``<c>`` and ``<00:00:01.000>`` are real markup in the file,
    so they are removed before HTML entities are decoded. A spoken comparison
    is stored as ``&lt;`` and must survive. Decoding first and then deleting
    everything between angle brackets would turn ``a &lt; b and c &gt; d``
    into ``a d``. After decoding, ``<``, ``>``, and ``&`` are escaped so a
    caption cannot become raw HTML. Backslashes and square brackets are
    escaped too, so ``[label](https://example)`` and ``![alt](url)`` stay
    text instead of a Markdown link or image.
    """
    text = TAG_RE.sub("", text)
    previous = None
    while previous != text:
        previous = text
        text = html.unescape(text)
    text = text.replace("\u00a0", " ")
    text = " ".join(text.split())
    text = html.escape(text, quote=False)
    return (
        text.replace("\\", "\\\\")
        .replace("[", "\\[")
        .replace("]", "\\]")
    )


def parse_vtt(raw: str) -> list[tuple[float, float, str]]:
    """Return (start_seconds, end_seconds, cue_text) for every non-empty cue."""
    cues: list[tuple[float, float, str]] = []
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if "-->" not in line:
            index += 1
            continue
        start_text, end_text = line.split("-->", 1)
        start = parse_timestamp(start_text)
        end = parse_timestamp(end_text)
        index += 1
        parts: list[str] = []
        while index < len(lines) and lines[index].strip():
            parts.append(lines[index].strip())
            index += 1
        text = clean_cue(" ".join(parts))
        if text:
            cues.append((start, end, text))
    return cues


def new_words(previous: list[str], current: list[str]) -> list[str]:
    """Drop the longest suffix of previous that is a prefix of current."""
    limit = min(len(previous), len(current))
    for size in range(limit, 0, -1):
        if previous[-size:] == current[:size]:
            return current[size:]
    return current


def dedupe_cues(cues: list[tuple[float, float, str]]) -> list[tuple[float, str]]:
    """Collapse rolling auto-caption windows. Keep the first time a word appears.

    Only cues that overlap in time are windows of the same line. A later cue
    that merely starts with a word the previous cue ended on is new speech,
    including a repetition, and stays intact.
    """
    pieces: list[tuple[float, str]] = []
    previous: list[str] = []
    previous_end: float | None = None
    for start, end, text in cues:
        words = text.split()
        if not words:
            continue
        overlapping = previous_end is not None and start < previous_end
        fresh = new_words(previous, words) if overlapping else words
        if fresh:
            pieces.append((start, " ".join(fresh)))
        previous = words
        previous_end = end
    return pieces


def format_stamp(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def ends_sentence(text: str) -> bool:
    stripped = text.rstrip().rstrip("\"'”")
    return bool(stripped) and stripped[-1] in ".?!"


def join_chunks(chunks: list[str]) -> str:
    """Join cue text. A cue that starts with punctuation stays attached."""
    text = chunks[0]
    for chunk in chunks[1:]:
        if chunk[:1] in ".,;:!?":
            text += chunk
        else:
            text += " " + chunk
    return " ".join(text.split())


def paragraphs(
    pieces: list[tuple[float, str]],
    min_seconds: float = 20,
    max_seconds: float = 45,
) -> list[tuple[float, str]]:
    """Group consecutive pieces into roughly min_seconds–max_seconds paragraphs.

    Break at a sentence boundary once the paragraph has reached min_seconds.
    Break at max_seconds even if the sentence is still open.
    """
    grouped: list[tuple[float, str]] = []
    start: float | None = None
    chunks: list[str] = []
    for moment, text in pieces:
        if start is None:
            start = moment
        chunks.append(text)
        span = moment - start
        text_so_far = join_chunks(chunks)
        if (span >= min_seconds and ends_sentence(text)) or span >= max_seconds:
            grouped.append((start, text_so_far))
            start = None
            chunks = []
    if chunks and start is not None:
        grouped.append((start, join_chunks(chunks)))
    return grouped


def render(
    raw: str,
    min_seconds: float = 20,
    max_seconds: float = 45,
    manual: bool = False,
) -> str:
    cues = parse_vtt(raw)
    if manual:
        pieces = [(start, text) for start, _end, text in cues]
    else:
        pieces = dedupe_cues(cues)
    blocks = paragraphs(pieces, min_seconds=min_seconds, max_seconds=max_seconds)
    lines = [f"[{format_stamp(start)}] {text}" for start, text in blocks]
    return "\n\n".join(lines) + ("\n" if lines else "")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vtt", type=Path, help="WebVTT file to convert")
    parser.add_argument(
        "--min-seconds",
        type=float,
        default=20,
        help="start a new paragraph at a sentence boundary after this many seconds",
    )
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=45,
        help="start a new paragraph once a cue begins this far from the paragraph start",
    )
    parser.add_argument(
        "--manual",
        action="store_true",
        help="keep every cue; do not collapse overlapping automatic-caption windows",
    )
    args = parser.parse_args(argv)
    raw = args.vtt.read_text(encoding="utf-8")
    sys.stdout.write(
        render(
            raw,
            min_seconds=args.min_seconds,
            max_seconds=args.max_seconds,
            manual=args.manual,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
