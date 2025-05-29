from glorybot.helpers import *
from glorybot import global_states


class VuotChuongNgaiVatView(View):
    CNV_STRING = ''
    CNV_INDEX = 0
    user_who_pressed = set()

    def __init__(self):
        super().__init__(timeout=None)
        self.block_a_ping_button = Button(label="TRẢ LỜI Ổ KHOÁ A", style=ButtonStyle.blurple, custom_id="VCNV_BLOCK_A_PING")
        self.block_b_ping_button = Button(label="TRẢ LỜI Ổ KHOÁ B", style=ButtonStyle.blurple, custom_id="VCNV_BLOCK_B_PING")
        self.block_c_ping_button = Button(label="TRẢ LỜI Ổ KHOÁ C", style=ButtonStyle.blurple, custom_id="VCNV_BLOCK_C_PING")
        self.vcnv_button = Button(label="TRẢ LỜI CHƯỚNG NGẠI VẬT", style=ButtonStyle.blurple, custom_id="VCNV_CNV_PING")
        self.block_button = Button(label="15s cuối cùng", style=ButtonStyle.red, custom_id="VCNV_BLOCK")
        
        self.add_item(self.block_a_ping_button)
        self.add_item(self.block_b_ping_button)
        self.add_item(self.block_c_ping_button)
        self.add_item(self.vcnv_button)
        self.add_item(self.block_button)
    
        self.callback_executed = False

        self.block_a_ping_button.callback = self.ping_button_callback
        self.block_b_ping_button.callback = self.ping_button_callback
        self.block_c_ping_button.callback = self.ping_button_callback
        self.vcnv_button.callback = self.ping_button_callback
        self.block_button.callback = self.block_button_callback

    async def ping_button_callback(self, interaction: Interaction):
        if interaction.user.id in self.user_who_pressed:
            await interaction.response.send_message("Bạn chỉ được phép nhấn chuông trả lời ổ khoá hoặc chướng ngại vật một lần!", ephemeral=True)
            return
        
        # Disable the button and set the callback_executed to prevent re-triggering
        if self.callback_executed:
            return
        
        self.user_who_pressed.add(interaction.user.id)
        self.callback_executed = True
        self.ping_button.disabled = True
        await interaction.response.edit_message(view=self)  # Disable the button immediately

        # Play the sound and set the event
        global_states.reset_event.set()
        global_states.voice_client.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=VCNV_AUDIO_PATH))
        
        # Update the message with the user who pressed the button
        self.CNV_INDEX += 1
        self.CNV_STRING += f"\n{self.CNV_INDEX}. {interaction.user.nick} đã giành được quyền trả lời chướng ngại vật!"
        
        embed = create_user_embed_message(
            title="VƯỢT CHƯỚNG NGẠI VẬT",
            description=self.CNV_STRING,
            color=discord.Color.yellow(),
            interaction=interaction
        )
        await interaction.edit_original_response(embed=embed, view=self)
        
        # Wait for 5 seconds
        await asyncio.sleep(5)
        
        # Enable the button again
        self.ping_button.disabled = False
        self.callback_executed = False  # Allow other users to press the button
        await interaction.edit_original_response(view=self)
        
        
    async def block_button_callback(self, interaction: Interaction):
        restricted_role = bot.utils.get(interaction.user.roles, id=self.restrcited_role_id)
        if restricted_role:
            return
        self.block_button.disabled = True
        interaction.edit_original_response(view=self)
        await asyncio.sleep(15)
        self.ping_button.disabled = True
        await interaction.edit_original_response(view=self)