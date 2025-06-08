from glorybot.helpers import *
from glorybot import global_states


from discord.ui import View, Button
from discord import ButtonStyle, Interaction
import discord
import asyncio

# You must define FFMPEG_PATH, VCNV_AUDIO_PATH, global_states, create_user_embed_message, bot

class VuotChuongNgaiVatView(View):
    CNV_STRING = ''
    
    def __init__(self):
        super().__init__(timeout=None)
        
        self.CNV_INDEX = 0
        self.user_button_press_map = {}  # Maps user_id to a set of pressed button custom_ids
        self.button_press_count = {
            "VCNV_BLOCK_A_PING": 0,
            "VCNV_BLOCK_B_PING": 0,
            "VCNV_BLOCK_C_PING": 0,
            "VCNV_CNV_PING": 0
        }
        
        self.callback_executed = False

        # Define buttons
        self.block_a_ping_button = Button(label="TRẢ LỜI Ổ KHOÁ A", style=ButtonStyle.blurple, custom_id="VCNV_BLOCK_A_PING")
        self.block_b_ping_button = Button(label="TRẢ LỜI Ổ KHOÁ B", style=ButtonStyle.blurple, custom_id="VCNV_BLOCK_B_PING")
        self.block_c_ping_button = Button(label="TRẢ LỜI Ổ KHOÁ C", style=ButtonStyle.blurple, custom_id="VCNV_BLOCK_C_PING")
        self.vcnv_button = Button(label="TRẢ LỜI CHƯỚNG NGẠI VẬT", style=ButtonStyle.blurple, custom_id="VCNV_CNV_PING")
        self.block_button = Button(label="15s cuối cùng", style=ButtonStyle.red, custom_id="VCNV_BLOCK")

        # Add buttons to the view
        self.add_item(self.block_a_ping_button)
        self.add_item(self.block_b_ping_button)
        self.add_item(self.block_c_ping_button)
        self.add_item(self.vcnv_button)
        self.add_item(self.block_button)

        # Assign callbacks
        self.block_a_ping_button.callback = self.ping_button_callback
        self.block_b_ping_button.callback = self.ping_button_callback
        self.block_c_ping_button.callback = self.ping_button_callback
        self.vcnv_button.callback = self.ping_button_callback
        self.block_button.callback = self.block_button_callback

    async def ping_button_callback(self, interaction: Interaction):
        user_id = interaction.user.id
        custom_id = interaction.data["custom_id"]

        if user_id not in self.user_button_press_map:
            self.user_button_press_map[user_id] = set()

        if custom_id in self.user_button_press_map[user_id]:
            await interaction.response.send_message(
                "Bạn chỉ được phép trả lời mỗi Ổ Khoá và Chướng Ngại Vật duy nhất một lần!", ephemeral=True
            )
            return

        if self.callback_executed:
            return

        self.user_button_press_map[user_id].add(custom_id)
        self.callback_executed = True

        pressed_button = next(
            (btn for btn in [self.block_a_ping_button, self.block_b_ping_button, self.block_c_ping_button, self.vcnv_button] if btn.custom_id == custom_id),
            None
        )

        self.block_a_ping_button.disabled = True
        self.block_b_ping_button.disabled = True
        self.block_c_ping_button.disabled = True
        self.vcnv_button.disabled = True

        await interaction.response.edit_message(view=self)

        # Play sound and trigger event
        global_states.reset_event.set()
        global_states.voice_client.play(
            discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=VCNV_AUDIO_PATH)
        )

        # Update index and message
        self.button_press_count[custom_id] += 1
        self.CNV_INDEX += 1
        label = pressed_button.label if pressed_button else "Nút không xác định"
        user_display = interaction.user.nick or interaction.user.name

        self.CNV_STRING += f"\n{self.CNV_INDEX}. {user_display} đã giành được quyền **{label}**!"

        embed = create_user_embed_message(
            title="VƯỢT CHƯỚNG NGẠI VẬT",
            description=self.CNV_STRING,
            color=WHITE,
            interaction=interaction
        )

        await interaction.edit_original_response(embed=embed, view=self)
        await asyncio.sleep(5)

        self.block_a_ping_button.disabled = False
        self.block_b_ping_button.disabled = False
        self.block_c_ping_button.disabled = False
        self.vcnv_button.disabled = False
        self.callback_executed = False
        await interaction.edit_original_response(view=self)

    async def block_button_callback(self, interaction: Interaction):
        # Optional: add role check if needed
        self.block_button.disabled = True
        self.block_a_ping_button.disabled = True
        self.block_b_ping_button.disabled = True
        self.block_c_ping_button.disabled = True
        await interaction.edit_original_response(view=self)

        await asyncio.sleep(20)

        # Disable all ping buttons after 20s
        
        self.vcnv_button.disabled = True

        await interaction.edit_original_response(view=self)