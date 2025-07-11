import discord
from discord.ext import commands
import discord.opus
from discord import ButtonStyle, Embed, Interaction
from discord.ui import View, Button

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/src/configs/.env",verbose=True, override=True)
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
print(bot)


LOGIN = os.environ.get("LOGIN")
PASSWORD = os.environ.get("PASSWORD")
NGROK_ENDPOINT = os.environ.get("NGROK_ENDPOINT")
BOT_TOKEN = os.environ.get("BOT_TOKEN")


GLORIA_PLAYER_CHANNEL_ID_1 = int(os.environ.get("GLORIA_PLAYER_CHANNEL_ID_1"))
GLORIA_PLAYER_CHANNEL_ID_2 = int(os.environ.get("GLORIA_PLAYER_CHANNEL_ID_2"))
GLORIA_PLAYER_CHANNEL_ID_3 = int(os.environ.get("GLORIA_PLAYER_CHANNEL_ID_3"))
# GLORIA_PLAYER_CHANNEL_ID_4 = int(os.environ.get("GLORIA_PLAYER_CHANNEL_ID_4"))


CONTROLLER_CHANNEL_ID = int(os.environ.get("CONTROLLER_CHANNEL_ID"))
VOICE_STUDIO_CHANNEL_ID = int(os.environ.get("VOICE_STUDIO_CHANNEL_ID"))
PING_CHANNEL_ID = int(os.environ.get("PING_CHANNEL_ID"))
ANSWER_CHANNEL_ID = int(os.environ.get("ANSWER_CHANNEL_ID"))
# MUSIC_CHANNEL_ID = os.environ.get("MUSIC_CHANNEL_ID")


ADMIN_ROLE_ID = int(os.environ.get("ADMIN_ROLE_ID"))
GLORIA_PLAYER_ROLE_ID_1 = int(os.environ.get("GLORIA_PLAYER_ROLE_ID_1"))
GLORIA_PLAYER_ROLE_ID_2 = int(os.environ.get("GLORIA_PLAYER_ROLE_ID_2"))
GLORIA_PLAYER_ROLE_ID_3 = int(os.environ.get("GLORIA_PLAYER_ROLE_ID_3"))
# GLORIA_PLAYER_ROLE_ID_4 = int(os.environ.get("GLORIA_PLAYER_ROLE_ID_4"))


GLORIA_PLAYER_NAME_1 = os.environ.get("GLORIA_PLAYER_NAME_1")
GLORIA_PLAYER_NAME_2 = os.environ.get("GLORIA_PLAYER_NAME_2")
GLORIA_PLAYER_NAME_3 = os.environ.get("GLORIA_PLAYER_NAME_3")
# GLORIA_PLAYER_NAME_4 = os.environ.get("GLORIA_PLAYER_NAME_4")
GLORIA_PLAYER_NAMES = [GLORIA_PLAYER_NAME_1, GLORIA_PLAYER_NAME_2, GLORIA_PLAYER_NAME_3]


GLORIA_PLAYER_CHANNEL_IDS = [GLORIA_PLAYER_CHANNEL_ID_1, GLORIA_PLAYER_CHANNEL_ID_2, GLORIA_PLAYER_CHANNEL_ID_3]
DISPLAY_CHANNEL_IDS = GLORIA_PLAYER_CHANNEL_IDS.copy().append(ANSWER_CHANNEL_ID)
GLORIA_ROLE_IDS = [GLORIA_PLAYER_ROLE_ID_1, GLORIA_PLAYER_ROLE_ID_2, GLORIA_PLAYER_ROLE_ID_3]
GLORIA_PLAYER_NAMES = [GLORIA_PLAYER_NAME_1, GLORIA_PLAYER_NAME_2, GLORIA_PLAYER_NAME_3]
DELETE_CHANNEL_IDS = [ANSWER_CHANNEL_ID, PING_CHANNEL_ID, CONTROLLER_CHANNEL_ID, GLORIA_PLAYER_CHANNEL_ID_1, GLORIA_PLAYER_CHANNEL_ID_2, GLORIA_PLAYER_CHANNEL_ID_3]

ROUND_NAMES = ['XUẤT PHÁT', 'VƯỢT ĐÈO', 'THẦN TỐC', 'VỀ ĐÍCH', 'CÂU HỎI PHỤ']

PING_AUDIO_PATH = "/src/sounds/ping.mp3"
VCNV_AUDIO_PATH = "/src/sounds/vcnv.mp3"
PREPARE_TO_PING_AUDIO_PATH = "/src/sounds/prepare-to-ping.mp3"
CHANGE_ANSWER_AUDIO_PATH = "/src/sounds/change-answer.mp3"