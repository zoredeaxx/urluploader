#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy
import os
from PIL import Image
import time
import pyrogram
from pyrogram import Client, filters
logging.getLogger("pyrogram").setLevel(logging.WARNING)

DL ="./thumb"


@Client.on_message(pyrogram.filters.photo)
async def save_photo(bot, update):
    if update.media_group_id is not None:
        # album is sent
        download_location = DL + "/" + str(update.from_user.id) + "/" + str(update.media_group_id) + "/"
        # create download directory, if not exist
        if not os.path.isdir(download_location):
            os.makedirs(download_location)
        await bot.download_media(
            message=update,
            file_name=download_location
        )
    else:
        # received single photo
        download_location = DL + "/" + str(update.from_user.id) + ".jpg"
        await bot.download_media(
            message=update,
            file_name=download_location
        )
        await bot.send_message(
            chat_id=update.chat.id,
            text="**Saved Thumbnail Successfully**",
            reply_to_message_id=update.message_id
        )


@Client.on_message(pyrogram.filters.command(["delthumb"]))
async def delete_thumbnail(bot, update):
    download_location = DL + "/" + str(update.from_user.id)
    try:
        os.remove(download_location + ".jpg")
        # os.remove(download_location + ".json")
    except:
        pass
    await bot.send_message(
        chat_id=update.chat.id,
        text="**Deleted Thumbnail Successfully**",
        reply_to_message_id=update.message_id
    )
