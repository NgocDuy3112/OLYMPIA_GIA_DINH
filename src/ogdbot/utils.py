from datetime import datetime
import logging
import discord

from configs import *

WHITE = 0xeeffee

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GLORIA LOGGING SYSTEM")

## For Windows
# FFMPEG_PATH = r"C:\FFmpeg\bin\ffmpeg.exe"
# if not discord.opus.is_loaded():
#     # Path to the opus library (if not automatically detected)
#     # discord.opus.load_opus('libopus-0.dll')  

## For macOS - You need to install ffmpeg and opus via Homebrew
# FFMPEG_PATH = "ffmpeg"
# if not discord.opus.is_loaded():
#     # Path to the opus library (if not automatically detected)
#     discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.5.2/lib/libopus.dylib')  

## For Linux (including Alpine) - Use this when you want to run with Docker
FFMPEG_PATH = "/usr/bin/ffmpeg"
if not discord.opus.is_loaded():
    # Path to the opus library (if not automatically detected)
    discord.opus.load_opus('libopus.so') 

# Check if OPUS was loaded successfully
if discord.opus.is_loaded():
    logger.info("✅ Opus is loaded and ready!")
else:
    logger.error("❌ Failed to load Opus!")
    logger.debug("Check the Opus!")