from ocbot.helpers import *
from ocbot import global_states


class VeDichControllerView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.start_button_1 = Button(label="10s", style=ButtonStyle.blurple, custom_id="VD_START_1", row=0)
        self.start_button_2 = Button(label="15s", style=ButtonStyle.blurple, custom_id="VD_START_2", row=0)
        self.start_button_3 = Button(label="20s", style=ButtonStyle.blurple, custom_id="VD_START_3", row=0)
        self.start_button_4 = Button(label="25s", style=ButtonStyle.blurple, custom_id="VD_START_4", row=0)
        self.change_button = Button(label="5s thay đổi đáp án", style=ButtonStyle.blurple, custom_id="VD_CHANGE", row=0)
        self.reset_button = Button(label="Reset đồng hồ", style=ButtonStyle.red, custom_id="VD_RESET", row=1)

        self.add_item(self.start_button_1)
        self.add_item(self.start_button_2)
        self.add_item(self.start_button_3)
        self.add_item(self.start_button_4)
        self.add_item(self.reset_button)
        self.add_item(self.change_button)

        self.start_button_1.callback = self.generate_vd_callback(10)
        self.start_button_2.callback = self.generate_vd_callback(15)
        self.start_button_3.callback = self.generate_vd_callback(20)
        self.start_button_4.callback = self.generate_vd_callback(25)
        self.reset_button.callback = self.reset_button_callback
        self.change_button.callback = self.change_button_callback

    def generate_vd_callback(self, delay_seconds):
        async def callback(interaction):
            await self.start_vd_button_callback(delay_seconds, interaction)
        return callback

    async def start_vd_button_callback(self, delay_seconds: int, interaction: Interaction):
        self.start_button_1.disabled = True
        self.start_button_2.disabled = True
        self.start_button_3.disabled = True
        self.start_button_4.disabled = True
        await interaction.response.edit_message(view=self)
        start_time = datetime.now().astimezone()
        try:
            global_states.messages.clear()
            # Extract the delay value from the message content
            tasks = []
            temp_messages = []
            for source_channel_id in GLORIA_PLAYER_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                embed = create_bot_embed_message(
                    title="VỀ ĐÍCH",
                    description=f"Thời gian trả lời câu hỏi bắt đầu!\nNhập câu trả lời cho câu hỏi ở kênh chat tương ứng với tên của bạn và nhấn Enter trong {delay_seconds} giây để hệ thống ghi nhận câu trả lời.",
                    color=discord.Color.blue()
                )
                if channel:
                    message = channel.send(embed=embed)
                    temp_messages.append(message)
                    tasks.append(message)
            await asyncio.gather(*tasks)
            await asyncio.sleep(delay_seconds)

            tasks = []
            for source_channel_id in GLORIA_PLAYER_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                embed = create_bot_embed_message(
                    title="VỀ ĐÍCH",
                    description="Thời gian trả lời câu hỏi kết thúc!",
                    color=discord.Color.red()
                )
                if channel:
                    tasks.append(channel.send(embed=embed))
            await asyncio.gather(*tasks)
            await display_answers(global_states.messages, start_time, delay_seconds)   

        except (IndexError, ValueError):
            pass  # Ignore if there's no delay specified or an invalid delay value

    async def reset_button_callback(self, interaction: Interaction):
        self.start_button_1.disabled = False
        self.start_button_2.disabled = False
        self.start_button_3.disabled = False
        self.start_button_4.disabled = False
        await interaction.response.edit_message(view=self)

    async def change_button_callback(self, interaction: Interaction):
        if global_states.voice_client and global_states.voice_client.is_connected():
            global_states.voice_client.play(
                discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=CHANGE_ANSWER_AUDIO_PATH)
            )