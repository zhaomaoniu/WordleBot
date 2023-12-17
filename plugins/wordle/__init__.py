import json
import random
from typing import Dict, List, Literal
from nonebot import get_driver, require

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import (
    on_alconna,
    Alconna,
    Option,
    Args,
    Arparma,
    AlconnaMatches,
    Target,
    Image,
    MessageTarget,
)

from .draw import draw_map
from .model import Context, LetterStatus


dic_list = ["CET4", "CET6", "GMAT", "GRE", "IELTS", "SAT", "TOEFL", "专八", "专四", "考研"]

words: Dict[
    Literal["CET4", "CET6", "GMAT", "GRE", "IELTS", "SAT", "TOEFL", "专八", "专四", "考研"],
    Dict[str, Dict[Literal["中释", "英释"], str]],
] = {}
words_all: List[str] = []
wordle_context: Dict[str, Context] = {}


@get_driver().on_startup
async def _():
    global words
    global words_all

    for i in dic_list:
        with open(f"data/{i}.json", "r", encoding="utf-8") as f:
            words[i] = json.load(f)
            words_all += list(words[i].keys())


wordle = on_alconna(
    Alconna(
        "wordle",
        Option(
            "--length", Args["length", int], alias=["-l"], help_text="单词长度", default=5
        ),
        Option("--dic", Args["dic", str], alias=["-d"], help_text="词库", default="CET4"),
    ),
    priority=10,
    block=True,
)
wordle_answer = on_alconna(Alconna("{word:str}"), priority=15)


@wordle.handle()
async def _(target: Target = MessageTarget(), result: Arparma = AlconnaMatches()):
    global wordle_context

    session_id = target.id

    if session_id in wordle_context:
        await wordle.finish("你已经在玩 Wordle 了哦")

    length: int = result.options["length"].value or result.other_args["length"]
    dic_name: str = result.options["dic"].value or result.other_args["dic"]

    if dic_name not in dic_list:
        await wordle.finish(f"词库 {dic_name} 不存在, 请从以下词库中选择: {', '.join(dic_list)}")

    dic = words[dic_name]

    word_length_dic: Dict[int, List[str]] = {}

    for i in dic.keys():
        if not i.isalpha():
            continue
        if len(i) not in word_length_dic:
            word_length_dic[len(i)] = []
        word_length_dic[len(i)].append(i)

    if length not in word_length_dic:
        await wordle.finish(f"词库中不存在长度为 {length} 的单词")

    word = random.choice(word_length_dic[length])

    wordle_context[session_id] = Context(
        word=word,
        meaning=dic[word],
        row=0,
        letters=[["" for _ in range(length)] for _ in range(length)],
        statuses=[[LetterStatus.EMPTY for _ in range(length)] for _ in range(length)],
    )

    await wordle.send(f"单词长度为 {length}，单词已选定，开始猜测")


@wordle_answer.handle()
async def _(target: Target = MessageTarget(), result: Arparma = AlconnaMatches()):
    global wordle_context
    global words_all

    word: str = result.header["word"]
    session_id = target.id

    if session_id not in wordle_context:
        return None

    if word == "bzd":
        await wordle.send(
            f"正确答案为: {wordle_context[session_id]['word']}\n{wordle_context[session_id]['meaning']['中释'].strip()}"
        )
        del wordle_context[session_id]
        return None

    context: Context = wordle_context[session_id]

    if len(word) != len(context["word"]):
        return None

    # 只能是26个字母
    if word.isalpha() == False:
        return None

    if word not in words_all:
        await wordle_answer.finish(f"你确定 {word} 是个合法的单词吗？")

    for i, letter in enumerate(word):
        context["letters"][context["row"]][i] = letter
        if letter == context["word"][i]:
            context["statuses"][context["row"]][i] = LetterStatus.CORRECT
        elif letter in context["word"]:
            context["statuses"][context["row"]][i] = LetterStatus.WRONG_POSITION
        else:
            context["statuses"][context["row"]][i] = LetterStatus.WRONG_LETTER

    context["row"] += 1

    wordle_img = draw_map(context["letters"], context["statuses"])

    if word == context["word"]:
        await wordle.send(
            f"答对啦！正确答案为: {word}\n{context['meaning']['中释'].strip()}"
            + Image(raw=wordle_img)
        )
        del wordle_context[session_id]
        return None
    elif context["row"] == len(context["letters"]):
        del wordle_context[session_id]
        await wordle.finish(
            f"次数用完啦！正确答案为: {context['word']}\n{context['meaning']['中释'].strip()}"
            + Image(raw=wordle_img)
        )
    else:
        wordle_context[session_id] = context
        await wordle.finish(Image(raw=wordle_img))
