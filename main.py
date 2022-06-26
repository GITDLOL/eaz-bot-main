#Imports
import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive
import random
import json
from random import randint
from discord.ext.commands import Bot, has_permissions, CheckFailure
import asyncio
from discord.utils import get
from discord.ext import tasks
import youtube_dl
import randfacts
import names

#Secrets
load_dotenv()
TOKEN = os.getenv('TOKEN')
my_secret = os.environ['abcdefg']
#password = os.environ['password']



#Settings
bot = commands.Bot(command_prefix='z-', help_command=None)
#bot.load_extension("helpcommand")
#plsdo in test rpl

@bot.event
async def on_ready():
    print(f'{bot.user.name} IS UP')

    await bot.change_presence(activity=discord.Game(
            name=
            f"z-help, Made by mrtbts and zryabguy | {len(bot.guilds)} servers"), status=discord.Status.do_not_disturb)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '**Cooling Down**, the bot is overheating, try again in {:.2f}s'.format(
            error.retry_after)
        await ctx.send(msg)


@bot.event
async def on_dbl_vote(data):
    print(data)


#Commands
@bot.command(name='help')
async def helpmenu(message):
    #if command :
      #await message.send("Check back later for specific command help, meanwhile here's the normal help message")
    #else:
    await message.send("Check your DMs ✅")
    Help = discord.Embed(
        title='EaZ The Bot\'s Help Menu\n',
        description=
        'The Prefix is: **z-** and if you want more info about the bot, do z-info'
    )
    Help.add_field(
        name='Random Commands',
        value='z-randomname\nz-randomwebsite\nz-facts')
    Help.add_field(
        name='Administrator Commands',
        value=
        'z-ban `user` `reason`\nz-kick `user`\nz-slowmode `amount`\nz-lockchannel\nz-unlockchannel\nz-delete `msgamount`\nz-mute `user` `reason`\nz-unmute `user`\nz-whois `user`'
    )
    Help.add_field(
        name='Economy Commands',
        value=
        'z-balance\nz-beg\nz-deposit `amount`\nz-withdraw `amount`\nz-bet `amount`\nz-give `member` `amount`'
    )
    Help.add_field(
        name='Misc Commands',
        value=
        'z-embedsay `MESSAGE`\nz-mybotperms\nz-calculator `mathquestion`\nz-hack `user`\nz-ping'
    )

    await message.author.send(embed=Help)

@bot.command(name='facts')
async def wordmix(message):
    await message.send(randfacts.get_fact(filter_enabled=True))


@bot.command(name='randomname')
async def randomname(message):
  await message.send(names.get_full_name())


@bot.command(name='embedsay')
async def embedsay(message, *, args):
    embedSay = discord.Embed(title="You said: ",
                             description=args,
                             color=0x00ff00)
    await message.send(embed=embedSay)


@bot.command(name='randomwebsite')
async def randweb(message):
    RandomWebsites = [
        "https://www.agegeek.com/", "https://www.worldsdumbestgame.com/",
        "https://www.crazycardtrick.com/", "https://www.inherentlyfunny.com/",
        "https://hczhcz.github.io/Flappy-2048/"
    ]
    RandWebRandomizer = random.choice(RandomWebsites)
    RandWeb = discord.Embed(title="Here is your random website (Not NSFW): ",
                            description=RandWebRandomizer)
    await message.send(embed=RandWeb)


@bot.command(name='info')
async def botinfoget(message):
    BotVer = "0.3"

    em = discord.Embed(title="Info About EaZ: ")
    em.add_field(
        name="Discord Server: ",
        value=
        "The Official Invite to the EaZ Hub Discord Server: https://discord.gg/SERsBybPwt",
        inline=False)
    em.add_field(name="Bot Version: ", value=BotVer)
    em.add_field(
        name="Credits",
        value=
        "**Programmers/Developers: \n** *mynameiszryab* \n YT Channel: [`zryab`](https://www.youtube.com/channel/UCEH-nZRHMYo1flXOcVPqkiw) \n *mrtbts* \n Twitch: [`mrtbtswastaken`](https://twitch.tv/mrtbtswastaken)"
    )
    em.add_field(name="Invite: ", value="<https://bit.ly/3pFzDBi>")

    await message.send(embed=em)

@bot.command(name='vote')
async def vote(message):
  voteEm = discord.Embed(title="Vote for EaZ on: ", description="[`Top.gg`](https://top.gg/bot/918510933549121536)\n[`discordbotlist.com`](https://discordbotlist.com/bots/eaz)")

  await message.send(embed=voteEm)

@bot.command(name='slowmode')
@has_permissions(manage_channels=True)
async def setdelay(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)

    await ctx.send(
        f"The current slowmode for this channel is now {seconds} seconds!")


@bot.command(name='lockchannel')
@has_permissions(manage_channels=True)
async def lock(message):
    await message.channel.set_permissions(message.guild.default_role,
                                          send_messages=False)
    await message.send("Channel Locked 🔒")


@bot.command(name='unlockchannel')
@has_permissions(manage_channels=True)
async def unlock(message):
    await message.channel.set_permissions(message.guild.default_role,
                                          send_messages=True)
    await message.send("Channel Unlocked 🔓")


@bot.command(name='balance')
async def balance(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await getBankData()

    walletAmount = users[str(user.id)]["wallet"]
    bankAmount = users[str(user.id)]["bank"]

    BalanceEmbed = discord.Embed(title=f"{ctx.author.name}'s balance",
                                 color=0x00ff00)
    BalanceEmbed.add_field(name="Wallet Balance: ",
                           value="B$" + str(walletAmount))
    BalanceEmbed.add_field(name="Bank Balance: ", value="B$" + str(bankAmount))

    await ctx.send(embed=BalanceEmbed)


@bot.command(name='beg')
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await getBankData()

    Earns = random.randrange(105)

    await ctx.send(f"You got B${Earns} from begging")

    users[str(user.id)]["wallet"] += Earns

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


@bot.command(name='deposit')
async def deposit(message, depositamount: int):
    await open_account(message.author)

    user = message.author
    users = await getBankData()

    walletAmount = users[str(user.id)]["wallet"]

    if depositamount <= walletAmount:
        users[str(user.id)]["wallet"] -= depositamount
        users[str(user.id)]["bank"] += depositamount
    else:
        return False

    await message.send("You deposited B$" + str(depositamount) +
                       " in your bank account")

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


@bot.command(name='dep')
async def deposit(message, depositamount: int):
    await open_account(message.author)

    user = message.author
    users = await getBankData()

    walletAmount = users[str(user.id)]["wallet"]

    if depositamount <= walletAmount:
        users[str(user.id)]["wallet"] -= depositamount
        users[str(user.id)]["bank"] += depositamount
    else:
        return False

    await message.send("You deposited B$" + str(depositamount) +
                       " in your bank account")

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


@bot.command(name='withdraw')
async def withdraw(message, withamount: int):
    await open_account(message.author)

    user = message.author
    users = await getBankData()

    bankAmount = users[str(user.id)]["bank"]

    if withamount <= bankAmount:
        users[str(user.id)]["wallet"] += withamount
        users[str(user.id)]["bank"] -= withamount
    else:
        return False

    await message.send("You withdrew B$" + str(withamount) +
                       " in your bank account")

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


@bot.command(name='with')
async def withdraw(message, withamount: int):
    await open_account(message.author)

    user = message.author
    users = await getBankData()

    bankAmount = users[str(user.id)]["bank"]

    if withamount <= bankAmount:
        users[str(user.id)]["wallet"] += withamount
        users[str(user.id)]["bank"] -= withamount
    else:
        return False

    await message.send("You withdrew B$" + str(withamount) +
                       " in your bank account")

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True

@bot.command(name='mybotperms')
async def balance(ctx):
    await get_perms(ctx.author)

    user = ctx.author
    users = await getRankData()

    CurRank = users[str(user.id)]["rank"]

    BalanceEmbed = discord.Embed(title="**Your rank is: **",
                                 description=CurRank,
                                 color=0x00ff00)

    await ctx.send(embed=BalanceEmbed)

@bot.command(name='give')
async def givetouser(message, giveuser : discord.Member, amount : int):
  await open_account(message.author)
  await open_account(giveuser)

  user = message.author
  users = await getBankData()

  walletAmount = users[str(user.id)]["wallet"]
  givewalletAmount = users[str(giveuser.id)]["wallet"]

  print("We got the variables")
  print(walletAmount)
  print(givewalletAmount)

  if walletAmount >= amount:
    print("Condition was satisfied")
    users[str(user.id)]["wallet"] -= amount
    users[str(giveuser.id)]["wallet"] += amount
    print("added to giver account")
    await message.send("Sent B$" + str(amount) + " to " + f"{giveuser.mention}")
  else:
    await message.send("You don't have enough to give to that person.")


  with open("mainbank.json", "w") as f:
    json.dump(users, f)
  return True

@bot.command(name='calculator')
async def calc(message, number: int, operator, secondNumber: int):

    if operator == "+":
        result = number + secondNumber
    elif operator == "-":
        result = number - secondNumber
    elif operator == "*":
        result = number * secondNumber
    elif operator == "x":
        result = number * secondNumber
    elif operator == "/":
        result = number // secondNumber
    else:
        await message.send("That is not a valid operator")

    ResultEmbed = discord.Embed(title="The result is: ",
                                description=result,
                                color=0x00ff00)

    await message.send(embed=ResultEmbed)


@bot.command(name='bet')
@commands.cooldown(1, 15, commands.BucketType.user)
async def bet(message, betamount: int):
    await open_account(message.author)

    user = message.author
    users = await getBankData()
    walletAmount = users[str(user.id)]["wallet"]

    RNG = random.randint(0, 5)

    if RNG == 3:

        if walletAmount >= betamount:
            users[str(user.id)]["wallet"] += betamount

            BetEmbed = discord.Embed(title="You won!", color=0x00ff00)
            await message.send(embed=BetEmbed)
        else:
            await message.send("You don't have enough money.")

    else:
        if walletAmount >= betamount:
            users[str(user.id)]["wallet"] -= betamount

            BetEmbed = discord.Embed(title="You lost!", color=0x00ff00)
            await message.send(embed=BetEmbed)
        else:
            await message.send("You don't have enough money.")

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


@bot.command(name='ban')
@has_permissions(ban_members=True)
async def ban(message, memberName: discord.Member, *, memberReason=None):
    await memberName.ban(reason=memberReason)
    await message.send(f'{memberName} was banned')


@bot.command(name='kick')
@has_permissions(kick_members=True)
async def ban(message, memberName: discord.Member, *, memberReason=None):
    await memberName.kick(reason=memberReason)
    await message.send(f'{memberName} was kicked')


@bot.command(name='delete')
@has_permissions(manage_channels=True)
async def clear(message, amount=1):
    await message.channel.purge(limit=amount)
    await message.channel.purge(limit=1)

    purgeEmbed = discord.Embed(
        title="Deleted Messages",
        description="You deleted " + str(amount) +
        " messages\n**THIS MESSAGE WILL DELETE AUTOMATICALLY**, DO NOT SEND ANY MESSAGES AFTER THIS OR IT WILL DELETE THAT MESSAGE INSTEAD."
    )

    await message.send(embed=purgeEmbed)
    await asyncio.sleep(5)
    await message.channel.purge(limit=1)


@bot.command(name='hack')
async def hack(message, memberHack):

    RandomPass = [
        "\"sammylol7\"", "\"iLoveICEcream\"", "\"whatMCs*it\"", "\"n**ga90\""
    ]

    RandomDMs = [
        "\"I love cookies\"", "\"show me the things\"",
        "\"what's the server ip?\"",
        "\"You haven't talked to me in a while :(\""
    ]


    await message.send("Hacking " + memberHack + "...")
    await asyncio.sleep(3)

    await message.send("Getting TCP Packets...")
    await asyncio.sleep(3)

    await message.send("Bruteforcing into account...")
    await asyncio.sleep(3)

    await message.send("Getting Discord Password...")
    await asyncio.sleep(3)

    await message.send("Checking DMs...")
    await asyncio.sleep(3)

    await message.send("Bruteforcing into network...")
    await asyncio.sleep(3)

    await message.send("Getting IP Address...")
    await asyncio.sleep(3)

    await message.send("Failed to get IP Address")
    await asyncio.sleep(3)

    await message.send(memberHack + "\'s last DM was " + random.choice(RandomDMs))
    await message.send(memberHack + "\'s password is " + random.choice(RandomPass))


@bot.command(name='mute')
@has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

    for channel in guild.channels:
        await channel.set_permissions(mutedRole,
                                      speak=False,
                                      send_messages=False)
    embed = discord.Embed(title="Muted",
                          description=f"{member.mention} was muted ",
                          colour=discord.Colour.light_gray())
    embed.add_field(name="Reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(
        f"You have been muted from: {guild.name} reason: {reason}")


@bot.command(name='unmute')
@has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f"You have been unmuted from: - {ctx.guild.name}")
    embed = discord.Embed(title="Unmute",
                          description=f"Unmuted {member.mention}",
                          colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)

@bot.command(name='whois')
async def whois(ctx,user:discord.Member=None):

    if user==None:
        user=ctx.author

    rlist = []
    for role in user.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)

    b = ", ".join(rlist)


    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_footer(text=f'Requested by - {ctx.author}',
  icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID:',value=user.id,inline=False)
    embed.add_field(name='Name:',value=user.display_name,inline=False)

    embed.add_field(name='Created at:',value=user.created_at,inline=False)
    embed.add_field(name='Joined at:',value=user.joined_at,inline=False)



    embed.add_field(name='Bot?',value=user.bot,inline=False)

    embed.add_field(name=f'Roles:({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Top Role:',value=user.top_role.mention,inline=False)

    await ctx.send(embed=embed)

@bot.command(name='ping')
async def justleavemealone(message):
    latency = round(bot.latency * 10000)
    await message.send(f'Pong **{latency} ms**!')


@bot.command(name='setup', pass_context=True)
async def botsetup(ctx):
    setupembed = discord.Embed(title="Bot Requirements and Setup")
    setupembed.add_field(
        name="Role Requirements",
        value=
        "Please put the EaZ role above members role or put the default bot role above members"
    )
    setupembed.add_field(
        name="Announcment Channel",
        value=
        "If you do not want the bot to send all bot announcements to the first channel of your server, run z-setchannel [channelnamehere]"
    )
    setupembed.add_field(name="More setup options will be added soon.",
                         value="Coming Soon")

    await ctx.send(embed=setupembed)


@bot.command(name='serverprofile')
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(title=name + " Server Information",
                          description=description,
                          color=discord.Color.green())
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)


@bot.command(name='broadcast')
async def broadcast(ctx, *, msg):
    await get_perms(ctx.author)

    user = ctx.author
    users = await getRankData()

    userperm = users[str(user.id)]["rank"]

    if userperm == "✅ Bot Owner" or userperm == "🛠️ Utilitator":
        await ctx.send("Sent " + msg + " to every server")
        for server in bot.guilds:
            if True:
                if await get_channel(server.id):
                    c = await get_channel(server.id)
                    channel = bot.get_channel(c)
                    print(c)
                    await channel.send(msg)
                else:
                    for channel in server.text_channels:
                        print("id/name is " + str(channel))
                        try:
                            await channel.send(msg)
                        except Exception:
                            continue
                        else:
                            break
    else:
        await ctx.send("Function Denied")


@bot.command(name='staffchat')
async def getprivstaff(message):
    await get_perms(message.author)

    user = message.author
    users = await getRankData()

    userperms = users[str(user.id)]["rank"]

    if userperms == "✅ Bot Owner" or userperms == "🛠️ Utilitator" or userperms == "👍 Tester":
        await message.send("Check your DMs for the chat")
        await message.author.send(my_secret)
    else:
        await message.send("Function Denied")


@bot.command(name='setchannel')
@has_permissions(manage_guild=True)
async def channelSet(ctx, *, id):
    print("omg function ran")
    print(ctx.guild.id)
    print(id)
    await add_channel(ctx.guild.id, id)
    await ctx.send("Current Announcment Channel set to " + id)

@bot.command(name='replit')
async def getrepl(message):
    await get_perms(message.author)

    user = message.author
    users = await getRankData()

    userperms = users[str(user.id)]["rank"]

    if userperms == "✅ Bot Owner" or userperms == "🛠️ Utilitator" or userperms == "👍 Tester":
        await message.send("https://replit.com/@BotMakerHM/EaZ#main.py")
    else:
        await message.send("Function Denied")

# Tester Commands

@bot.command(name='testerinstructions')
async def giveInstructions(message):
    await get_perms(message.author)

    user = message.author
    users = await getRankData()

    userperms = users[str(user.id)]["rank"]

    if userperms == "✅ Bot Owner" or userperms == "🛠️ Utilitator" or userperms == "👍 Tester":
        await message.send("Any Instructions will be put here.")
    else:
        await message.send("Function Denied")


@bot.command(name='punch')
async def punch(message, personpunch: discord.Member):
    await get_perms(message.author)

    user = message.author
    users = await getRankData()

    userperms = users[str(user.id)]["rank"]

    if userperms == "✅ Bot Owner" or userperms == "🛠️ Utilitator" or userperms == "👍 Tester":
        await message.send(
            f"{personpunch.mention} has been punched by {message.author.mention}"
        )
    else:
        await message.send("Function Denied")


@bot.command(name='jail')
async def punch(message, personjailed: discord.Member, reasonjailed, charge):
    await get_perms(message.author)

    user = message.author
    users = await getRankData()

    userperms = users[str(user.id)]["rank"]

    if userperms == "✅ Bot Owner" or userperms == "🛠️ Utilitator" or userperms == "👍 Tester":
        await message.send(
            f"I have orders to arrest {personjailed.mention}, he is being jailed due to "
            + reasonjailed + " and has been charged with " + charge)

        await message.send(
            f"{personjailed.mention} has been put to jail by {message.author.mention}"
        )
    else:
        await message.send("Function Denied")

# Ignore
async def get_channel(server):
    file = await getServerChannel()
    if str(server) in file:
        return int(file[str(server)]["channel"])
    else:
        return False


async def add_channel(server, channel):
    print("yes")
    file = await getServerChannel()
    id = re.findall("\d+", channel)[0]
    print(id)
    file[str(server)] = {}
    file[str(server)]["channel"] = id
    with open("channel.json", "w") as f:
        json.dump(file, f)
    print("file saved")


async def getServerChannel():
    print("test")
    with open("channel.json", "r") as f:
        print("loading file")
        channel = json.load(f)
        print("file loaded")
    return channel


async def getEventData():
    with open("events.json", "r") as f:
        events = json.load(f)
    return events


async def get_perms(user):

    users = await getRankData()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["rank"] = "💬 Bot User"

    with open("ranks.json", "w") as f:
        json.dump(users, f)
    return True


async def getRankData():
    with open("ranks.json", "r") as f:
        users = json.load(f)
    return users


async def open_account(user):

    users = await getBankData()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


async def getBankData():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users

#passinput = input("Password: ")

#while passinput != password:
  #passinput = input("Password: ")

bot.run(TOKEN)
