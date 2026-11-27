# Fetching YouTube transcripts with yt-dlp

Notes for **yt-dlp 2026.11.23**, checked on this machine with
`yt-dlp --version`. Node was v22.23.4 at `/exec-daemon/node`. Deno was not
installed. `youtube-transcript-api` 1.2.5 was used only after yt-dlp failed.

The proof of concept is Julia Turc, [How is hardware reshaping LLM design?](https://www.youtube.com/watch?v=BSzhrZOp2x8)
(`BSzhrZOp2x8`, published 2026-03-03, 22 minutes 46 seconds, channel
`UCMUy_WsUIYbM_hKR9drb9dA`). It is a regular video, not a Short. The cleaned
transcript is
[`videos/transcripts/transcript_BSzhrZOp2x8.md`](videos/transcripts/transcript_BSzhrZOp2x8.md).

yt-dlp never returned a caption file from this VM. YouTube answered every
player client with a sign-in bot check. The saved text is the manual English
track from the public [youtubegpt](https://youtubegpt.ai/youtube-transcript-api/)
transcript API (`caption_source: manual`, `method: youtubegpt`). The chain
stopped there because that response included timestamps. Raw VTT stayed in
`/tmp` and is not in the repo.

`YT_PROXY` was unset, so the proxied retry in the skill was skipped.

## Listing tracks

```bash
yt-dlp --no-playlist --list-subs \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

When extraction works, yt-dlp prints two lists:

- **Available subtitles** are manual tracks. `kind` is absent on the caption
  track. Download them with `--write-subs`.
- **Available automatic captions** are speech-recognition tracks. `kind` is
  `asr`. Download them with `--write-auto-subs` (alias
  `--write-automatic-subs`).

`--list-subs` simulates a download. It does not write a subtitle file unless
you also pass `--no-simulate`.

This run never reached either list. The first command was:

```bash
yt-dlp --no-playlist --list-subs \
  --retries 5 --retry-sleep exp=2:60 \
  "https://www.youtube.com/watch?v=BSzhrZOp2x8"
```

```text
[youtube] Extracting URL: https://www.youtube.com/watch?v=BSzhrZOp2x8
[youtube] BSzhrZOp2x8: Downloading webpage
WARNING: [youtube] No supported JavaScript runtime could be found. Only deno is enabled by default; to use another runtime add  --js-runtimes RUNTIME[:PATH]  to your command/config. YouTube extraction without a JS runtime has been deprecated, and some formats may be missing. See  https://github.com/yt-dlp/yt-dlp/wiki/EJS  for details on installing one
[youtube] BSzhrZOp2x8: Downloading visionos player API JSON
WARNING: [youtube] No title found in player responses; falling back to title from initial data. Other metadata may also be missing
ERROR: [youtube] BSzhrZOp2x8: Sign in to confirm you’re not a bot. This helps protect our community. Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp  for how to manually pass cookies. Also see  https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies  for tips on effectively exporting YouTube cookies
```

Exit code 1. `--dump-single-json` on the same URL exited 1 with the same
warning and the same bot error, so there was no metadata JSON either.

In 2026.11.23 only Deno is enabled by default
(`--js-runtimes RUNTIME[:PATH]` in `--help`). Supported runtimes, highest
priority first, are deno, node, quickjs, and bun. Retrying with Node removed
the runtime warning and still failed:

```bash
yt-dlp --no-playlist --list-subs \
  --js-runtimes "node:/exec-daemon/node" \
  --retries 5 --retry-sleep exp=2:60 \
  "https://www.youtube.com/watch?v=BSzhrZOp2x8"
```

```text
[youtube] Extracting URL: https://www.youtube.com/watch?v=BSzhrZOp2x8
[youtube] BSzhrZOp2x8: Downloading webpage
[youtube] BSzhrZOp2x8: Downloading tv samsung player API JSON
[youtube] BSzhrZOp2x8: Downloading visionos player API JSON
WARNING: [youtube] No title found in player responses; falling back to title from initial data. Other metadata may also be missing
ERROR: [youtube] BSzhrZOp2x8: Sign in to confirm you’re not a bot. This helps protect our community. Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp  for how to manually pass cookies. Also see  https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies  for tips on effectively exporting YouTube cookies
```

## Manual and automatic captions

Pass one of these, not both, when you want a single kind of track:

```bash
yt-dlp --no-playlist --skip-download --write-subs \
  --sub-langs "en.*" --sub-format vtt \
  --retries 5 --retry-sleep exp=2:60 \
  -o "/tmp/yt-%(id)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

```bash
yt-dlp --no-playlist --skip-download --write-auto-subs \
  --sub-langs "en-orig,en.*,en" --sub-format vtt \
  --retries 5 --retry-sleep exp=2:60 \
  -o "/tmp/yt-%(id)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

`--write-subs` reads the manual dictionary (`subtitles` in the info JSON).
`--write-auto-subs` reads `automatic_captions`. In this version's YouTube
extractor, a track with `kind != "asr"` is manual. An `asr` track is
automatic. For the original spoken language, the extractor also stores that
automatic track under a `lang-orig` code, for example `en-orig`, labeled
"English (Original)", and it keeps a copy without the `-orig` suffix.

This VM did not get as far as writing a VTT. `--list-subs` and
`--dump-single-json` failed in the player response, before any subtitle URL
was fetched, so the `--write-subs` form above was not run as a second call.
It uses the same player extraction that already returned the bot check.

## `--sub-langs`

From `--help` in 2026.11.23: languages can be a regex, or `all`, separated
by commas. Prefix a code with `-` to drop it, as in `all,-live_chat`.

`en.*` is a full match against the language tag. It matches `en`, `en-US`,
`en-GB`, and `en-orig`. Quote it so the shell does not expand `*`.

The comma list is a priority order, and this version downloads **every** tag
that matches, not only the first. `orderedSet_from_options` walks the
patterns and keeps each matching tag once. Putting `en-orig` before `en.*`
makes the original automatic track sort first. `en.*` already matches both
`en-orig` and `en`, so the extra `en` at the end does not add a language.
Record the file you actually keep. Prefer the manual English track, then
`en-orig`, then `en`.

## `--sub-format` and `--convert-subs`

`--sub-format` is a preference list split on `/`, for example `vtt` or
`vtt/json3/best`. The YouTube extractor in this version offers:

`json3`, `srv1`, `srv2`, `srv3`, `ttml`, `srt`, `vtt`

(`_SUBTITLE_FORMATS` in `yt_dlp/extractor/youtube/_video.py`). `--sub-format
vtt` selects the `vtt` entry. `best`, or a format the track does not have,
falls through to the last listed format and prints a warning.

| Format | What it is |
| --- | --- |
| `vtt` | WebVTT cues. This is what the skill saves and what `scripts/vtt_to_transcript.py` reads. Automatic tracks use overlapping rolling cues. |
| `srv3` | YouTube's timed-text XML. Word timing is in attributes on the text runs. |
| `json3` | JSON events with `tStartMs` and `segs[].utf8`. Skip events that have no `segs`. A rolling auto track still repeats words across events. |
| `srt` | SubRip. YouTube can serve it directly. `--convert-subs srt` can also build it from whatever was downloaded. |

`--convert-subs` is a post-processor, separate from `--sub-format`. In this
version the conversion targets are `ass`, `lrc`, `srt`, and `vtt`. The
default is no conversion (`--convert-subs none`). Example:

```bash
yt-dlp --no-playlist --skip-download --write-auto-subs \
  --sub-langs "en-orig" --sub-format vtt --convert-subs srt \
  -o "/tmp/yt-%(id)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

That still has to download a source track before it writes the SRT. It was
not run here, because the player call never returned a track.

## `--skip-download` and `-o`

`--skip-download` (alias `--no-download`) does not download the video. It
still writes the related files you asked for, including subtitles.
`--simulate` writes nothing. Use `--skip-download` when you want the VTT and
not the media.

`-o` is the output template. `-o "/tmp/yt-%(id)s"` sets the base name.
`subtitles_filename` then appends the language and the extension, so a saved
English VTT lands at `/tmp/yt-VIDEO_ID.en.vtt` (or `.en-orig.vtt`). Delete
that file after the markdown is written. Do not commit it.

## Player clients, cookies, proxy, and rate limits

Change one thing at a time after a bot check, a 403, an empty caption list,
or a log line that says subtitles were discarded because a PO token was not
provided. This run's log never mentioned a PO token. The failure was the
sign-in check. The PO token cases are described in the
[yt-dlp PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide).

Once a client returns a track list, subtitle download is the same extractor
argument plus `--skip-download --write-subs --write-auto-subs`. On this run
every client died in the player call, so each retry was `--list-subs` only.
The `tv` command that was actually run:

```bash
yt-dlp --no-playlist --list-subs \
  --js-runtimes "node:/exec-daemon/node" \
  --extractor-args "youtube:player_client=tv" \
  --retries 5 --retry-sleep exp=2:60 \
  "https://www.youtube.com/watch?v=BSzhrZOp2x8"
```

The other clients used that command with `player_client` set to `web_safari`,
`android`, `ios`, and `mweb`. Waits between YouTube attempts followed the
skill's backoff, from 5 seconds up to 60. `ios` and `mweb` were 20 seconds
apart, after the cookie lookup failed on this machine without contacting
YouTube.

| Client | What the log added | Result |
| --- | --- | --- |
| `tv` | `Downloading tv client config`, `Downloading player b485e332-tv`, `Downloading tv player API JSON` | Same bot error, including "This helps protect our community." |
| `web_safari` | `Downloading web safari client config`, `Downloading web safari player API JSON` | Same bot error |
| `android` | `Downloading android player API JSON` | Bot error, without the "This helps protect our community" sentence |
| `ios` | `Downloading ios player API JSON` | Same shorter bot error as `android` |
| `mweb` | `Downloading mweb client config`, `Downloading mweb player API JSON` | Same bot error as the web clients |

The `tv` listing, in full:

```text
[youtube] Extracting URL: https://www.youtube.com/watch?v=BSzhrZOp2x8
[youtube] BSzhrZOp2x8: Downloading webpage
[youtube] BSzhrZOp2x8: Downloading tv client config
[youtube] BSzhrZOp2x8: Downloading player b485e332-tv
[youtube] BSzhrZOp2x8: Downloading tv player API JSON
WARNING: [youtube] No title found in player responses; falling back to title from initial data. Other metadata may also be missing
ERROR: [youtube] BSzhrZOp2x8: Sign in to confirm you’re not a bot. This helps protect our community. Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp  for how to manually pass cookies. Also see  https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies  for tips on effectively exporting YouTube cookies
```

Browser cookies stay on this machine's own network, and they stay off the
proxy. Chrome is installed here, and it has no profile:

```bash
yt-dlp --no-playlist --skip-download --write-subs --write-auto-subs \
  --sub-langs "en-orig,en.*,en" --sub-format vtt \
  --cookies-from-browser chrome \
  --proxy "" \
  --js-runtimes "node:/exec-daemon/node" \
  --retries 5 --retry-sleep exp=2:60 \
  -o "/tmp/yt-%(id)s" \
  "https://www.youtube.com/watch?v=BSzhrZOp2x8"
```

```text
Extracting cookies from chrome
ERROR: could not find chrome cookies database in "/home/ubuntu/.config/google-chrome"
```

`--proxy ""` forces a direct connection when a yt-dlp config file sets a
proxy. `--help` describes `--proxy URL` as an HTTP, HTTPS, or SOCKS proxy.
There was no cookie database to send, and `YT_PROXY` was empty, so the
residential-proxy command was not run.

Rate limits from `--help`:

- `--retries 5` and `--retry-sleep exp=2:60` are what the skill puts on every
  yt-dlp command. The default retry count in this version is 10.
- `--sleep-requests SECONDS` waits between requests during extraction.
- `--sleep-subtitles SECONDS` waits before each subtitle download.
- The preset alias `-t sleep` expands to `--sleep-subtitles 5 --sleep-requests 0.75`.

A 429, "Sign in to confirm you're not a bot", `RequestBlocked`, or
`IpBlocked` is a block. Back off. A tight loop makes the block worse.

## Why automatic VTT repeats itself

YouTube's automatic captions are a rolling window. Each cue is the line on
screen at that moment, not a new sentence. The next cue overlaps the
previous one, drops a word from the front, and adds a word at the end. A
manual track does not do this. The manual VTT for this video, fetched later
from youtubegpt, starts like this:

```text
WEBVTT

00:00:00.138 --> 00:00:05.975
One quadrillion floating point operations per second, or 1000 TFLOPs per second.

00:00:06.575 --> 00:00:10.475
That's the peak compute throughput of an NVIDIA H100 GPU.
```

Those two cues share no words. Joining them with a space is enough.

An automatic track looks more like the fixture below. It is the rolling
shape, written out so the cleaner can be checked. It is not a file yt-dlp
saved on this run. No raw automatic VTT was available: yt-dlp was blocked,
and the track that was saved is the manual one.

```text
WEBVTT

00:00:00.000 --> 00:00:01.500
memory bandwidth

00:00:00.400 --> 00:00:02.000
memory bandwidth caps

00:00:00.900 --> 00:00:02.600
bandwidth caps decode

00:00:01.400 --> 00:00:03.200
caps decode speed

00:00:02.000 --> 00:00:04.000
decode speed here.
```

Read left to right, the new words are `memory`, `bandwidth`, `caps`,
`decode`, `speed`, `here.` Naive concatenation prints "memory bandwidth"
five times.

`scripts/vtt_to_transcript.py` keeps the longest suffix of the previous cue
that is a prefix of the current cue, appends only the new words, and stamps
them with the cue that introduced them. It then groups the result into
paragraphs of about 20–45 seconds, breaking at a sentence boundary once the
paragraph is at least 20 seconds, or at 45 seconds if the sentence is still
open. A cue that starts with punctuation stays attached to the previous
sentence. That happens in this video's manual track: one cue is
`decoding step, which is the bottleneck` and the next cue starts with
`. You might`.

```bash
python3 scripts/vtt_to_transcript.py --min-seconds 1 --max-seconds 30 /tmp/yt-poc/rolling.vtt
```

```text
[00:00] memory bandwidth caps decode speed here.
```

The same script with the default 20–45 second window turned the manual VTT
into the 51 paragraphs in the transcript file:

```bash
python3 scripts/vtt_to_transcript.py /tmp/yt-poc/manual.vtt
```

The one caption edit after that pass is in the source line of the transcript:
the manual cue says "auto aggressive", and the markdown says "auto-regressive".

## What worked after yt-dlp

Same video, same fallback order as the skill.

`youtube-transcript-api` 1.2.5 raised `RequestBlocked`:

```text
RequestBlocked
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=BSzhrZOp2x8! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.
```

The proxied form of that call was skipped because `YT_PROXY` was unset.

The watch page returned HTTP 200 and a player response
(`INNERTUBE_CLIENT_VERSION` `2.20261125.00.00`). `playabilityStatus` was
`LOGIN_REQUIRED` with reason "Sign in to confirm you’re not a bot", and the
page had no `captionTracks`. The WEB and ANDROID Innertube player calls
returned the same status, zero tracks, and no title.

Public pages that did not return speech: `youtubetotranscript.com` HTTP 403,
`kome.ai` HTTP 429, and HTML shells from Tactiq and DownSub.
`inv.nadeko.net` listed an English track and an English (auto-generated)
track, then returned an empty body for both VTT URLs.

The call that returned speech was:

```text
GET https://youtubegpt.ai/api/transcript?v=BSzhrZOp2x8&format=json&lang=en
```

HTTP 200, `Cache-Control: public, max-age=3600`, 358 segments. The chosen
track was `{language: en, name: English, generated: false}`. The other
listed track was English (auto-generated). Duration 1366 seconds. Title and
channel matched the channel feed. A second request with `format=vtt` returned
the manual WebVTT quoted above. `generated=1` was ignored and returned the
same manual JSON. Because the segments have start times, the chain stops.
Audio was not downloaded, and Whisper was not run.

## Catalog row

`BSzhrZOp2x8` is not in `sources/youtube/video-id.json` on `main`. It is on
the open catalog branch `cursor/sync-youtube-catalog-0b0e` (PR #36), with
`transcript` and `summary` still null. That pull request appends thousands of
lines to `video-id.json`. This proof of concept does not edit that file, so
the two branches do not both change the end of the array.

After PR #36 lands, point the existing row at the files saved here:

```json
{
  "video_id": "BSzhrZOp2x8",
  "title": "How is hardware reshaping LLM design?",
  "url": "https://www.youtube.com/watch?v=BSzhrZOp2x8",
  "transcript": "sources/youtube/videos/transcripts/transcript_BSzhrZOp2x8.md",
  "summary": "sources/youtube/videos/BSzhrZOp2x8.md"
}
```
