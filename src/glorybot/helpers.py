from aiohttp import BasicAuth, ClientSession
import asyncio

from glorybot import global_states
from glorybot.utils import *
from app.schema.v0.answer import AnswerSchema


def create_bot_embed_message(title: str, description: str, color: discord.Color):
    embed = Embed(title=title, description=description, color=color)
    embed.set_author(name="GLORYTEAM", icon_url=bot.user.avatar.url)
    return embed


def create_user_embed_message(title: str, description: str, color: discord.Color, interaction: discord.Interaction):
    embed = Embed(title=title, description=description, color=color)
    embed.set_author(name=interaction.user.nick)
    return embed


async def send_answer(player_index, player_name, record_time, answer, url: str=f"https://helped-allowing-mudfish.ngrok-free.app/v0/answers/"):
    try:
        # Validate and structure data using the Pydantic model
        answer = AnswerSchema(
            index=player_index,
            name=player_name,
            answer=answer,
            time=record_time
        )

        headers = {'Content-Type': 'application/json; charset=utf-8'}

        async with ClientSession() as session:
            async with session.post(url, json=answer.model_dump(mode="json"), headers=headers) as response:
                if response.status == 200:
                    logger.info(f"✅ Đã cập nhật đáp án từ người chơi {player_name} thành công!")
                else:
                    logger.error(f"❌ Đáp án từ người chơi {player_name} không được cập nhật.")
                    logger.error(f"❌ {response.status} {response.text}")
    except Exception as e:
        logger.exception(f"❌ Lỗi khi gửi đáp án: {e}")


async def display_answers(messages, start_time, delay_seconds):
    display_string = ''
    
    for shape_index, source_channel_id in enumerate(GLORIA_PLAYER_CHANNEL_IDS, start=1):
        channel = bot.get_channel(source_channel_id)
        if not channel:
            continue  # skip if channel is not found

        channel_name = ' '.join(word.capitalize() for word in channel.name.split('-'))

        time_difference = 0
        if source_channel_id in messages:
            last_message = messages[source_channel_id]
            answer = last_message['content'].upper()
            timestamp = last_message['timestamp']
            time_difference = round((timestamp - start_time).total_seconds(), 3)
            if time_difference > delay_seconds or time_difference < 0:
                time_difference = delay_seconds
            await send_answer(shape_index, channel_name, time_difference, answer)
            display_string += f"\n({time_difference}) {channel_name}: {answer}"
        else:
            await send_answer(shape_index, channel_name, time_difference, "")
            display_string += f"\n(NA) {channel_name}: "

    embed = create_bot_embed_message(
        title="GLORYTEAM",
        description=display_string,
        color=discord.Color.gold()
    )
    await bot.get_channel(ANSWER_CHANNEL_ID).send(embed=embed)


async def start_reset_timer(view, interaction, title="GLORYTEAM", seconds=5.0):
    try:
        await asyncio.wait_for(global_states.reset_event.wait(), timeout=seconds)  # Wait for 
    except asyncio.TimeoutError:
        embed = create_bot_embed_message(
            title=title,
            description="Kết thúc việc bấm chuông!",
            color=discord.Color.red()
        )
        view.ping_button.style = ButtonStyle.blurple
        view.ping_button.disabled = True
        await interaction.message.edit(embed=embed, view=view)