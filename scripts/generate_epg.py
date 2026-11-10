#!/usr/bin/env python3
"""
Generate XMLTV EPG for Sony channels (14 days).
Runs daily via GitHub Actions.
"""

from datetime import datetime, timedelta, timezone
import gzip
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Output paths
ROOT = Path(__file__).resolve().parent.parent
EPG_DIR = ROOT / "epg"
EPG_DIR.mkdir(parents=True, exist_ok=True)
XML_PATH = EPG_DIR / "sony-epg.xml"
GZ_PATH = EPG_DIR / "sony-epg.xml.gz"

# Channels definition
CHANNELS = [
    {
        "id": "SonyCine",
        "name": "Sony Cine",
        "icon": "https://i.imgur.com/placeholder-sony-cine.png",
        "category": "Movies",
        "programs": [
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
        ],
    },
    {
        "id": "SonyMoviesChannel",
        "name": "Sony Movies Channel",
        "icon": "https://i.imgur.com/placeholder-sony-movies.png",
        "category": "Movies",
        "programs": [
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
            ("To Be Announced", "Movies", 120),
        ],
    },
    {
        "id": "SonyOneComedyHits",
        "name": "Sony One Comedy Hits",
        "icon": "https://i.imgur.com/placeholder-comedy-hits.png",
        "category": "Comedy",
        "programs": [
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
        ],
    },
    {
        "id": "SonyOneActionHits",
        "name": "Sony One Action Hits",
        "icon": "https://i.imgur.com/placeholder-action-hits.png",
        "category": "Action",
        "programs": [
            ("To Be Announced", "Action", 120),
            ("To Be Announced", "Action", 120),
            ("To Be Announced", "Action", 120),
            ("To Be Announced", "Action", 120),
            ("To Be Announced", "Action", 120),
            ("To Be Announced", "Action", 120),
        ],
    },
    {
        "id": "SonyOneComedyTV",
        "name": "Sony One Comedy TV",
        "icon": "https://i.imgur.com/placeholder-comedy-tv.png",
        "category": "Comedy",
        "programs": [
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
            ("To Be Announced", "Comedy", 120),
        ],
    },
    {
        "id": "SonyOneFaves",
        "name": "Sony One Faves",
        "icon": "https://i.imgur.com/placeholder-faves.png",
        "category": "Series",
        "programs": [
            ("To Be Announced", "Series", 120),
            ("To Be Announced", "Series", 120),
            ("To Be Announced", "Series", 120),
            ("To Be Announced", "Series", 120),
            ("To Be Announced", "Series", 120),
            ("To Be Announced", "Series", 120),
        ],
    },
    {
        "id": "SonyOneThrillerTV",
        "name": "Sony One Thriller TV",
        "icon": "https://i.imgur.com/placeholder-thriller.png",
        "category": "Thriller",
        "programs": [
            ("To Be Announced", "Thriller", 120),
            ("To Be Announced", "Thriller", 120),
            ("To Be Announced", "Thriller", 120),
            ("To Be Announced", "Thriller", 120),
            ("To Be Announced", "Thriller", 120),
            ("To Be Announced", "Thriller", 120),
        ],
    },
]


def fmt_time(dt: datetime) -> str:
    """XMLTV time format: YYYYMMDDHHMMSS +0000"""
    return dt.strftime("%Y%m%d%H%M%S +0000")


def prettify(elem: ET.Element) -> str:
    rough = ET.tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")


def generate():
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    # Start from beginning of today UTC
    start_day = now.replace(hour=0)

    tv = ET.Element("tv")
    tv.set("generator-info-name", "sony-epg-auto")
    tv.set("generator-info-url", "https://github.com/yourusername/sony-epg-auto")

    # Channels
    for ch in CHANNELS:
        channel = ET.SubElement(tv, "channel", id=ch["id"])
        dn = ET.SubElement(channel, "display-name")
        dn.text = ch["name"]
        if ch.get("icon"):
            ET.SubElement(channel, "icon", src=ch["icon"])

    # Programmes – 14 days, continuous rotation
    for ch in CHANNELS:
        programs = ch["programs"]
        current = start_day
        prog_idx = 0

        # Fill 14 full days
        end = start_day + timedelta(days=14)

        while current < end:
            title, category, duration_min = programs[prog_idx % len(programs)]
            stop = current + timedelta(minutes=duration_min)

            programme = ET.SubElement(
                tv,
                "programme",
                start=fmt_time(current),
                stop=fmt_time(stop),
                channel=ch["id"],
            )
            t = ET.SubElement(programme, "title", lang="en")
            t.text = title

            cat = ET.SubElement(programme, "category", lang="en")
            cat.text = category.split("·")[0].strip()

            current = stop
            prog_idx += 1

    # Write XML
    xml_str = prettify(tv)
    # Remove extra blank lines from minidom
    lines = [line for line in xml_str.splitlines() if line.strip()]
    clean_xml = "\n".join(lines) + "\n"

    XML_PATH.write_text(clean_xml, encoding="utf-8")
    print(f"Written: {XML_PATH}")

    # Also write gzipped
    with gzip.open(GZ_PATH, "wt", encoding="utf-8") as f:
        f.write(clean_xml)
    print(f"Written: {GZ_PATH}")

    print(f"Channels: {len(CHANNELS)}")
    print(f"Coverage: {start_day.date()} → {(start_day + timedelta(days=13)).date()} (UTC)")


if __name__ == "__main__":
    generate()
