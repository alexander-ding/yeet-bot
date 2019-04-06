from collections import defaultdict
from settings import Setting
from utils import download_filter, download_image, apply_overlay, process_image
from discord.ext.commands import Bot

import os

TOKEN = os.environ["YEETBOT_TOKEN"]

prefix = "!yeet "
client = Bot(command_prefix=prefix)

user_settings = defaultdict(Setting)

async def say(context, msg):
    return await client.send_message(context.message.channel, "{} {}".format(msg, context.message.author.mention))

@client.command(name='overlay',
                description="Overlays one image over all faces in another image.",
                brief="Overlays one image over all faces in another image.",
                aliases=['yeet'],
                pass_context=True)
async def overlay(context):
    if len(context.message.attachments) == 0:
        url = str(context.message.content)[(len(prefix+"overlay ")):]
        username = str(context.message.author)
        ok, err, background = download_image(url)
        if not ok:
            await say(context, err)
            return
        foreground = user_settings[username].get_foreground_image()
        try:
            io_buffer = apply_overlay(background, foreground, user_settings[username])
        except:
            await say(context, "Cannot overlay! Sorry mate")
        await client.send_file(context.message.channel, io_buffer, filename="new.jpeg")

@client.command(name='clean',
                description="Cleans your filter with an alpha layer",
                brief="Cleans the *rim* of your filter",
                pass_context=True)
async def clean(context):
    if str(context.message.author) not in user_settings.keys():
        await say(context, "Set a filter first with !yeet set [url]")
        return
    im = user_settings[str(context.message.author)].get_foreground_image()
    im = process_image(im)

    with open("pictures/{}.png".format(context.message.author), mode="wb") as fp:
        im.save(fp)
    user_settings[str(context.message.author)].foreground = "{}.png".format(context.message.author)

    with open("pictures/{}.png".format(context.message.author), mode="rb") as fp:
        await client.send_file(context.message.channel, fp, filename="cleaned.png")
        await say(context, "Cleaned it up for ya")

@client.command(name='set',
                description="Sets your custom filter to superimpose on people's faces. Pass a link or an attachment! A filter is stored for each user",
                brief="Sets image to replace faces",
                pass_context=True)
async def set_filter(context):
    if len(context.message.attachments) == 0:
        url = str(context.message.content)[(len(prefix+"set ")):]
        username = str(context.message.author)
        ok, s = download_filter(url, username)
        if ok:
            user_settings[username].foreground = s
            await say(context, "Gotcha")
        else:
            await say(context, s)
    else:
        await say(context, "Attachment is still being developed")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)