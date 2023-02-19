import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime
import json
import os
import ctypes



redirect_dms_to_channel = 1050399620892721192
role_verified = 1048376186377609316
guild = 1048256699607298129
configfile = "config.json"

config = json.load(open(configfile))

token = config["token"]



class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        intents.members = True
        intents.bans = True
        super().__init__(command_prefix="$", intents=intents, help_command=None)

    async def setup_hook(self):
        # await self.tree.sync(guild=discord.Object(id=guild))
        await self.tree.sync()
        


client = Bot()





@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="🔹 /help | $help 🔹"), status=discord.Status.do_not_disturb)


@client.event
async def on_message(msg: discord.Message):
    if not msg.guild:
        if msg.author.id != client.user.id:

            try:
                """CREATE DM"""
                await msg.author.create_dm()
            except:
                """DM ALREADY CREATED"""
                pass

            ch = client.get_channel(redirect_dms_to_channel)

            if len(msg.attachments) < 1:
                embed=discord.Embed(title=f"{msg.author.id}", description=f"{msg.content}", color=0x0de7a6)
                embed.set_author(name=f"{msg.author.name}#{msg.author.discriminator}", icon_url=f"{msg.author.avatar.url}")
                (embed.set_thumbnail(url=f"{msg.author.banner.url}")) if msg.author.banner != None else None
                embed.set_footer(text=f"{client.user} | {datetime.now()}")
                await ch.send(embed=embed)
            else:
                embed=discord.Embed(title=f"{msg.author.id}", description=f"{msg.content}", color=0x0de7a6)
                embed.set_author(name=f"{msg.author.name}#{msg.author.discriminator}", icon_url=f"{msg.author.avatar.url}")
                (embed.set_thumbnail(url=f"{msg.author.banner.url}")) if msg.author.banner != None else None
                embed.set_footer(text=f"{client.user} | {datetime.now()}")
                await ch.send(embed=embed)
                for a in msg.attachments:
                    await ch.send(a.url)





@client.hybrid_command(name="load_dll", with_app_command=True, description="ANY | Execute Extension File [.DLL or .SO]")
async def load_dll(ctx: commands.Context, filename: str):

    MyDLL = ctypes.CDLL(f"./assets/lib/{filename}")
    # MyDLL.loader.restype = ctypes.c_char_p

    await ctx.send(f"Out: ```{MyDLL.main()}```")

    




@client.hybrid_command(name="libs", with_app_command=True, description="ANY | Get all extensions (DLL's)")
async def libs(ctx: commands.Context):
    await ctx.send(f'`{os.listdir(f"{os.getcwd()}/assets/lib/")}`', ephemeral=True)





@client.hybrid_command(name="dm", with_app_command=True, description="DEV | DM as bot")
async def dm(ctx: commands.Context, userid: str, message: str):

    usr = client.get_user(int(userid))

    embed=discord.Embed(
        title=f"**Message sent by {ctx.author.name}**", 
        description=f"{message}", color=0xe2e9e6
    )
    embed.set_author(
        name=f"{ctx.author.id}", 
        icon_url=f"{ctx.author.avatar.url}"
    )
    (embed.set_thumbnail(url=f"{ctx.author.banner.url}")) if ctx.author.banner != None else None
    embed.set_footer(text=f"{client.user} | {datetime.now()}", icon_url=f"{ctx.author.avatar.url}")
    await usr.send(embed=embed)

    await ctx.send("Message Sent!", ephemeral=True)






@client.hybrid_command(name="upload", with_app_command=True, description="DEV | Upload Object")
@app_commands.guilds(discord.Object(id=guild))
async def upload(ctx: commands.Context, file: discord.Attachment):

    await ctx.defer(ephemeral=True)

    attachment = file
    src = await attachment.read()
    with open(f"./assets/uploads/{attachment.filename}", mode="wb+") as fileuploadnet:
        fileuploadnet.write(src)
        fileuploadnet.close()
    embed=discord.Embed(title="💾 File Uploaded 💾", color=0x00ff40)
    embed.add_field(name="1️⃣ Filename", value=f"`{attachment.filename}`", inline=True)
    embed.add_field(name="2️⃣ Size", value=f"`{attachment.size}`", inline=True)
    embed.add_field(name="3️⃣ Attachment ID", value=f"`{attachment.id}`", inline=True)
    embed.add_field(name="4️⃣ Saved To", value=f"`./assets/uploads/{attachment.filename}`", inline=True)
    await ctx.author.send(embed=embed)

    await ctx.send(f"**Your file `{attachment.filename}` has been successfully uploaded.**", ephemeral=True)






@client.hybrid_command(name="remove_file", with_app_command=True, description="DEV | Remove Object")
@app_commands.guilds(discord.Object(id=guild))
async def remove_file(ctx: commands.Context, file: str):
    try:
        os.remove(f"./assets/uploads/{file}")
        await ctx.send(f"File {file} has been deleted.", ephemeral=True)
    except:
        await ctx.send(f"ERROR: {file} not exists.. [ FILES:  {os.listdir('./assets/uploads/')} ]", ephemeral=True)








    







@client.hybrid_command(name="purge", with_app_command=True, description="ADMIN | Purge Messages")
@app_commands.guilds(discord.Object(id=guild))
async def purge(ctx: commands.Context, messages: int = 10, oldest_first: bool = False):
    await ctx.channel.purge(limit=messages+1, oldest_first=oldest_first)
    selfmsg = await ctx.send(f"Deleted {messages} messages.")
    selfmsg.delete(2)




@client.hybrid_command(name="ping", with_app_command=True, description="ANY | Bot Latency")
@app_commands.guilds(discord.Object(id=guild))
async def ping(ctx: commands.Context):
    await ctx.defer(ephemeral=True)
    await ctx.send(f"Latency {client.latency}")







@client.hybrid_command(name="verify", with_app_command=True, description="ANY | Verify Yourself")
@app_commands.guilds(discord.Object(id=guild))
async def verify(ctx: commands.Context):

    button = Button(label="Verify", style=discord.ButtonStyle.green, emoji="✅")

    async def bcall(interaction: discord.Interaction):
        await interaction.response.edit_message(content="Already Verified", view=None, embed=None)
        v_getrole = discord.utils.get(ctx.author.guild.roles, id=role_verified)
        await ctx.author.add_roles(v_getrole, reason=f"HOST | Verified [ User: full={ctx.author.name}#{ctx.author.discriminator} | created_at={ctx.author.created_at} | is_active_on_mobile_now={ctx.author.is_on_mobile()} | status={ctx.author.desktop_status} ]")


    button.callback = bcall

    view = View()

    view.add_item(button)


    embed=discord.Embed(
        title=f"✅ Click button below to verify your account ✅", 
        description=f"Welcome to Lefeu's Discord server!\nClick button below to verify your account and receive member role.\nFor more info please visit http://lefeu.nvnet.pl", 
        color=0xffea00
    )
    embed.set_author(name=f"🖐 Welcome {ctx.author.name} 🖐")
    embed.set_footer(text=f"{client.user} | {datetime.now()}")

    await ctx.send(embed=embed, view=view, ephemeral=True)










client.run(token)