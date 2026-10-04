"""Generate placeholder photos with EXIF dates and GPS, for trying the tool
without real photos: `uv run scripts/make_sample_photos.py samples/`."""

import random
import sys
from datetime import datetime, timedelta
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TRIPS = [  # city, lat, lon, start, days
    ("Ghent", 51.054, 3.725, datetime(2025, 4, 19, 10), 2),
    ("Lisbon", 38.722, -9.139, datetime(2025, 7, 3, 9), 3),
    ("Porto", 41.150, -8.611, datetime(2025, 7, 6, 11), 2),
]


def dms(value: float):
    value = abs(value)
    d = int(value)
    m = int((value - d) * 60)
    s = round(((value - d) * 60 - m) * 60, 2)
    return (Fraction(d), Fraction(m), Fraction(s).limit_denominator(100))


def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(1)
    font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", 160)
    n = 0
    for city, lat, lon, start, days in TRIPS:
        for day in range(days):
            t = start + timedelta(days=day)
            for _ in range(rng.randint(7, 12)):
                t += timedelta(minutes=rng.randint(10, 70))
                size = (3000, 2000) if rng.random() < 0.65 else (2000, 3000)
                hue = rng.randint(0, 255)
                img = Image.new("HSV", size, (hue, 90, 200)).convert("RGB")
                draw = ImageDraw.Draw(img)
                for y in range(0, size[1], 8):  # vertical gradient
                    shade = int(60 * y / size[1])
                    draw.line([(0, y), (size[0], y)], fill=tuple(max(0, c - shade) for c in img.getpixel((0, y))), width=8)
                n += 1
                draw.text((120, 120), f"{city} #{n}", fill="white", font=font)
                draw.text((120, 320), t.strftime("%d %b %H:%M"), fill="white", font=font)

                exif = Image.Exif()
                exif[306] = t.strftime("%Y:%m:%d %H:%M:%S")
                gps = exif.get_ifd(0x8825)
                gps.update({1: "N" if lat >= 0 else "S", 2: dms(lat), 3: "E" if lon >= 0 else "W", 4: dms(lon)})
                img.save(out / f"IMG_{n:04d}.jpg", quality=88, exif=exif)
                if rng.random() < 0.1:  # a burst duplicate one second later
                    exif[306] = (t + timedelta(seconds=1)).strftime("%Y:%m:%d %H:%M:%S")
                    img.save(out / f"IMG_{n:04d}b.jpg", quality=88, exif=exif)
    print(f"{n} photos -> {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "samples"))
