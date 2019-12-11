import discord
import random
import os
from math import sqrt, e, pi, sin, cos, tan, asin, acos, atan, factorial
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Lost Ark'))
    print('Бот готов к работе.')

@client.event
async def on_member_join(member):
    print(f'{member} появился на сервере!')
    await member.create_dm()
    await member.dm_channel.send(f'Вітаємо тебе на сервері, {member.name}!')

@client.event
async def on_member_remove(member):
    print(f'{member} выпал с сервера!')

# @commands.error
# async def command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send('ты че несешь??! я не знаю такой команды..')

# Пинг-понг и проверить задержку до сервера

@client.command()
async def ping(ctx):
    await ctx.send(f'Понг! {round(client.latency * 1000)} мс')

# Магический шар

@client.command(aliases=['8ball', 'qball', 'question', 'magicball', 'mb'])
async def _8ball(ctx, *, question):
    responses = [
        'Бесспорно',
        'Совершенно точно',
        'Никаких сомнений',
        'Определённо да',
        'Можешь быть уверен в этом',
        'Мне кажется, да',
        'Вероятнее всего',
        'Хорошие перспективы',
        'Знаки говорят — «да»',
        'Да',
        'Пока не ясно, попробуй снова',
        'Спроси позже',
        'Лучше не спрашивай',
        'Сейчас нельзя предсказать',
        'Сконцентрируйся и спроси опять',
        'Даже не думай',
        'Мой ответ — «нет»',
        'По моим данным — «нет»',
        'Перспективы не очень хорошие',
        'Весьма сомнительно'
    ]
    await ctx.send(f'Вопрос: {question}\nОтвет: {random.choice(responses)}')

# Проверка на отсутствие вопроса

@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Может вопрос-то введешь?!??!?!?!?')

# Проверка: является ли пользователь членом команды SunRise

@client.command()
@commands.has_any_role('Он тут по приколу', 'кубик', 'Кто этот дельфин', 'Лост-Аркер', 'Подключен к сети')
async def testMe(ctx):
    await ctx.send('Да, ты из SunRise!')

# Проверка на ошибку, если пользователь не состоит в SunRise

@testMe.error
async def testMe_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send('Ты не из SunRise!')

# Удаление сообщений в чате (только если владелец сервера)

@client.command()
@commands.is_owner()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Удалено {amount} сообщений.")

# Проверка на ошибку об отсутствии прав владельца

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send('Кажется, у тебя недостаточно прав!')

# Кик пользователя (только с ролью "кубик")

@client.command()
@commands.has_role('кубик')
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

# Проверка на ошибку об отсутствии роли "кубик" и вывод сообщения об ошибке

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Кажется, у тебя недостаточно прав!')

# Бан пользователя (только с ролью "кубик")

@client.command()
@commands.has_role('кубик')
async def ban(ctx, member : discord.Member, *, reason=None):
    await ctx.send(f'Пользователь {member.mention} забанен!')
    await member.ban(reason=reason)

# Проверка на ошибку об отсутствии роли "кубик" и вывод сообщения об ошибке

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Кажется, у тебя недостаточно прав...')

# Разбан пользователя по имени Discord, например, .unban Bamboni#1234

@client.command()
@commands.has_role('кубик')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Пользователь {user.mention} разбанен!")
            return

# Две ошибки при разбане пользователя

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('Введите имя пользователя полностью! Например, Bamboni#1234')
    if isinstance(error, commands.MissingRole):
        await ctx.send('Кажется, у тебя недостаточно прав...')

# Список пользователей сервера

@client.command()
async def members(ctx):
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} подключен к следующим серверам:\n'
        f'{guild.name} (id: {guild.id})\n')

    members = '\n - '.join([member.name for member in guild.members])
    await ctx.send(f'Работники компании Рассвет:\n - {members}') 

# Изменение статуса бота

@client.command()
@commands.has_any_role('Он тут по приколу', 'кубик', 'Кто этот дельфин', 'Лост-Аркер', 'Подключен к сети')
async def changeStatus(ctx, *, status):
    await client.change_presence(activity=discord.Game(status))

# Калькулятор

@client.command()
async def calc(ctx, *, message):
    await ctx.send(eval(message))

# Ошибка калькулятора (если неверно введен пример)

@calc.error
async def calc_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('кажись ты ввел пример неправильно..')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if 'youtube.com/watch?v' in message.content.lower():
#         await message.channel.send('о, видосик, надо глянуть')
#     if message.content.lower().startswith('.'):
#         pass

client.run(TOKEN)