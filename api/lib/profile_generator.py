from lib.GImage import GImage, Anchors, Algin, ImageAnchors
from PIL import Image, ImageFont, ImageDraw


def _get_rounded_rectangle(size: tuple[int, int], radius: float, color: tuple[int, int, int, int]):
    base = Image.new(mode="RGBA", size=size)
    box = ImageDraw.Draw(base)
    box.rounded_rectangle(
        xy=((0, 0), size),
        radius=radius,
        fill=color,
        outline=None,
        width=1
    )

    return base


class StatusTile:

    TILE_SIZE = (350, 120)
    TILE_COLOR = (0x00, 0x00, 0x00, 0x64)
    TILE_RADIUS = 15

    def __init__(self, icon_path: str, title: str):
        self.icon_path = icon_path
        self.title = title

    def get_status_tile(self, status: str):
        TILE_SIZE = StatusTile.TILE_SIZE
        X, Y = TILE_SIZE
        TILE_RADIUS = StatusTile.TILE_RADIUS
        TILE_COLOR = StatusTile.TILE_COLOR

        base = GImage(box_size=TILE_SIZE)
        base.paste(
            im=_get_rounded_rectangle(
                size=TILE_SIZE,
                radius=TILE_RADIUS,
                color=TILE_COLOR)
        )
        IMAGE_ANC = Y//2
        base.add_image(
            image_path=self.icon_path,
            box=(IMAGE_ANC, IMAGE_ANC),
            image_anchor=ImageAnchors.MIDDLE_MIDDLE
        )
        TEXT_X = X-Y
        test = GImage(box_size=(TEXT_X, Y))
        test.draw_text(
            text=self.title,
            position=(TEXT_X//2, 20),
            anchor=Anchors.MIDDLE_TOP
        )
        test.draw_text(
            text=status,
            position=(TEXT_X//2, Y-20),
            anchor=Anchors.MIDDLE_BASELINE
        )
        base.paste(im=test, box=(Y, 0))
        return base
