"""Book formats: trim size, bleed and margins per print provider."""

from dataclasses import dataclass

MM = 72 / 25.4  # PDF points per millimetre


@dataclass(frozen=True)
class BookFormat:
    name: str
    description: str
    trim_w: float  # mm
    trim_h: float  # mm
    bleed: float  # mm, added on top, bottom and outer edge
    gutter_bleed: bool  # also add bleed on the binding edge
    margin: float = 12.0  # mm, white border inside the trim for framed layouts
    gap: float = 4.0  # mm between photos
    min_pages: int = 20
    max_pages: int = 440

    def page_size(self) -> tuple[float, float]:
        """PDF page size in mm, including bleed."""
        w = self.trim_w + self.bleed * (2 if self.gutter_bleed else 1)
        return w, self.trim_h + 2 * self.bleed

    def trim_origin(self, page_no: int) -> tuple[float, float]:
        """Lower-left corner of the trim box in mm. Page 1 is a right-hand page."""
        right_hand = page_no % 2 == 1
        x = self.bleed if (self.gutter_bleed or not right_hand) else 0.0
        return x, self.bleed


FORMATS = {
    f.name: f
    for f in [
        BookFormat(
            name="25x20",
            description="25 x 20 cm landscape, 3 mm bleed all round (common for EU labs)",
            trim_w=250,
            trim_h=200,
            bleed=3,
            gutter_bleed=True,
        ),
        BookFormat(
            name="blurb-standard-landscape",
            description="Blurb Standard Landscape ('10x8'; real trim 9.5x8 in, calculator 2026-10-04)",
            trim_w=241.3,
            trim_h=203.2,
            bleed=3.175,
            gutter_bleed=False,
            margin=16,  # Blurb's safe zone is 0.625 in at the binding edge
        ),
    ]
}
