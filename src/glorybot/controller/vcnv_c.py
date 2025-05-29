from glorybot.helpers import *
from glorybot import global_states


class VuotChuongNgaiVatControllerView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.start_button_1 = Button(label="10s", style=ButtonStyle.blurple, custom_id="VCNV_START_1")
        self.start_button_2 = Button(label="15s", style=ButtonStyle.blurple, custom_id="VCNV_START_2")
        self.reset_button = Button(label="Reset đồng hồ", style=ButtonStyle.red, custom_id="VCNV_RESET")

        self.add_item(self.start_button_1)
        self.add_item(self.start_button_2)
        self.add_item(self.reset_button)

        self.start_button_1.callback = self.generate_vcnv_callback(10)
        self.start_button_2.callback = self.generate_vcnv_callback(15)
        self.reset_button.callback = self.reset_button_callback
    
    def generate_vcnv_callback(self, delay_seconds):
        async def callback(interaction):
            await self.start_vcnv_button_callback(delay_seconds, interaction)
        return callback

    async def start_vcnv_button_callback(self, delay_seconds: int, interaction: Interaction):
        self.start_button_1.disabled = True
        self.start_button_2.disabled = True
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
                    title="VƯỢT CHƯỚNG NGẠI VẬT",
                    description=f"Thời gian trả lời câu hỏi bắt đầu!\nNhập câu trả lời cho câu hỏi ở kênh chat tương ứng với tên của bạn và nhấn Enter trong {delay_seconds} giây để hệ thống ghi nhận câu trả lời.\nĐể trả lời Chướng ngại vật, vào kênh <#{PING_CHANNEL_ID}> và nhấn vào nút BẤM CHUÔNG. Lưu ý: Bạn chỉ được phép nhấn chuông trả lời chướng ngại vật DUY NHẤT MỘT LẦN!",
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
                    title="VƯỢT CHƯỚNG NGẠI VẬT",
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
        await interaction.response.edit_message(view=self)