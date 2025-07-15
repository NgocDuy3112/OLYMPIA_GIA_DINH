from src.ogdbot.v0.helpers import *
from src.ogdbot.v0 import global_states


class VeDichView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.ping_button = Button(label="BẤM CHUÔNG", style=ButtonStyle.gray, disabled=True, custom_id="VD_PING")
        self.reset_button = Button(label="Reset chuông", style=ButtonStyle.red, custom_id="VD_RESET")
        self.add_item(self.ping_button)
        self.add_item(self.reset_button)
        self.callback_executed = False

        self.ping_button.callback = self.ping_button_callback
        self.reset_button.callback = self.reset_button_callback

    async def ping_button_callback(self, interaction: Interaction):
        if self.callback_executed:
            return
        
        self.callback_executed = True
        global_states.reset_event.set()
        embed = create_user_embed_message(
            title="VỀ ĐÍCH",
            description=f"{interaction.user.nick or interaction.user.name} đã giành được quyền trả lời!",
            color=discord.Color.red(),
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

        # Defer the interaction response so we can update the message later
        await interaction.response.defer()

        # Play the reset sound
        if global_states.voice_client and global_states.voice_client.is_connected():
            global_states.voice_client.play(
                discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=PREPARE_TO_PING_AUDIO_PATH)
            )

        # Step 1: Show "Chú ý hiệu lệnh!" while sound plays
        attention_embed = create_bot_embed_message(
            title="VỀ ĐÍCH",
            description="Chú ý hiệu lệnh!",
            color=WHITE
        )
        self.ping_button.disabled = True
        await interaction.edit_original_response(embed=attention_embed, view=self)

        # Wait for the sound to play
        await asyncio.sleep(5)

        # Step 2: Enable the button and update the embed
        ready_embed = create_bot_embed_message(
            title="VỀ ĐÍCH",
            description="Nhấn vào nút BẤM CHUÔNG để giành quyền trả lời!",
            color=WHITE
        )
        self.ping_button.style = ButtonStyle.blurple
        self.ping_button.disabled = False
        await interaction.edit_original_response(embed=ready_embed, view=self)

        # Start the reset timer
        asyncio.create_task(start_reset_timer(self, interaction, title="VỀ ĐÍCH"))