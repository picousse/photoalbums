"""Read photos from a folder: size, capture time and GPS location."""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".tif", ".tiff"}
EXIF_IFD, GPS_IFD = 0x8769, 0x8825
DATETIME_ORIGINAL, DATETIME, ORIENTATION = 36867, 306, 274


@dataclass
class Photo:
    path: Path  # relative to the photos folder
    width: int  # after applying EXIF orientation
    height: int
    taken: datetime
    lat: float | None = None
    lon: float | None = None
    city: str | None = None

    @property
    def aspect(self) -> float:
        return self.width / self.height


def _dms(value) -> float:
    d, m, s = (float(v) for v in value)
    return d + m / 60 + s / 3600


def _exif(img: Image.Image) -> tuple[datetime | None, float | None, float | None]:
    exif = img.getexif()
    raw = exif.get_ifd(EXIF_IFD).get(DATETIME_ORIGINAL) or exif.get(DATETIME)
    taken = None
    if raw:
        try:
            taken = datetime.strptime(str(raw).strip("\x00"), "%Y:%m:%d %H:%M:%S")
        except ValueError:
            pass
    lat = lon = None
    gps = exif.get_ifd(GPS_IFD)
    try:
        if 2 in gps and 4 in gps:
            lat = _dms(gps[2]) * (-1 if gps.get(1) == "S" else 1)
            lon = _dms(gps[4]) * (-1 if gps.get(3) == "W" else 1)
    except (TypeError, ValueError, ZeroDivisionError):
        lat = lon = None
    return taken, lat, lon


def _takeout_sidecar(path: Path) -> dict | None:
    """Google Takeout writes metadata next to each photo, with names that vary
    (`x.jpg.json`, `x.jpg.supplemental-metadata.json`, truncated variants)."""
    for candidate in sorted(path.parent.glob(f"{path.name[:40]}*.json")):
        try:
            return json.loads(candidate.read_text())
        except (OSError, json.JSONDecodeError):
            continue
    return None


def scan(folder: Path) -> list[Photo]:
    photos = []
    for path in sorted(p for p in folder.rglob("*") if p.suffix.lower() in EXTENSIONS):
        with Image.open(path) as img:
            w, h = img.size
            if img.getexif().get(ORIENTATION) in (5, 6, 7, 8):
                w, h = h, w
            taken, lat, lon = _exif(img)

        if sidecar := _takeout_sidecar(path):
            if taken is None and (ts := sidecar.get("photoTakenTime", {}).get("timestamp")):
                taken = datetime.fromtimestamp(int(ts), timezone.utc).replace(tzinfo=None)
            geo = sidecar.get("geoDataExif") or sidecar.get("geoData") or {}
            if lat is None and geo.get("latitude") not in (None, 0.0):
                lat, lon = geo["latitude"], geo["longitude"]

        if taken is None:
            taken = datetime.fromtimestamp(path.stat().st_mtime)
        photos.append(Photo(path.relative_to(folder), w, h, taken, lat, lon))

    photos.sort(key=lambda p: p.taken)
    _add_cities(photos)
    return photos


def _add_cities(photos: list[Photo]) -> None:
    located = [p for p in photos if p.lat is not None]
    if not located:
        return
    import reverse_geocoder  # offline lookup; loads its city table on first use

    results = reverse_geocoder.search([(p.lat, p.lon) for p in located], mode=1, verbose=False)
    for photo, result in zip(located, results):
        photo.city = result["name"]
