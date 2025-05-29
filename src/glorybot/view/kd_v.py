from glorybot.helpers import *
from glorybot import global_states


class KhoiDongView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.ping_button = Button(label="BẤM CHUÔNG", style=ButtonStyle.gray, disabled=True, custom_id="KD_PING")
        self.reset_button = Button(label="Reset chuông", style=ButtonStyle.red, custom_id="KD_RESET")
        self.add_item(self.ping_button)
        self.add_item(self.reset_button)
        
        self.ping_button.disabled = True
        self.callback_executed = False

        self.ping_button.callback = self.ping_button_callback
        self.reset_button.callback = self.reset_button_callback

    async def ping_button_callback(self, interaction: Interaction):
        if self.callback_executed:
            return
        self.callback_executed = True
        global_states.reset_event.set()

        embed = create_user_embed_message(
            title="KHỞI ĐỘNG",
            description=f"{interaction.user.nick} đã giành được quyền trả lời!",
            color=discord.Color.yellow(),
            interaction=interaction
        )
        self.ping_button.style = ButtonStyle.green
        self.ping_button.disabled = True

        await interaction.response.edit_message(embed=embed, view=self)
        global_states.voice_client.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=PING_AUDIO_PATH))

    async def reset_button_callback(self, interaction: Interaction):
        global_states.reset_event.clear()
        # Check if the user has the required role
        role = discord.utils.get(interaction.user.roles, id=ADMIN_ROLE_ID)
        if role is None:
            await interaction.response.send_message("Bạn không thể thao tác trên nút này.", ephemeral=True)
            return
        
        self.callback_executed = False

        embed = create_bot_embed_message(
            title="KHỞI ĐỘNG",
            description="Nhấn vào nút BẤM CHUÔNG để giành quyền trả lời!",
            color=discord.Color.blue()
        )
        self.ping_button.style = ButtonStyle.blurple
        self.ping_button.disabled = False
        await interaction.response.edit_message(embed=embed, view=self)
        asyncio.create_task(start_reset_timer(self, interaction, title="KHỞI ĐỘNG"))