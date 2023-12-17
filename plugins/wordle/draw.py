import io
from typing import List
from PIL import Image, ImageDraw, ImageFont

from .model import LetterStatus


font = ImageFont.truetype("data/consolab.ttf", size=32)


def i2b(img: Image.Image) -> bytes:
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format="PNG")
    return imgByteArr.getvalue()


def draw_background(status: LetterStatus) -> Image.Image:
    """绘制背景"""
    if status == LetterStatus.CORRECT:
        return Image.new("RGBA", (40, 40), (106, 172, 100))
    elif status == LetterStatus.WRONG_POSITION:
        return Image.new("RGBA", (40, 40), (202, 181, 87))
    elif status == LetterStatus.WRONG_LETTER or status == LetterStatus.EMPTY:
        return Image.new("RGBA", (40, 40), (121, 125, 127))


def draw_letter_block(letter: str, status: LetterStatus) -> Image.Image:
    """绘制字母块"""
    background = draw_background(status)
    draw = ImageDraw.Draw(background)
    letter_bbox = draw.textbbox((0, 0), letter.upper(), font=font)
    draw.text(
        (20 - letter_bbox[2] / 2, 20 - letter_bbox[3] / 2 - 2),
        letter.upper(),
        font=font,
        fill=(255, 255, 255),
    )
    return background


def draw_map(letters: List[List[str]], statuses: List[List[LetterStatus]]) -> bytes:
    """绘制 Wordle 图片, 未猜测字母传空字符串即可"""
    block_sep = 10
    block_size = 40
    width = len(letters[0]) * (block_size + block_sep) - block_sep
    height = len(letters) * (block_size + block_sep) - block_sep
    background = Image.new("RGBA", (width + block_sep * 2, height + block_sep * 2), (255, 255, 255))
    for i, row in enumerate(letters):
        for j, letter in enumerate(row):
            background.paste(
                draw_letter_block(letter, statuses[i][j]),
                (block_sep + j * (block_size + block_sep), block_sep + i * (block_size + block_sep)),
            )
    return i2b(background)
