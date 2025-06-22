from glorybot.helpers import *

from glorybot.controller.kd_c import KhoiDongControllerView
from glorybot.controller.vcnv_c import VuotChuongNgaiVatControllerView
from glorybot.controller.tt_c import TangTocControllerView
from glorybot.controller.vd_c import VeDichControllerView

from glorybot.view.kd_v import KhoiDongView
from glorybot.view.vcnv_v import VuotChuongNgaiVatView
from glorybot.view.vd_v import VeDichView

from glorybot import global_states


class ControllerView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.kd_button = Button(label="XUẤT PHÁT", style=ButtonStyle.blurple, custom_id="C_KD", row=0)
        self.vcnv_button = Button(label="VƯỢT ĐÈO", style=ButtonStyle.blurple, custom_id="C_VCNV", row=0)
        self.tt_button = Button(label="THẦN TỐC", style=ButtonStyle.blurple, custom_id="C_TT", row=0)
        self.vd_button = Button(label="VỀ ĐÍCH", style=ButtonStyle.blurple, custom_id="C_VD", row=0)
        # self.chp_button = Button(label="CÂU HỎI PHỤ", style=ButtonStyle.blurple, custom_id="C_CHP", row=0)
        self.turn_off_button = Button(label="TẮT BOT", style=ButtonStyle.red, custom_id="C_TURN_OFF", row=1)

        self.add_item(self.kd_button)
        self.add_item(self.vcnv_button)
        self.add_item(self.tt_button)
        # self.add_item(self.hs_button)
        self.add_item(self.vd_button)
        # self.add_item(self.chp_button)
        self.add_item(self.turn_off_button)

        self.kd_button.callback = self.kd_button_callback
        self.vcnv_button.callback = self.vcnv_button_callback
        self.tt_button.callback = self.tt_button_callback
        self.vd_button.callback = self.vd_button_callback
        # self.chp_button.callback = self.chp_button_callback
        self.turn_off_button.callback = self.turn_off_button_callback

    async def kd_button_callback(self, interaction: Interaction):
        await interaction.response.edit_message(view=self)
        target_embed = create_bot_embed_message(
            title="KHỞI ĐỘNG",
            description="Bộ đếm giờ",
            color=discord.Color.gold()
        )
        await bot.get_channel(CONTROLLER_CHANNEL_ID).send(embed=target_embed, view=KhoiDongControllerView())
        ping_embed = create_bot_embed_message(
            title="KHỞI ĐỘNG",
            description="Nhấn vào nút BẤM CHUÔNG để giành quyền trả lời!",
            color=WHITE
        )
        await bot.get_channel(PING_CHANNEL_ID).send(embed=ping_embed, view=KhoiDongView())

    async def vcnv_button_callback(self, interaction: Interaction):
        await interaction.response.edit_message(view=self)
        embed = create_bot_embed_message(
            title="VƯỢT CHƯỚNG NGẠI VẬT",
            description="Bộ đếm giờ",
            color=discord.Color.gold()
        )
        await bot.get_channel(CONTROLLER_CHANNEL_ID).send(embed=embed, view=VuotChuongNgaiVatControllerView())
        ping_embed = create_bot_embed_message(
            title="VƯỢT CHƯỚNG NGẠI VẬT",
            description="Nhấn vào nút BẤM CHUÔNG để giành quyền trả lời Ổ Khoá và Chướng Ngại Vật!",
            color=WHITE
        )
        await bot.get_channel(PING_CHANNEL_ID).send(embed=ping_embed, view=VuotChuongNgaiVatView())

    async def tt_button_callback(self, interaction: Interaction):
        await interaction.response.edit_message(view=self)
        embed = create_bot_embed_message(
            title="TĂNG TỐC",
            description="Bộ đếm giờ",
            color=discord.Color.gold()
        )
        await bot.get_channel(CONTROLLER_CHANNEL_ID).send(embed=embed, view=TangTocControllerView())

    async def vd_button_callback(self, interaction: Interaction):
        await interaction.response.edit_message(view=self)
        embed = create_bot_embed_message(
            title="VỀ ĐÍCH",
            description="Bộ đếm giờ",
            color=discord.Color.gold()
        )
        await bot.get_channel(CONTROLLER_CHANNEL_ID).send(embed=embed, view=VeDichControllerView())
        ping_embed = create_bot_embed_message(
            title="VỀ ĐÍCH",
            description="Nhấn vào nút BẤM CHUÔNG để giành quyền trả lời!",
            color=WHITE
        )
        await bot.get_channel(PING_CHANNEL_ID).send(embed=ping_embed, view=VeDichView())

    # async def chp_button_callback(self, interaction: Interaction):
    #     await interaction.response.edit_message(view=self)
    #     target_embed = create_bot_embed_message(
    #         title="CÂU HỎI PHỤ",
    #         description="Phần thi Câu hỏi phụ bắt đầu!",
    #         color=discord.Color.gold()
    #     )
    #     await bot.get_channel(TARGET_CHANNEL_ID).send(embed=target_embed)
    #     ping_embed = create_bot_embed_message(
    #         title="CÂU HỎI PHỤ",
    #         description="Nhấn vào nút BẤM CHUÔNG để giành quyền trả lời!",
    #         color=discord.Color.blue()
    #     )
    #     await bot.get_channel(PING_CHANNEL_ID).send(embed=ping_embed, view=CauHoiPhuView())
        
    async def turn_off_button_callback(self, interaction: Interaction):
        tasks = []
        for channel_id_to_clear in DELETE_CHANNEL_IDS:
            channel_to_clear = bot.get_channel(channel_id_to_clear)
            if channel_to_clear:
                messages_to_clear = [mess async for mess in channel_to_clear.history(limit=1000)]
                tasks.append(channel_to_clear.delete_messages(messages_to_clear))
        await asyncio.gather(*tasks)

        if global_states.voice_client.is_connected():
            await global_states.voice_client.disconnect()

        await bot.close()