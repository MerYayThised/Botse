import discord
from discord.ext import commands
import random
import os
import asyncio

bot_token = "MTEyMjk5MTg2MzUwNzQ2MDIzOQ.G5lLgB.nduNFGy8nEiHHYKjZByMwYFacXOeGYXF9hej7A"  # Botunuzun token'ını buraya girin
invite_channel_id = 1075788177626910912  # Davet loggerin çalıştığı kanalın ID'sini buraya girin
disney_file = "Disney.txt"  # Disney Plus hesaplarının bulunduğu dosya
netflix_folder = "Netflix"  # Netflix hesaplarının bulunduğu klasör
valorant_file = "Valorants.txt"
minecraft_file = "Minecraft.txt"
admin_role_id = 1234567890  # Admin rolünün ID'sini buraya girin

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')  # Varsayılan yardım komutunu kaldırıyoruz

@bot.event
async def on_ready():
    print('Bot başlatıldı.')
    await bot.change_presence(activity=discord.Game(name="!yardim yazarak yardım alabilirsiniz"))

@bot.command()
async def yardim(ctx):
    help_embed = discord.Embed(title="Komut Listesi", description="Botun mevcut komutları aşağıda listelenmiştir.", color=0x00ff00)
    help_embed.add_field(name="!netflix", value="Ücretsiz Netflix hesabı almak için kullanılır.", inline=False)
    help_embed.add_field(name="!disney", value="Ücretsiz Disney Plus hesabı almak için kullanılır.", inline=False)
    help_embed.add_field(name="!valorant", value="Ücretsiz Valorant Hesabı almak için kullanılır.", inline=False)
    help_embed.add_field(name="!minecraft", value="Ücretsiz Minecraft Hesabı almak için kullanılır.", inline=False)
    help_embed.add_field(name="!stock", value="Hesap stok durumunu kontrol etmek için kullanılır.", inline=False)
    help_embed.add_field(name="!kacinvite", value="Davet sayılarını kontrol etmek için kullanılır.", inline=False)
    help_embed.add_field(name="!kick", value="Kullanıcıyı sunucudan atmak için kullanılır.", inline=False)
    help_embed.add_field(name="!ban", value="Kullanıcıyı sunucudan yasaklamak için kullanılır.", inline=False)
    help_embed.add_field(name="!unban", value="Kullanıcının sunucudaki yasağını kaldırmak için kullanılır.", inline=False)
    help_embed.add_field(name="!clear", value="Belirli bir miktarda mesajı silmek için kullanılır.", inline=False)
    help_embed.add_field(name="!mute", value="Kullanıcıyı susturmak için kullanılır.", inline=False)
    help_embed.add_field(name="!unmute", value="Kullanıcının susturmasını kaldırmak için kullanılır.", inline=False)
    help_embed.add_field(name="!createchannel", value="Metin kanalı oluşturmak için kullanılır.", inline=False)
    help_embed.add_field(name="!deletechannel", value="Belirli bir metin kanalını silmek için kullanılır.", inline=False)
    help_embed.add_field(name="!createnickname", value="Kullanıcının takma adını değiştirmek için kullanılır.", inline=False)
    help_embed.add_field(name="!serverinfo", value="Sunucu hakkında bilgileri göstermek için kullanılır.", inline=False)
    # Ek komutları burada devam ettirebilirsiniz
    await ctx.send(embed=help_embed)

@bot.command()
async def netflix(ctx):
    account = get_account_from_folder(netflix_folder)
    if account:
        file = discord.File(account, filename="Netflix.txt")
        await ctx.author.send("İşte ücretsiz bir Netflix hesabı:", file=file)
        remove_account_from_folder(netflix_folder, account)  # Hesabı klasörden silme işlemi
        await ctx.send("Hesabınız DM'den gönderildi.")
    else:
        await ctx.send("Üzgünüm, Netflix hesapları tükenmiş.")

@bot.command()
async def disney(ctx):
    account = get_account_from_file(disney_file)
    if account:
        await ctx.author.send(f"İşte ücretsiz bir Disney Plus hesabı:\n{account}")
        remove_account_from_file(disney_file, account)  # Hesabı dosyadan silme işlemi
        await ctx.send("Hesabınız DM'den gönderildi.")
    else:
        await ctx.send("Üzgünüm, Disney Plus hesapları tükenmiş.")

@bot.command()
async def valorant(ctx):
    invite = get_invite_from_file(valorant_file)
    if invite:
        await ctx.author.send(f"İşte ücretsiz bir Valorant hesap:\n{invite}")
        remove_invite_from_file(valorant_file, invite)
        await ctx.send("Hesabınız DM'den gönderildi.")
    else:
        await ctx.send("Üzgünüm, Valorant hesapları tükenmiş.")

@bot.command()
async def minecraft(ctx):
    invite = get_invite_from_file(minecraft_file)
    if invite:
        await ctx.author.send(f"İşte ücretsiz bir Minecraft Hesabı :\n{invite}")
        remove_invite_from_file(minecraft_file, invite)
        await ctx.send("Hesabınız DM'den gönderildi.")
    else:
        await ctx.send("Üzgünüm, Minecraft Hesapları tükenmiş.")

@bot.command()
async def stock(ctx):
    stock_embed = discord.Embed(title="Hesap Stok Durumu", description="Mevcut hesap stok durumu aşağıda listelenmiştir.", color=0x00ff00)
    stock_embed.add_field(name="Netflix", value=f"Toplam {count_files_in_folder(netflix_folder)} adet hesap bulunuyor.")
    stock_embed.add_field(name="Disney Plus", value=f"Toplam {count_lines_in_file(disney_file)} adet hesap bulunuyor.")
    stock_embed.add_field(name="Valorant Hesaplar", value=f"Toplam {count_lines_in_file(valorant_file)} adet Hesap bulunuyor.")
    stock_embed.add_field(name="Minecraft Hesaplar", value=f"Toplam {count_lines_in_file(minecraft_file)} adet Hesap bulunuyor.")
    await ctx.send(embed=stock_embed)

@bot.command()
async def kacinvite(ctx):
    invite = awaitctx.guild.invites()
    for inv in invite:
        if inv.inviter == ctx.author:
            invite_count = inv.uses
            break
    else:
        invite_count = 0

    invite_embed = discord.Embed(title="Davet Sayısı", description=f"{ctx.author} kullanıcısının davet sayısı: {invite_count}", color=0x00ff00)
    await ctx.send(embed=invite_embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} sunucudan atıldı.")


@bot.command()
async def yazıyaz(ctx, channel: discord.TextChannel, *, message):
    await channel.send(message)
    await ctx.send(f"Mesajınız {channel.mention} kanalına gönderildi.")



announcements = []

@bot.command()
async def duyuruekle(ctx, *, message):
    announcements.append(message)
    await ctx.send("Duyuru başarıyla eklendi.")

@bot.command()
async def duyuru(ctx):
    if not announcements:
        await ctx.send("Henüz herhangi bir duyuru eklenmemiş.")
    else:
        announcement_embed = discord.Embed(title="Duyurular", description="Aşağıda mevcut duyurular listelenmektedir.", color=0x00ff00)
        for index, announcement in enumerate(announcements, start=1):
            announcement_embed.add_field(name=f"Duyuru {index}", value=announcement, inline=False)
        await ctx.send(embed=announcement_embed)

@bot.command()
async def duyurusil(ctx, *, duyuru):
    channel = ctx.channel
    async for message in channel.history(limit=None):
        if message.content == duyuru:
            await message.delete()
    await ctx.send("Duyuru silindi.")








@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} sunucudan yasaklandı.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member:
            await ctx.guild.unban(user)
            await ctx.send(f"{user} sunucudaki yasağı kaldırıldı.")
            return
    await ctx.send(f"{member} kullanıcısı sunucuda yasaklı değil.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"{amount} mesaj silindi.", delete_after=5)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: int, time_unit: str, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member} susturuldu.")
    duration_seconds = get_time_in_seconds(duration, time_unit)
    if duration_seconds > 0:
        await asyncio.sleep(duration_seconds)
        await member.remove_roles(muted_role)
        await ctx.send(f"{member} susturulması kaldırıldı.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"{member} susturulması kaldırıldı.")
    else:
        await ctx.send(f"{member} zaten susturulmamış.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def createchannel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        await guild.create_text_channel(channel_name)
        await ctx.send(f"{channel_name} adında bir metin kanalı oluşturuldu.")
    else:
        await ctx.send("Böyle bir kanal zaten mevcut.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def deletechannel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel:
        await existing_channel.delete()
        await ctx.send(f"{channel_name} adlı metin kanalı silindi.")
    else:
        await ctx.send("Böyle bir kanal bulunamadı.")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def createnickname(ctx, member: discord.Member, nickname):
    try:
        await member.edit(nick=nickname)
        await ctx.send(f"{member} kullanıcısının takma adı değiştirildi.")
    except discord.Forbidden:
        await ctx.send("Bu kullanıcının takma adını değiştiremiyorum.")

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    server_info_embed = discord.Embed(title="Sunucu Bilgileri", description=f"{guild.name} sunucusu hakkında bilgiler:", color=0x00ff00)
    server_info_embed.add_field(name="Sunucu Sahibi", value=guild.owner)
    server_info_embed.add_field(name="Oluşturulma Tarihi", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S"))
    server_info_embed.add_field(name="Üye Sayısı", value=guild.member_count)
    server_info_embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=server_info_embed)


def get_account_from_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    files = os.listdir(folder_path)
    if files:
        account_file = random.choice(files)
        account_path = os.path.join(folder_path, account_file)
        return account_path
    return None

def remove_account_from_folder(folder_name, account_path):
    os.remove(account_path)

def get_account_from_file(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        accounts = file.readlines()
        if accounts:
            account = random.choice(accounts)
            return account.strip()
    return None

def remove_account_from_file(file_name, account):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        accounts = file.readlines()
    with open(file_path, "w") as file:
        for acc in accounts:
            if acc.strip() != account:
                file.write(acc)

def get_invite_from_file(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        invites = file.readlines()
        if invites:
            invite = random.choice(invites)
            return invite.strip()
    return None

def remove_invite_from_file(file_name, invite):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        invites = file.readlines()
    with open(file_path, "w") as file:
        for inv in invites:
            if inv.strip() != invite:
                file.write(inv)

def count_files_in_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    files = os.listdir(folder_path)
    return len(files)

def count_lines_in_file(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        lines = file.readlines()
        return len(lines)


bot.run(bot_token)