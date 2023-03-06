from fastapi.responses import Response
from fastapi import FastAPI
from model.image import get_image, Colors, Fonts

from collections import OrderedDict
from hashlib import md5


CACHE_MAX_SIZE = 500
CACHE_IMAGES = OrderedDict()

NAME_DICT = {
    "bankan": 30,  # ばんかんちゃん
    # "gomi": 31,  # ごみにぃとちゃん
}

CHAR_NAMES = [k for k in NAME_DICT.keys()]


def get_hash_int(texts: list[str]) -> int:
    result = int(md5("".join(texts).encode()).hexdigest(), 16)
    return result


app = FastAPI()


# jsonを出力するとこ
@app.get("/color.json")
async def get_color_json():
    """利用可能な色を取得します。

    Returns:
        Response: json
    """
    return Colors.get_color_options()


@app.get("/font.json")
async def get_font_json():
    """利用可能なフォント一覧を取得します。

    Returns:
        Response: json
    """
    return Fonts.get_font_options()


@app.get("/character.json")
async def get_character_json():
    """キャラクター名一覧を取得します。

    Returns:
        Response: json
    """
    return CHAR_NAMES


@app.get("/{char_name:str}.png")
async def get_char_image(char_name: str,  message: str = "なんかよう？"):
    """キャラクター名を指定してその画像をベースにメッセージを喋らせます

    Args:
        char_name (str): キャラクター名(指定キャラクター名)
        message (str, optional): _description_. Defaults to "なんかよう？".

    Raises:
        ValueError: キャラクター名が存在しない場合にエラーを返す

    Returns:
        Response: image/png
    """
    key = get_hash_int([char_name, message])

    if key in CACHE_IMAGES:
        byte_data = CACHE_IMAGES[key]
    else:
        if char_name in NAME_DICT:
            data = await get_image(image_id=NAME_DICT[char_name], message=message)
        else:
            raise ValueError("is not a valid")

        byte_data = await data.get_bytes()
        CACHE_IMAGES[key] = byte_data

        if len(CACHE_IMAGES) > CACHE_MAX_SIZE:
            CACHE_IMAGES.popitem(False)

    return Response(content=byte_data, media_type="image/png")
