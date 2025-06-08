from glorybot.helpers import *
from glorybot import global_states


class VuotChuongNgaiVatControllerView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.start_button = Button(label="15s", style=ButtonStyle.blurple, custom_id="VCNV_START")
        self.reset_button = Button(label="Reset đồng hồ", style=ButtonStyle.red, custom_id="VCNV_RESET")

        self.add_item(self.start_button)
        self.add_item(self.reset_button)

        self.start_button.callback = self.generate_vcnv_callback(15)
        self.reset_button.callback = self.reset_button_callback
    
    def generate_vcnv_callback(self, delay_seconds):
        async def callback(interaction):
            await self.start_vcnv_button_callback(delay_seconds, interaction)
        return callback

    async def start_vcnv_button_callback(self, delay_seconds: int, interaction: Interaction):
        self.start_button.disabled = True
        self.reset_button.disabled = True
        await interaction.response.edit_message(view=self)
        start_time = datetime.now().astimezone()
        try:
            global_states.messages.clear()
            # Extract the delay value from the message content
            tasks = []
            for source_channel_id in GLORIA_PLAYER_CHANNEL_IDS:
                channel = bot.get_channel(source_channel_id)
                embed = create_bot_embed_message(
                    title="VƯỢT CHƯỚNG NGẠI VẬT",
                    description=f"Thời gian trả lời câu hỏi bắt đầu!\nNhập câu trả lời cho câu hỏi ở kênh chat tương ứng với tên của bạn và nhấn Enter trong {delay_seconds} giây để hệ thống ghi nhận câu trả lời.\nĐể trả lời Chướng ngại vật hoặc Ổ khoá, vào kênh <#{PING_CHANNEL_ID}> và nhấn vào nút BẤM CHUÔNG và chọn vào nút bạn muốn trả lời. Lưu ý: Bạn chỉ được phép nhấn chuông trả lời mỗi Ổ Khoá và Chướng Ngại Vật DUY NHẤT MỘT LẦN!",
                    color=discord.Color.blue()
                )
                if channel:
                    tasks.append(channel.send(embed=embed))
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
        self.start_button.disabled = False
        self.reset_button.disabled = False
        await interaction.response.edit_message(view=self)