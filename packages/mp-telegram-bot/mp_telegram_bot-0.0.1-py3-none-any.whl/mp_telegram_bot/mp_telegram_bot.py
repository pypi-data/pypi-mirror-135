#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Meltingplot Telegram Bot Module."""

import base64
import hashlib
import json
import logging
import os
import tempfile
import time
import urllib.parse
from pathlib import Path

import attr

import imageio as iio

import requests

from telegram.ext import CommandHandler
from telegram.ext import PicklePersistence
from telegram.ext import Updater

from .config import Config
from .duet.api import RepRapFirmware

config = None
duet = None
logger = None


def start(update, context):
    if 'retries' not in context.user_data:
        context.user_data['retries'] = 0

    if 'active' in context.user_data and context.user_data['active'] is True:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Hi {0}, I already know you.').format(
                update.effective_user.first_name,
            ),
        )
    elif len(update.message.text.split(' ')) > 1:
        return register(update, context)
    elif (
        context.bot_data['in_challenge_response'] < time.time()
        and context.user_data['retries'] < 5
    ):
        context.bot_data['in_challenge_response'] = time.time() + 360
        context.user_data['retries'] = context.user_data['retries'] + 1

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                'Hi {0}, I\'m your Meltingplot 3D printer. Please follow the'
                ' instructions on your printers DWC.'
            ).format(
                update.effective_user.first_name,
            ),
        )

        challenge = base64.b64encode(
            os.urandom(32)).decode('utf-8').replace('+', '') \
            .replace('=', '').replace('/', '')[:32]

        challenge_hash = hashlib.sha256()
        challenge_hash.update(challenge.encode('utf-8'))
        context.user_data['challenge'] = challenge_hash.digest()

        bot_user = context.bot.get_me()

        gcode = (
            'M291 R"Register Telegram User" P"Send '
            '<a href=""https://t.me/{1}?start={0}"">'
            '/start {2}</a>  to {1}"'
            ' S1 T60'.format(
                urllib.parse.quote_plus(challenge),
                bot_user.username,
                challenge,
            )
        )

        duet.rr_gcode(gcode)
    else:
        update.message.reply_text(
            'Hi {0}, please be patient, there is already a challenge response'
            ' in progress. Try again later.'.format(
                update.effective_user.first_name,
            ),
        )


def register(update, context):
    try:
        challenge = update.message.text.split(' ', 1)[1].strip()
        challenge_hash = hashlib.sha256()
        challenge_hash.update(challenge.encode('utf-8'))
        local_challenge = context.user_data['challenge']

        if len(challenge) == 32 and challenge_hash.digest() == local_challenge:
            context.user_data['active'] = True
            update.message.reply_text(
                'Hi {0}, welcome!'.format(update.effective_user.first_name),
            )
            context.user_data.pop('challenge', None)
            context.user_data.pop('retries', None)
            context.bot_data['in_challenge_response'] = 0
        else:
            update.message.reply_text('The provided challenge is not valid!')
    except (KeyError, IndexError):
        update.message.reply_text('The provided challenge is not valid!')


def unregister(update, context):
    if (
        'active' not in context.user_data
        or context.user_data['active'] is not True
    ):
        return

    update.message.reply_text('Bye.')
    context.user_data.pop('active', None)


def webcam(update, context):
    if (
        'active' not in context.user_data
        or context.user_data['active'] is not True
    ):
        return

    with tempfile.NamedTemporaryFile(suffix='.mp4') as video_out:
        w = iio.get_writer(video_out.name, format='FFMPEG', mode='I', fps=1)
        for _ in range(0, 5):
            w.append_data(
                iio.imread(
                    iio.core.urlopen(config.webcam_url).read(),
                    '.jpg',
                ),
            )
            time.sleep(1)
        w.close()

        video_out.seek(0)

        context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=video_out,
        )


def check_for_user_request(context):
    message = duet.rr_model(
        key='state.messageBox',
        verbose=True,
        include_null=True,
    )['result']

    logger.debug("state.messageBox: {0}".format(message))

    try:
        if message['message'] == "waiting for telegram bot ...":
            # acknowledge message
            duet.rr_gcode('M292 P0')

            bot_user = context.bot.get_me()

            gcode = (
                'M291 P"Send '
                '<a href=""https://t.me/{0}?start"">'
                '/start</a>  to {0}"'
                ' S1 T60'.format(bot_user.username)
            )

            duet.rr_gcode(gcode)
    except (TypeError, KeyError) as e:
        logger.debug(e)


def main():
    global config
    global duet
    global logger

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )

    logger = logging.getLogger(__name__)

    try:
        with open('config/config.json') as f:
            config_dict = {
                k: v
                for (k, v) in json.loads(f.read()).items() if k[0] != '_'
            }
            config = Config(**config_dict)
    except FileNotFoundError:
        p = Path('./config')
        p.mkdir(parents=True, exist_ok=True)

        config = Config()
        config_dict = attr.asdict(config)
        with open('./config/config.json', mode='w') as f:
            f.write(json.dumps(
                config_dict,
                indent=4,
            ))

    logger.info(
        'Connect to duet on {0} with password {1}...'.format(
            config.duet_api_address,
            config.duet_api_password[:3],
        ),
    )

    duet = RepRapFirmware(
        address=config.duet_api_address,
        password=config.duet_api_password,
    )
    duet.connect()

    board = duet.rr_model(key='boards[0]')
    logger.info('Connected to Duet Board {0}'.format(board['result']))

    try:
        duet_config_file = duet.rr_download(
            '0:/sys/meltingplot/telegram-config.json',
        ).decode('utf-8')

        logger.debug('received telegram config file.')
        logger.debug('Content: {0}'.format(duet_config_file))

        try:
            duet_config_dict = {
                k: v
                for (k, v) in json.loads(duet_config_file).items()
                if k[0] != '_'
            }
            duet_config = Config(**duet_config_dict)
        except Exception as e:
            logger.exception(e)

        logger.debug(
            'New Telegram Token: {0}'.format(duet_config.telegram_token),
        )

        config_dict['telegram_token'] = duet_config.telegram_token
        config.telegram_token = duet_config.telegram_token
        with open('config/config.json', 'w') as f:
            f.write(json.dumps(
                config_dict,
                indent=4,
            ))
            duet.rr_delete('0:/sys/meltingplot/telegram-config.json')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            pass
        else:
            raise e from e

    logger.info(
        'Connecting to Telegram using token: {0}...'.format(
            config.telegram_token[:4],
        ),
    )

    persistence = PicklePersistence(filename='printerbot-persistence.dat')
    updater = Updater(
        token=config.telegram_token,
        persistence=persistence,
        use_context=True,
    )
    dispatcher = updater.dispatcher
    dispatcher.bot_data['in_challenge_response'] = 0.0

    start_handler = CommandHandler('start', start)
    register_handler = CommandHandler('register', register)
    unregister_handler = CommandHandler('unregister', unregister)
    webcam_handler = CommandHandler('webcam', webcam)

    updater.job_queue.run_repeating(
        check_for_user_request,
        interval=30,
        first=30,
    )

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(unregister_handler)
    dispatcher.add_handler(webcam_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
