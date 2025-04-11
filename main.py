import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

# 設定 Intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 已登入為 {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if before.content == after.content:
        return  # 如果內容沒變就不送

    embed = discord.Embed(
        title="✏️ 訊息被編輯",
        description=f"**作者：** {before.author.mention}\n**頻道：** {before.channel.mention}",
        color=discord.Color.greyple(),  # 灰色
    )
    embed.add_field(name="原始內容", value=before.content or "*無內容*", inline=False)
    embed.add_field(name="編輯後", value=after.content or "*無內容*", inline=False)
    embed.set_footer(text=f"訊息 ID: {before.id}")
    
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    embed = discord.Embed(
        title="🗑️ 訊息被刪除",
        description=f"**作者：** {message.author.mention}\n**頻道：** {message.channel.mention}",
        color=discord.Color.red(),  # 紅色
    )
    embed.add_field(name="刪除內容", value=message.content or "*無內容*", inline=False)
    embed.set_footer(text=f"訊息 ID: {message.id}")
    
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)

bot.run(TOKEN)
