import discord
from discord.ext import commands
from config import token  # Import the bot's token from configuration file

intents = discord.Intents.default()
intents.members = True  # Allows the bot to detect member join/leave events
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Event: ketika bot siap digunakan
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Event: ketika ada anggota baru bergabung ke server
@bot.event
async def on_member_join(member):
    # Mengirim pesan ucapan selamat di setiap text channel di server
    for channel in member.guild.text_channels:
        try:
            await channel.send(f'Selamat datang, {member.mention}! 🎉')
            break  # kirim ke channel pertama yang bisa dikirim
        except discord.Forbidden:
            continue  # jika bot tidak punya izin di channel itu, lanjut ke berikutnya

# Command: perintah sederhana untuk menguji bot
@bot.command()
async def start(ctx):
    await ctx.send("Hi! I'm a chat manager bot!")

# Command: perintah untuk ban pengguna (hanya admin)
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("It is not possible to ban a user with equal or higher rank!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"User {member.name} was banned.")
    else:
        await ctx.send("This command should point to the user you want to ban. For example: `!ban @user`")

# Error handler untuk perintah ban
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have sufficient permissions to execute this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found.")

# Jalankan bot
bot.run(token)
