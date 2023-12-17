from enum import IntEnum
from typing import Dict, List, Literal, TypedDict


class LetterStatus(IntEnum):
    """Wordle 中的字母状态"""

    CORRECT = 1
    """字母及其位置都正确"""
    WRONG_POSITION = 2
    """字母正确，但位置错误"""
    WRONG_LETTER = 3
    """字母错误"""
    EMPTY = 4
    """空白"""


class Context(TypedDict):
    """Wordle 上下文"""

    word: str
    """单词"""
    meaning: Dict[Literal["中释", "英释"], str]
    """单词含义"""
    row: int
    """本次行数"""
    letters: List[List[str]]
    """字母列表"""
    statuses: List[List[LetterStatus]]
    """字母状态列表"""
