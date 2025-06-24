from glorybot.helpers import *
from glorybot.v0.controller.main_c import *
from glorybot import global_states


@bot.command(name='delete')
async def delete(ctx, num_messages=999, clean_target: bool | None = None):
    try:
        DELETE_CHANNEL_IDS = [ANSWER_CHANNEL_ID, PING_CHANNEL_ID, GLORIA_PLAYER_ROLE_ID_1, GLORIA_PLAYER_ROLE_ID_2, GLORIA_PLAYER_ROLE_ID_3]
        if clean_target is True:
            DELETE_CHANNEL_IDS.append(CONTROLLER_CHANNEL_ID)
        num_messages_to_clear = int(num_messages) + 1
        tasks = []
        for channel_id_to_clear in DELETE_CHANNEL_IDS:
            channel_to_clear = bot.get_channel(channel_id_to_clear)
            if channel_to_clear:
                messages_to_clear = [mess async for mess in channel_to_clear.history(limit=num_messages_to_clear)] 
                tasks.append(channel_to_clear.delete_messages(messages_to_clear))
        await asyncio.gather(*tasks)
    except Exception:
        print(Exception)



@bot.command(name='rename')
async def rename(ctx, *new_names):
    if ADMIN_ROLE_ID in [role.id for role in ctx.author.roles]:
        try:
            if len(new_names) != len(GLORIA_PLAYER_CHANNEL_IDS):
                return
            
            tasks = []
            for channel_id, new_name in zip(GLORIA_PLAYER_CHANNEL_IDS, new_names):
                channel = bot.get_channel(channel_id)
                if channel:
                    tasks.append(channel.edit(name=new_name))
                else:
                    print(f"Kênh không tìm thấy.")

            # Rename channels simultaneously
            await asyncio.gather(*tasks)
        except IndexError: pass
    else: pass


@bot.event
async def on_message(message):
    global CURRENT_CONTEXT
    global last_processed_message

    if message.author == bot.user:
        return

    # Prevent processing the same message twice
    if hasattr(message, 'id') and getattr(last_processed_message, 'id', None) == message.id:
        return

    # Check if the message is from source channels
    if message.channel.id in GLORIA_PLAYER_CHANNEL_IDS:
        channel_id = message.channel.id
        
        # Update message tracking
        current_message = {
            'timestamp': message.created_at,
            'content': message.content,
            'channel_name': message.channel.name,
            'message_id': message.id
        }
        
        global_states.messages[channel_id] = current_message
        last_processed_message = message

    # Handle commands in target channel
    elif message.channel.id == CONTROLLER_CHANNEL_ID:
        if message.content.startswith("/start"):
            command = message.content.split()[1].lower()
            CURRENT_CONTEXT = command
        else:
            CURRENT_CONTEXT = None
        await bot.process_commands(message)


last_processed_message = None



@bot.event
async def on_interaction(interaction: Interaction):
    if interaction.user.id == bot.user.id:
        return



@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}')
    global_states.voice_client = await bot.get_channel(VOICE_STUDIO_CHANNEL_ID).connect()
    tasks = []
    
    for channel_id_to_clear in DELETE_CHANNEL_IDS:
        channel_to_clear = bot.get_channel(channel_id_to_clear)
        if channel_to_clear:
            messages_to_clear = [mess async for mess in channel_to_clear.history(limit=1000)]
            tasks.append(channel_to_clear.delete_messages(messages_to_clear))
    
    for channel_id, new_name in zip(GLORIA_PLAYER_CHANNEL_IDS, GLORIA_PLAYER_NAMES):
        channel = bot.get_channel(channel_id)
        if channel:
            tasks.append(channel.edit(name=new_name))
        
    # audio_embed = create_bot_embed_message(
    #     title="BẢNG ĐIỀU KHIỂN ÂM THANH",
    #     description="",
    #     color=discord.Color.gold()
    # )
    # tasks.append(bot.get_channel(TARGET_CHANNEL_ID).send(embed=audio_embed, view=AudioControllerView()))
    
    control_embed = create_bot_embed_message(
        title="BẢNG ĐIỀU KHIỂN CÁC VÒNG THI",
        description="Bấm vào vòng tương ứng để bắt đầu vòng thi",
        color=discord.Color.gold()
    )
    tasks.append(bot.get_channel(CONTROLLER_CHANNEL_ID).send(embed=control_embed, view=ControllerView()))
    await asyncio.gather(*tasks)


@bot.event
async def on_disconnect():
    tasks = []
    for channel_id_to_clear in DELETE_CHANNEL_IDS:
        channel_to_clear = bot.get_channel(channel_id_to_clear)
        if channel_to_clear:
            messages_to_clear = [mess async for mess in channel_to_clear.history(limit=1000)]
            tasks.append(channel_to_clear.delete_messages(messages_to_clear))
    await asyncio.gather(*tasks)
    logger.info("Bot has been shut down!")