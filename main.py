'''

Created by Anna Wahl

In this project, I created a discord bot that has the following features :
    - Logs on Discord and Sets Bot Status
    - Welcome and Leave Messages 
        - Administrators are able to create custom messages and embeds for both.
        - Administrators are also able to set custom welcome and leave channels as needed.
            - If the channels are not set by the administrator, the messages will be sent to the server's default event log channel.
    - Help Command
    - Placeholder Reference Page Command
        - Placeholders are able to be used in both welcome and leave messages, as well as in embeds.
    - Mute/Unmute Commands
    - Kick Command
    - Ban/Unban Commands
    - Custom Embeds
        - A Show Embed command references previously created embeds and displays them.

'''

# Import necessary packages
import discord, asyncio, datetime, random
from discord import utils, permissions
from datetime import datetime
from discord.ext import commands
from random import randint


client = commands.Bot(command_prefix="c!", intents=discord.Intents.all()) # Set bot prefix


# Initializing embeds dictionary
embeds = {}

# Set Status and Initialize Variables
@client.event
async def on_ready():

    global welcome_message, leave_message, leave_embed, welcome_embed, welcome_channel_id, leave_channel_id

    # Initializes welcome message variables
    welcome_message = None
    welcome_embed = None
    welcome_channel_id = None

    # Initializes leave message variables
    leave_message = None
    leave_embed = None
    leave_channel_id = None

    # Sets status
    game = discord.Game("c!Help")
    await client.change_presence(status=discord.Status.online, activity=game)
    print(f"Now logged in as {client.user}.")


# Send Welcome Message
@client.event
async def on_member_join(member):

    global welcome_message
    global welcome_channel_id
    global welcome_embed

    # Gets preset welcome channel
    if channel != None:
        channel=client.get_channel(welcome_channel_id)

    # Gets system messages channel if welcome channel is not set
    else:
        channel=client.get_channel(member.guild.system_channel.id)

    # Sends welcome message and embed
    await channel.send(content=welcome_message)
    await channel.send(embed=embeds[welcome_embed])


# Send Leave Message
@client.event
async def on_member_remove(member):

    global leave_message
    global leave_channel_id
    global leave_embed

    # Gets preset leave channel
    if channel != None:
        channel=client.get_channel(leave_channel_id)

    # Gets system messages channel if leave channel is not set
    else:
        channel=client.get_channel(member.guild.system_channel.id)
        
    # Sends leave message and embed
    await channel.send(content=leave_message)
    await channel.send(embed=embeds[leave_embed])


# Help Command
@client.command()
async def Help(ctx:commands.context):

    # Creates Embed
    embed = discord.Embed(
        title="╰┈➤ ❝ C O M M A N D S ❞",
        color=discord.Colour.from_rgb(43,45,49)
    )

    # embed.add_field(
    #    name="",
    #    value="",
    #    inline=False
    # )

    # Ban Command Instructions
    embed.add_field(
        name="c!Ban [member_ping] [reason]",
        value="> Bans a member. Must have administrator to use this command.",
        inline=False
    )

    # Create Embed Command Instructions
    embed.add_field(
        name="c!Embed_Create title=[title] | description=[description] | author=[author] | footer=[footer] | image=[image url] | thumbnail=[thumbnail url] | footer_url=[footer_url] | color=rgb [number], [number], [number] | author_url=[author_url] | timestamp=True/False",
        value="> Creates embedded message with title to be stored for later use. Must have administrator to use this command. See other help commands for additional assistance.",
        inline=False
    )

    # Show Embed Instructions
    embed.add_field(
        name="c!Embed_Show [title]",
        value="> Displays a previously created embedded message.",
        inline=False
     )
    
    # Help Instructions
    embed.add_field(
        name="c!Help",
        value="> Displays a list of all commands and explanations. Please note that commands are case sensitive.",
        inline=False
    )

    # Kick Command Instructions
    embed.add_field(
        name="c!Kick [member_ping] [reason]",
        value="> Kicks a member. Must have administrator to use this command.",
        inline=False
    )

    # Mute Command Instructions
    embed.add_field(
        name="c!Mute [member_ping] [reason]",
        value="> Creates a Muted Role and mutes a member. Must have administrator to use this command.",
        inline=False
    )

    # Placeholders Page Instructions
    embed.add_field(
        name="c!Placeholders",
        value="> Returns a full list of placeholders offered as well as their descriptions.",
        inline=False
     )
    
    embed.add_field(
        name="c!Set_Leave_Channel [channel ping]",
        value="> Sets channel for leave message. Must have administrator to use this command.",
        inline=False
    )

    embed.add_field(
        name="c!Set_Leave_Embed [embed title]",
        value="> Sets embed for leave message. Placeholders are able to be used. Must have administrator to use this command.",
        inline=False
    )

    embed.add_field(
        name="c!Set_Leave_Message [message]",
        value="> Sets leave message. Placeholders are able to be used. Must have administrator to use this command.",
        inline=False
    )

    embed.add_field(
        name="c!Set_Welcome_Channel [channel ping]",
        value="> Sets channel for welcome message. Must have administrator to use this command.",
        inline=False
    )

    embed.add_field(
        name="c!Set_Welcome_Embed [embed title]",
        value="> Sets embed for welcome message. Placeholders are able to be used. Must have administrator to use this command.",
        inline=False
    )

    embed.add_field(
        name="c!Set_Welcome_Message [message]",
        value="> Sets welcome message. Placeholders are able to be used. Must have administrator to use this command.",
        inline=False
    )

    # Unban Command Instructions
    embed.add_field(
        name="c!Unban [user_id] [reason]",
        value="> Unbans a previously banned member. Must have administrator to use this command.",
        inline=False
    )

    # Unmute Command Instructions
    embed.add_field(
        name="c!Unmute [member_ping] [reason]",
        value="> Unmutes a member. Must have administrator to use this command.",
        inline=False
    )


    # Sets thumbnail, footer, and timestamp
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.set_footer(text=f"Information requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.timestamp = datetime.now()

    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Placeholder Reference Command
@client.command()
async def Placeholders(ctx:commands.context):

    # Creates Embed
    embed = discord.Embed(
        title="╰┈➤ ❝ P L A C E H O L D E R S ❞",
        color=discord.Colour.from_rgb(43,45,49)
    )

    # {member_name} Placeholder
    embed.add_field(
        name="{member_name}",
        value="> Shows the message author's display name.",
        inline=True
    )

    # {member_mention} Placeholder
    embed.add_field(
        name="{member_mention}",
        value="> Mentions the author of the message.",
        inline=True
    )

    # Sets To Two Columns
    embed.add_field(name="\t", value="\t")

    # {member_id} Placeholder
    embed.add_field(
        name="{member_id}",
        value="> Displays the id of the message author.",
        inline=True
    )

    # {member_avatar} Placeholder
    embed.add_field(
        name="{member_avatar}",
        value="> Returns a url of the member's avatar.",
        inline=True
    )

    # Sets To Two Columns
    embed.add_field(name="\t", value="\t")
    
    # {server_name} Placeholder
    embed.add_field(
        name="{server_name}",
        value="> Displays the server name.",
        inline=True
    )

    # {server_id} Placeholder
    embed.add_field(
        name="{server_id}",
        value="> Displays the server id.",
        inline=True
    )

    # Sets To Two Columns
    embed.add_field(name="\t", value="\t")

    # {server_owner} Placeholder
    embed.add_field(
        name="{server_owner}",
        value="> Returns the server owner's name.",
        inline=True
    )

    # {server_icon} Placeholder
    embed.add_field(
        name="{server_icon}",
        value="> Returns the url of the server icon.",
        inline=True
     )
    
    # Sets To Two Columns
    embed.add_field(name="\t", value="\t")

    # {channel_mention} Placeholder
    embed.add_field(
        name="{channel_mention}",
        value="> Mentions channel in which the command was called.",
        inline=True
     )
    
    # {channel_name} Placeholder
    embed.add_field(
        name="{channel_name}",
        value="> Displays the name of the channel in which the command was called.",
        inline=True
     )
    
    # Sets To Two Columns
    embed.add_field(name="\t", value="\t")

    # {channel_id} Placeholder
    embed.add_field(
        name="{channel_id}",
        value="> Returns the id of the channel in which the command was called.",
        inline=True
     )

    # Sets thumbnail, footer, and timestamp
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.set_footer(text=f"Information requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.timestamp = datetime.now()
    
    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Ban Command
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Ban(ctx:commands.context, member:discord.Member, *, reason="No reason specified."):

    # Create embed
    embed = discord.Embed(
            title="╰┈➤ ❝ User Banned ❞",
            description=f"> {member.display_name.capitalize()} was banned.",
            color=discord.Colour.from_rgb(43,45,49)
        )

    # Adds reason for ban
    embed.add_field(
            name="Reason:",
            value=f"{reason}",
            inline=False
    )

    # Sets footer, thumbnail, and timestamp
    embed.set_footer(text=f"Banned by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.timestamp = datetime.now()

    # Bans user and sends reason to mod log
    await member.ban(reason=reason)

    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Create Embed Command
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Embed_Create(ctx: commands.context, *, contents):
    
    error = False # Allows for error checking within create embed command

    # Creates placeholder dictionary
    placeholders = {
        "{member_name}": ctx.author.display_name,
        "{member_mention}": ctx.author.mention,
        "{member_id}": str(ctx.author.id),
        "{member_avatar}": str(ctx.author.display_avatar),
        "{server_name}": ctx.guild.name,
        "{server_id}": str(ctx.guild.id),
        "{server_owner}": ctx.guild.owner,
        "{server_icon}": str(ctx.guild.icon),
        "{channel_mention}": ctx.channel.mention,
        "{channel_name}": ctx.channel.name,
        "{channel_id}": str(ctx.channel.id)
    }

    # Split contents in command
    contents_list = contents.split(" | ")
    
    # Create parameters dictionary
    parameters = {} 

    for content in contents_list:
        
        # Prepares contents to be added to embeds dictionary
        parameter_name, parameter_value = content.split("=")
        parameter_name = parameter_name.strip()
        parameter_value = parameter_value.strip()

        # Sets "color" or "colour" to "color"
        if parameter_name == "color" or parameter_name == "colour":
            parameter_name = "color"

        # Replaces placeholders
        for placeholder, value in placeholders.items():
            parameter_value = parameter_value.replace(placeholder, str(value))

        # Assigns embed parameter names and values to dicitonary
        parameters[parameter_name.lower()] = parameter_value
        
        # Converts color to rgb
        if parameter_name.lower() == "color":
            if parameter_value.startswith("rgb"):

                color_values = parameter_value[4:-1].split(", ")
                r, g, b = map(int, color_values)
                parameters["color"] = discord.Color.from_rgb(r, g, b)


        # Assigns timestamp if True
        if parameters.get("timestamp") == "True":
            parameters["timestamp"] = datetime.now()

        # Sets timestamp to none if Flase or None
        elif parameters.get("timestamp") == "False" or parameters.get("timestamp") == None:
            parameters["timestamp"] = None
        
        # Detects error in timestamp command
        else:

            error = True

            # Creates embed
            error_embed = discord.Embed(
                title="╰┈➤ ❝ E R R O R ❞",
                description=f"You entered an invalid timestamp. Please use c!EmbedHelp to get help with your embed.",
                color=discord.Colour.from_rgb(43,45,49)
            )

            # Sets embed footer, thumbnail, and timestamp
            error_embed.set_footer(text=f"Embed requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
            error_embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
            error_embed.timestamp = datetime.now()

            # Sends embed
            msg = await ctx.channel.send(embed=error_embed)

    # Continues if no error occurred
    if error == False:

        # Creates Embed
        embed = discord.Embed(
            title=parameters.get("title"),
            description=parameters.get("description"),
            color=parameters.get("color", discord.Colour.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        )

        # Sets embed footer, image, thumbnail, and timestamp
        embed.set_footer(text=parameters.get("footer"), icon_url=parameters.get("footer_url"))
        embed.set_image(url=parameters.get("image"))
        embed.set_thumbnail(url=parameters.get("thumbnail"))
        embed.timestamp=parameters.get("timestamp")

        # Sets author name and icon
        if parameters.get("author"):
            embed.set_author(name=parameters.get("author"), icon_url=parameters.get("author_url"))

        # Adds embed to embeds dictionary
        embeds[parameters.get("title")] = embed

        # Sends Embed
        msg = await ctx.channel.send(embed=embed)


# Show Embed Command
@client.command()
async def Embed_Show(ctx: commands.context, *, title):

    # If embed in embeds dictionary
    if embeds.get(title):

        # Send embed
        msg = await ctx.channel.send(embed=embeds[title])
    
    # If embed is not in embeds dictionary
    else:

        # Creates embed
        error_embed = discord.Embed(
            title="╰┈➤ ❝ E R R O R ❞",
            description=f"This embed does not exist.",
            color=discord.Colour.from_rgb(43,45,49)
        )

        # Sets embed footer, thumbnail, and timestamp
        error_embed.set_footer(text=f"Embed requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
        error_embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
        error_embed.timestamp = datetime.now()

        # Sends embed
        msg = await ctx.channel.send(embed=error_embed)


# Kick Command
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Kick(ctx:commands.context, member:discord.Member, *, reason="No reason specified."):

    # Create embed
    embed = discord.Embed(
            title="╰┈➤ ❝ User Kicked ❞",
            description=f"> {member.display_name.capitalize()} was kicked.",
            color=discord.Colour.from_rgb(43,45,49)
        )

    # Adds reason for kick
    embed.add_field(
            name="Reason:",
            value=f"{reason}",
            inline=False
    )

    # Sets footer, thumbnail, and timestamp
    embed.set_footer(text=f"Kicked by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.timestamp = datetime.now()

    # Kicks User
    await member.kick(reason=reason)

    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Mute Command
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Mute(ctx:commands.context, member:discord.Member, *, reason="No reason specified."):
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    # Creates Muted Role if Muted Role does not exist
    if role not in ctx.guild.roles:
        await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, speak=False))
        role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    # Overrides other roles to mute the user
    await role.edit(position=ctx.guild.me.top_role.position - 1)

    # Creates embed
    embed = discord.Embed(
        title="╰┈➤ ❝ User Muted ❞",
        description=f"> {member.display_name.capitalize()} was muted.",
        color=discord.Colour.from_rgb(43,45,49)
    )

    # Displays reasoning for mute
    embed.add_field(
        name="Reason:",
        value=f"{reason}",
        inline=False
    )

    # Sets embed footer, thumbnail, and timestamp
    embed.set_footer(text=f"Muted by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.timestamp = datetime.now()

    # Mutes User
    await member.add_roles(role)

    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Sets Leave Channel
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Set_Leave_Channel(ctx:commands.context, channel: discord.TextChannel):

    global leave_channel_id

    # Sets leave channel
    leave_channel_id = channel.id

    # Creates embed
    embed = discord.Embed(
            title="╰┈➤ ❝ Channel Set ❞",
            description=f"Your leave channel has been set.",
            color=discord.Colour.from_rgb(43,45,49)
        )
    
    # Sets embed footer, thumbnail, and timestamp
    embed.set_footer(text=f"Leave channel requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.timestamp = datetime.now()

    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Set Leave Embed
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Set_Leave_Embed(ctx:commands.context, *, leave_embed_title):

    global leave_embed

    # Sets leave embed
    leave_embed = leave_embed_title

    # Creates embed
    embed = discord.Embed(
            title="╰┈➤ ❝ Embed Set ❞",
            description=f"Your leave embed has been set.",
            color=discord.Colour.from_rgb(43,45,49)
        )
    
    # Sets footer, thumbnail, and timestamp
    embed.set_footer(text=f"Leave embed requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.timestamp = datetime.now()

    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Set Leave Message
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Set_Leave_Message(ctx: commands.context, *, message):

    global leave_message

    # Initializes placeholders dictionary
    placeholders = {
        "{member_name}": ctx.author.display_name,
        "{member_mention}": ctx.author.mention,
        "{member_id}": str(ctx.author.id),
        "{member_avatar}": str(ctx.author.display_avatar),
        "{server_name}": ctx.guild.name,
        "{server_id}": str(ctx.guild.id),
        "{server_owner}": ctx.guild.owner,
        "{server_icon}": str(ctx.guild.icon),
        "{channel_mention}": ctx.channel.mention,
        "{channel_name}": ctx.channel.name,
        "{channel_id}": str(ctx.channel.id)
    }

    # Replaces placeholders with value
    for placeholder, value in placeholders.items():
        message = message.replace(placeholder, str(value))

    # Sets leave message
    leave_message = message

    # Creates embed
    embed = discord.Embed(
            title="╰┈➤ ❝ Message Set ❞",
            description=f"Your leave message has been set.",
            color=discord.Colour.from_rgb(43,45,49)
        )
    
    # Sets embed footer, thumbnail, and timestamp
    embed.set_footer(text=f"Leave requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.timestamp = datetime.now()

    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Sets Welcome Channel
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Set_Welcome_Channel(ctx:commands.context, channel: discord.TextChannel):

    global welcome_channel_id

    # Sets welcome channel
    welcome_channel_id = channel.id

    # Creates embed
    embed = discord.Embed(
            title="╰┈➤ ❝ Channel Set ❞",
            description=f"Your welcome channel has been set.",
            color=discord.Colour.from_rgb(43,45,49)
        )
    
    # Sets footer, thumbnail, and timestamp
    embed.set_footer(text=f"Welcome channel requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.timestamp = datetime.now()

    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Sets Welcome Embed
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Set_Welcome_Embed(ctx:commands.context, *, welcome_embed_title):

    global welcome_embed

    # Sets welcome embed
    welcome_embed = welcome_embed_title

    # Creates Embed
    embed = discord.Embed(
            title="╰┈➤ ❝ Embed Set ❞",
            description=f"Your welcome embed has been set.",
            color=discord.Colour.from_rgb(43,45,49)
        )
    
    # Sets embed footer, thumbnail, and timestamp
    embed.set_footer(text=f"Welcome embed requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.timestamp = datetime.now()


# Set Welcome Message
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Set_Welcome_Message(ctx: commands.context, *, message):

    global welcome_message

    # Initializes placeholders dictionary
    placeholders = {
        "{member_name}": ctx.author.display_name,
        "{member_mention}": ctx.author.mention,
        "{member_id}": str(ctx.author.id),
        "{member_avatar}": str(ctx.author.display_avatar),
        "{server_name}": ctx.guild.name,
        "{server_id}": str(ctx.guild.id),
        "{server_owner}": ctx.guild.owner,
        "{server_icon}": str(ctx.guild.icon),
        "{channel_mention}": ctx.channel.mention,
        "{channel_name}": ctx.channel.name,
        "{channel_id}": str(ctx.channel.id)
    }

    # Replaces placeholders wtih values
    for placeholder, value in placeholders.items():
        message = message.replace(placeholder, str(value))

    # Sets welcome message
    welcome_message = message

    # Creates Embed
    embed = discord.Embed(
            title="╰┈➤ ❝ Message Set ❞",
            description=f"Your welcome message has been set.",
            color=discord.Colour.from_rgb(43,45,49)
        )
    
    # Sets embed footer, thumbnail, and timestamp
    embed.set_footer(text=f"Welcome requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
    embed.timestamp = datetime.now()

    # Sends embed
    msg = await ctx.channel.send(embed=embed)


# Unban Command
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Unban(ctx:commands.context, id: int, *, reason="No reason specified."):

    # Gets list of banned members
    banned = ctx.guild.bans()

    async for entry in banned:

        if entry.user.id == id: # If user is banned

            # Creates embed
            embed = discord.Embed(
                title="╰┈➤ ❝ User Unbanned ❞",
                description=f"> {entry.user.display_name.capitalize()} was unbanned.",
                color=discord.Colour.from_rgb(43,45,49)
            )

            # Adds reason for unban
            embed.add_field(
                name="Reason:",
                value=f"{reason}",
                inline=False
            )

            # Sets footer, thumbnail, and timestamp
            embed.set_footer(text=f"Unbanned by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
            embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
            embed.timestamp = datetime.now()

            # Unbans User and sends reason to mod log
            await ctx.guild.unban(discord.Object(id=id), reason=reason)

            # Sends embed
            msg = await ctx.channel.send(embed=embed)

            break
        
        else: # If user is not banned

            # Creates embed
            embed = discord.Embed(
                title="╰┈➤ ❝ User Not Found ❞",
                description=f"> {entry.user.display_name.capitalize()} was not found in the banned list. Are you sure this user was banned?",
                color=discord.Colour.from_rgb(43,45,49)
            )

            # Sets footer, thumbnail, and timestamp
            embed.set_footer(text=f"Ban requested by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
            embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
            embed.timestamp = datetime.now()
            
            # Sends embed
            msg = await ctx.channel.send(embed=embed)


    # Sends Embed
    msg = await ctx.channel.send(embed=embed)

    
# Unmute Command
@client.command()
@commands.has_permissions(administrator=True) # Admin Only Command
async def Unmute(ctx:commands.context, member:discord.Member, *, reason="No reason specified."):

    # Gets Muted Role
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    # If Muted Role does not exist, pass
    if role not in ctx.guild.roles:
        pass

    else:
        
        # Creates Embed
        embed = discord.Embed(
            title="╰┈➤ ❝ User Unmuted ❞",
            description=f"> {member.display_name.capitalize()} was unmuted.",
            color=discord.Colour.from_rgb(43,45,49)
        )

        # Adds Reason for Unmute
        embed.add_field(
            name="Reason:",
            value=f"{reason}",
            inline=False
        )

        # Sets footer, thumbnail and timestamp
        embed.set_footer(text=f"Muted by: {ctx.author.display_name.capitalize()}", icon_url="https://cdn3.emoji.gg/emojis/4730-modern-moderator.png")
        embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/2638-shinyredstaff.png")
        embed.timestamp = datetime.now()

        # Removes Muted Role
        await member.remove_roles(role)

        # Sends Embed
        msg = await ctx.channel.send(embed=embed)


# Run Bot with Token
client.run("TOKEN")
# Token will be reset after this bot is submitted for Global Hack Week
