import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

bc = commands.Bot(command_prefix='!')
allowed_Mentions = discord.AllowedMentions(everyone=True)


@bc.event
async def on_ready():
    print('We are logged in as {0.user}'.format(bc))


@bc.command()
async def ping(ctx):
    await ctx.send(f'Pong! `{round(bc.latency * 1000)}ms`')


@bc.command(pass_context=True)
@commands.has_permissions(manage_guild=True)
async def addrole(ctx, member: discord.Member, *, role: discord.Role = None):
    await ctx.message.delete()
    await member.add_roles(role)


@bc.command(pass_context=True)
@commands.has_permissions(manage_guild=True)
async def takerole(ctx, member: discord.Member, *, role: discord.Role = None):
    await ctx.message.delete()
    await member.remove_roles(role)


@bc.command(pass_context=True)
async def chnick(ctx, member: discord.Member, nick):
    await ctx.message.delete()
    await member.edit(nick=nick)


@bc.command(pass_context=True)
async def delnick(ctx, member: discord.Member):
    await ctx.message.delete()
    await member.edit(nick="")


@bc.command()
@commands.has_permissions(mention_everyone=True)
async def annce(ctx, *args):
    channel = bc.get_channel(884231052305006672)
    await ctx.message.delete()
    await channel.send('@everyone ' + ' '.join(args))


@bc.command()
async def invite(ctx, *args):
    await ctx.message.delete()
    await ctx.message.author.send("https://discord.gg/7fzHeKq88B")


@bc.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    await member.kick(reason=reason)


@bc.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    await member.ban(reason=reason)


@bc.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)


@bc.command()
@commands.has_permissions(manage_messages=True)
async def DM(ctx, member: discord.Member, *args):
    await ctx.message.delete()
    await member.send(' '.join(args))


@bc.event
async def on_message(message):
    if message.author == bc.user:
        return
    if isinstance(message.channel, discord.channel.DMChannel):
        guild = bc.get_guild(883760937427931166)
        channels = await guild.fetch_channels()
        channel = discord.utils.get(channels, name=message.author.id)
        message1 = message.author
        embedVar = discord.Embed(
            title=f'{message.author} has sent a new message',
            description=message.content,
            color=0xff0000)
        category = discord.utils.get(guild.categories, id=884233102837317632)
        embedMod = discord.Embed(
            title='Information for the mods',
            description='!close- Closes the text channel'
            '\n!DM- To DM the user anonymously. Use same command format as normal.',
            color=0x00FF00)

        embedDirections = discord.Embed(
            title=f'Directions for use:',
            description=
            'Please send all replies within this channel, please and thank you, as this will keep the server clean on our end!',
            color=0xff0000)

        if channel == None:  #Channel doesn't exist yet. So create it
            channel = await guild.create_text_channel(
                message.author.name + "#" + message.author.discriminator,
                category=category,
                id=message.author.name + "#" + message.author.discriminator)

            await message.author.send(
                "Your ticket has been created in " + guild.name +
                ". You may proceed into the server and await support! Thank you for contacting us with your issue!"
            )

        await channel.send(embed=embedDirections)
        await channel.send(embed=embedMod)
        await channel.send(embed=embedVar)

    await bc.process_commands(message)


@bc.command()
@commands.has_permissions(manage_messages=True)
async def close(ctx):
    await ctx.channel.delete()


keep_alive()
bc.run(os.environ['TOKEN'])
