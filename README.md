# Wordle Bot

基于 NoneBot2 编写的 Wordle 机器人

## Wordle 是什么
在 Wordle 中，玩家要在一天内用六次机会内猜中某个有五字英文字母的词汇。每次尝试后，玩家可能得到三种反馈：绿色表示字母位置正确；黄色表示答案包含该字母但位置错误；灰色表示答案没有该字母。

`Wordle Bot` 的 `wordle` 功能是原版的拓展，单词不再局限于只有五个字母

## 功能

### `wordle`
- 开始一局 Wordle 游戏

#### 使用方式
```
wordle -l <单词长度> -d <词典>
# 词典支持: CET4, CET6, GMAT, GRE, IELTS, SAT, TOEFL, 专八, 专四, 考研
```
#### 使用示例
```
wordle 
# 经典 Wordle, 猜五字单词，词典为CET4

wordle -l 6
# 猜六字单词，词典为CET4

wordle -d CET6
# 猜五字单词，词典为CET6

wordle -l 7 -d 考研
# 猜七字单词，词典为考研词典
```

## 部署
> 请确保您已经安装了 3.8 以上的 Python 并配置到环境变量

### 安装依赖
> 推荐在虚拟环境下进行

<details>
<summary>使用 PDM 安装</summary>
在本项目的根目录下打开命令行, 输入以下指令即可安装

    pdm install  
    
</details>

<details>
<summary>使用 pip 安装</summary>
在本项目的根目录下打开命令行, 输入以下指令即可安装

    pip install .  
    
</details>

### 配置
本项目依赖 nonebot-plugin-alconna 完成了多平台适配，默认对接到 QQ 频道，用户可依需求配置其他的适配器

#### 创建 QQ 机器人
注册 QQ开放平台 账号后，进入 https://q.qq.com/#/app/bot

点击 `应用管理` 中的 `创建机器人` 按钮，完成机器人配置。请在此步顺带完成沙箱频道配置

进入机器人界面，在 `开放` 的 `开发设置` 选项卡中获取 `AppID`, `Token` 和 `AppSecret`

#### 配置 NoneBot2
在本项目根目录创建 `.env` 文件，写入下列内容并修改
```
DRIVER=~httpx+~websockets

QQ_BOTS='
[
  {
    "id": "your_appid",
    "token": "your_token",
    "secret": "your_app_secret",
    "intent": {
      "guild_messages": true,
      "at_messages": false
    }
  }
]
'
```

依照需求，你可以根据 [NoneBot2 文档](https://nonebot.dev/docs/2.1.1/tutorial/application) 删减配置项

## 启动
<details>
<summary>PDM</summary>
PDM 会使用虚拟环境启动机器人，你不需要运行除此以外的指令

    pdm run bot.py  
    
</details>

<details>
<summary>Other</summary>
若配置了虚拟环境，请确保在虚拟环境下运行该指令

    python bot.py  
    
</details>

至此，Wordle Bot 已成功开始运行

你可以在刚才配置的沙箱频道中输入 `wordle` 来开始一局游戏

## 感谢

词库文件: [nonebot-plugin-wordle](https://github.com/noneplugin/nonebot-plugin-wordle)

> 没有任何词库以外的使用！