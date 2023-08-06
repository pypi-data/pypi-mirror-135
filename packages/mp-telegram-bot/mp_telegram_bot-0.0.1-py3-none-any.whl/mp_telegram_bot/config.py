#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Telegram Bot Config Module."""

import attr


@attr.s
class Config():
    """Config Class.

    This config class is a storage classe for config values.
    """

    duet_api_address = attr.ib(type=str, default="10.42.0.2")
    duet_api_password = attr.ib(type=str, default="meltingplot")
    webcam_url = attr.ib(
        type=str,
        default="http://10.42.0.3/picture/1/current/",
    )
    telegram_token = attr.ib(type=str, default="")
