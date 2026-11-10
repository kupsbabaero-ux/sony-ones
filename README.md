# Sony Channels EPG Auto-Updater

Weekly EPG (XMLTV) for these channels with **daily auto-update** via GitHub Actions:

- Sony Cine
- Sony Movies Channel
- Sony One Comedy Hits
- Sony One Action Hits
- Sony One Comedy TV
- Sony One Faves
- Sony One Thriller TV

## Features

- Generates clean XMLTV (`epg/sony-epg.xml` + `.gz`)
- Covers **7 days** of schedule
- Runs **every day** (00:30 UTC) via GitHub Actions
- You can also trigger manually
- Ready for TiviMate, OTT Navigator, IPTV Smarters, Kodi, etc.

## How to use (quick)

1. **Fork** this repository (or upload the zip to a new repo)
2. Go to **Actions** tab → enable workflows
3. Wait for the first run (or click **Run workflow**)
4. After success, use this URL as your EPG source:

```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/epg/sony-epg.xml
```

or the compressed version:

```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/epg/sony-epg.xml.gz
```

## Channel IDs (for your M3U)

```
SonyCine
SonyMoviesChannel
SonyOneComedyHits
SonyOneActionHits
SonyOneComedyTV
SonyOneFaves
SonyOneThrillerTV
```

Example M3U line:

```
#EXTINF:-1 tvg-id="SonyCine" tvg-name="Sony Cine" tvg-logo="" group-title="Movies",Sony Cine
http://your-stream-url
```

## Local generation

```bash
python scripts/generate_epg.py
```

## Notes

- Schedules are **theme-based sample programs** (movies/series typical for each channel).
- For real accurate live EPG of FAST channels (Samsung TV Plus / LG), you need official sources or paid EPG services.
- You can edit `scripts/generate_epg.py` to improve titles, add real descriptions, or integrate other sources later.

## License

MIT – free to use and modify.
