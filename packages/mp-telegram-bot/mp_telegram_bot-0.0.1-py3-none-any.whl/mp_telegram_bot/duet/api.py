#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Duet Web Control HTTP Api Module."""

import datetime
from zlib import crc32

import attr

import requests
from requests.adapters import HTTPAdapter

from urllib3.util.retry import Retry


class HTTPAdapterTimeout(HTTPAdapter):
    """Specialized HTTPAdapter with default Timeout."""

    __attrs__ = [
        'max_retries',
        'config',
        '_pool_connections',
        '_pool_maxsize',
        '_pool_block',
        'timeout',
    ]

    # pylint: disable=R0913
    def __init__(
        self,
        pool_connections=requests.adapters.DEFAULT_POOLSIZE,
        pool_maxsize=requests.adapters.DEFAULT_POOLSIZE,
        max_retries=requests.adapters.DEFAULT_RETRIES,
        pool_block=requests.adapters.DEFAULT_POOLBLOCK,
        timeout=30,
    ):
        """Initialize HTTPAdapterTimeout class."""
        super().__init__(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=max_retries,
            pool_block=pool_block,
        )

        self.timeout = timeout

    def send(
        self,
        request,
        stream=False,
        timeout=None,
        verify=True,
        cert=None,  # pylint: disable=R0913
        proxies=None,
    ):
        """Send request with timeout."""
        if timeout is None or self.timeout < timeout:
            timeout = self.timeout

        return super().send(
            request=request,
            stream=stream,
            timeout=timeout,
            verify=verify,
            cert=cert,
            proxies=proxies,
        )


def reauthenticate(retries=3):
    """Reauthenticate HTTP API requests."""
    status = {'retries': retries}

    def decorator(f):

        def inner(*args, **kwargs):
            while status['retries']:
                try:
                    return f(*args, **kwargs)
                except requests.HTTPError as e:
                    status_code = e.response.status_code
                    status['retries'] -= 1
                    if status_code == 401:
                        response = args[0].reconnect()
                        if response['err'] == 0:
                            status['retries'] = retries
                    else:
                        raise e from e
            raise Exception(
                'Retried {} times to reauthenticate.'.format(retries),
            )

        return inner

    return decorator


@attr.s
class RepRapFirmware():
    """RepRapFirmware API Class."""

    address = attr.ib(type=str, default="10.42.0.2")
    password = attr.ib(type=str, default="meltingplot")
    session_timeout = attr.ib(type=int, default=8000)
    http_timeout = attr.ib(type=int, default=15)
    http_retries = attr.ib(type=int, default=3)

    def connect(self) -> dict:
        retry = Retry(
            total=self.http_retries,
            read=self.http_retries,
            connect=self.http_retries,
            redirect=30,
            status=0,  # don't retry on bad status - we need to log this
            backoff_factor=0.3,
        )

        self.adapter = HTTPAdapterTimeout(
            max_retries=retry,
            timeout=self.http_timeout,
        )

        return self.reconnect()

    def reconnect(self) -> dict:
        url = 'http://{0}/rr_connect'.format(self.address)

        params = {
            'password': self.password,
        }

        self.session = requests.session()
        self.session.mount('https://', self.adapter)
        self.session.mount('http://', self.adapter)

        r = self.session.get(url, params=params)

        json_response = r.json()

        if json_response['err'] == 0:
            self.session_timeout = json_response['sessionTimeout']

        return json_response

    def disconnect(self) -> dict:
        url = 'http://{0}/rr_disconnect'.format(self.address)

        r = self.session.get(url)

        return r.json()

    @reauthenticate()
    def rr_model(
        self,
        key=None,
        frequently=False,
        verbose=False,
        include_null=False,
        include_obsolete=False,
        depth=99,
    ) -> dict:
        url = 'http://{0}/rr_model'.format(self.address)

        flags = []

        if frequently:
            flags.append('f')

        if verbose:
            flags.append('v')

        if include_null:
            flags.append('n')

        if include_obsolete:
            flags.append('o')

        flags.append('d{:d}'.format(depth))

        params = {
            'key': key if key is not None else '',
            'flags': ''.join(flags),
        }

        r = self.session.get(url, params=params)
        r.raise_for_status()

        return r.json()

    @reauthenticate()
    def rr_gcode(self, gcode) -> str:
        url = 'http://{0}/rr_gcode'.format(self.address)

        params = {
            'gcode': gcode,
        }

        r = self.session.get(url, params=params)
        r.raise_for_status()

        return self.rr_reply()

    @reauthenticate()
    def rr_reply(self) -> str:
        url = 'http://{0}/rr_reply'.format(self.address)

        r = self.session.get(url)
        r.raise_for_status()

        return r.text

    @reauthenticate()
    def rr_download(self, filepath) -> bytes:
        url = 'http://{0}/rr_download'.format(self.address)

        params = {
            'name': filepath,
        }

        r = self.session.get(url, params=params)
        r.raise_for_status()

        return r.content

    @reauthenticate()
    def rr_upload(
        self,
        filepath: str,
        content: bytes,
        last_modified: datetime.datetime = None,
    ) -> bytes:
        url = 'http://{0}/rr_upload'.format(self.address)

        params = {
            'name': filepath,
        }

        if last_modified is not None:
            params['time'] = last_modified.isoformat(timespec='seconds')

        try:
            checksum = crc32(content) & 0xffffffff
        except TypeError:
            content = content.encode('utf-8')
            checksum = crc32(content) & 0xffffffff

        params['crc32'] = '{0:x}'.format(checksum)

        r = self.session.post(url, data=content, params=params)
        r.raise_for_status()

        return r.content

    @reauthenticate()
    def rr_filelist(self, directory: str) -> object:
        url = 'http://{0}/rr_filelist'.format(self.address)

        params = {
            'dir': directory,
        }

        r = self.session.get(url, params=params)
        r.raise_for_status()

        return r.json()

    @reauthenticate()
    def rr_fileinfo(self, name: str = None) -> object:
        url = 'http://{0}/rr_fileinfo'.format(self.address)

        params = {}

        if name is not None:
            params['name'] = name

        r = self.session.get(url, params=params)
        r.raise_for_status()

        return r.json()

    @reauthenticate()
    def rr_mkdir(self, directory: str) -> object:
        """rr_mkdir Create a Folder.

        Create a Folder on the Duet.

        :param directory: Folder Path
        :type directory: str
        :return: Error Object
        :rtype: object
        """
        url = 'http://{0}/rr_mkdir'.format(self.address)

        params = {
            'dir': directory,
        }

        r = self.session.get(url, params=params)
        r.raise_for_status()

        return r.json()

    @reauthenticate()
    def rr_move(
        self,
        old_filepath: str,
        new_filepath: str,
        overwrite: bool = False,
    ) -> object:
        """rr_move Move File.

        Move a File on Filesystem.

        :param old_filepath: Source Filepath
        :type old_filepath: str
        :param new_filepath: Destination Filepath
        :type new_filepath: str
        :param overwrite: Override existing Destination, defaults to False
        :type overwrite: bool, optional
        :return: Error Object
        :rtype: object
        """
        url = 'http://{0}/rr_move'.format(self.address)

        params = {
            'old': old_filepath,
            'new': new_filepath,
            'deleteexisting': 'yes' if overwrite is True else 'no',
        }

        r = self.session.get(url, params=params)
        r.raise_for_status()

        return r.json()

    @reauthenticate()
    def rr_delete(self, filepath: str) -> object:
        """rr_delete delete remote file.

        Delete File on Duet.

        :param filepath: Filepath
        :type filepath: str
        :return: Error Object
        :rtype: object
        """
        url = 'http://{0}/rr_delete'.format(self.address)

        params = {
            'name': filepath,
        }

        r = self.session.get(url, params=params)
        r.raise_for_status()

        return r.json()
