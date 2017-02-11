#!/usr/bin/env python
# -*- encoding: utf-8
"""A script for backing up your Instapaper bookmarks.  Run with ``--help``
to get a usage message.

"""

from __future__ import unicode_literals

import argparse
import json

from instapaper import Instapaper
import keyring


def _bookmark_to_dict(bookmark):
    """Turns a bookmark into a dictionary.

    :param bookmark: An ``instapaper.Bookmark`` instance.

    """
    data = {}
    for field in ['bookmark_id', 'description', 'title', 'url', 'title',
                  'progress', 'progress_timestamp', 'starred']:
        data[field] = getattr(bookmark, field)
    return data


def fetch_all_bookmarks(api):
    """Fetches all the bookmarks for an account.

    Returns a dict of folder names and bookmarks.

    :param api: An ``Instapaper`` instance logged in to the Instapaper API.

    """
    # We have to retrieve the bookmarks from each folder in an account
    # individually, so start by getting a list of folders.
    folders = {f['folder_id']: f['title'] for f in api.folders()}

    # Unread and Archive aren't included in the ``folders()`` method,
    # but we still want to back them up.
    folders['archive'] = 'Archive'
    folders['unread'] = 'Unread'

    bookmarks = {}
    for folder_id, folder_title in folders.items():
        bookmarks[folder_title] = _fetch_bookmarks_for_folder(
            api=api, folder_id=folder_id)

    return bookmarks


def _fetch_bookmarks_for_folder(api, folder_id):
    """Fetches all the bookmarks for a given folder.

    :param api: An ``Instapaper`` instance logged in to the Instapaper API.
    :param folder_id: The folder ID, as returned by the ``folders`` method
        from the Instapaper API, or "unread" or "archive".

    """
    bookmarks = []
    while True:
        # Fetch the next batch of bookmarks from the API.  500 is the most
        # bookmarks we can fetch at once -- this lets us minimise API calls.
        new_bookmarks = api.bookmarks(
            folder=folder_id,
            have=','.join(b['bookmark_id'] for b in bookmarks),
            limit=500)

        # Add any new bookmarks.  Because we pass the ``have`` parameter,
        # the API guarantees that we aren't receiving any duplicates.
        new_bookmarks = [_bookmark_to_dict(b) for b in new_bookmarks]
        bookmarks.extend(new_bookmarks)

        # The next API call will be empty if there aren't any bookmarks left,
        # but checking here can save us an unnecessary API call.
        if len(new_bookmarks) < 500:
            break

    return bookmarks


def read_config():
    """Returns configuration for using the script.

    Configuration is read from one of two places:
     1. The system keychain
     2. Command-line arguments

    Command-line arguments take precedence over keychain values.  If the
    keychain values are empty/missing, the command-line switches are required.

    """
    # Read some initial config from the system keychain: if this doesn't
    # exist, then we require it from command-line arguments.
    username = keyring.get_password('instapaper', 'username')
    password = keyring.get_password('instapaper', 'password')
    oauthkey = keyring.get_password('instapaper', 'oauthkey')
    oauthsec = keyring.get_password('instapaper', 'oauthsec')

    parser = argparse.ArgumentParser(
        description='A script to back up bookmarks from Instapaper',
        epilog='This script requires API keys for Instapaper. You can get an '
               'API key from '
               'https://www.instapaper.com/main/request_oauth_consumer_token')

    parser.add_argument(
        '--output', default='instapaper_bookmarks.json',
        help='output path for the backup file')
    parser.add_argument(
        '--username', required=(username is None),
        help='Instapaper username')
    parser.add_argument(
        '--password', required=(password is None),
        help='Instapaper password')
    parser.add_argument(
        '--oauthkey', required=(oauthkey is None),
        help='OAuth key for the Instapaper API')
    parser.add_argument(
        '--oauthsec', required=(oauthsec is None),
        help='OAuth secret for the Instapaper API')

    config = vars(parser.parse_args())

    if config['username'] is None:
        config['username'] = username
    if config['password'] is None:
        config['password'] = password
    if config['oauthkey'] is None:
        config['oauthkey'] = oauthkey
    if config['oauthsec'] is None:
        config['oauthsec'] = oauthsec

    return config


def setup_api(username, password, oauthkey, oauthsec):
    """Set up an instance of the Instapaper API.

    :param username: Instapaper username
    :param password: Instapaper password
    :param oauthkey: OAuth key for the Instapaper API
    :param oauthsec: OAuth secret for the Instapaper API

    """
    api = Instapaper(oauthkey=oauthkey, oauthsec=oauthsec)
    api.login(username=username, password=password)
    return api


def main():
    """Use the Instapaper API to save bookmarks to disk."""
    config = read_config()
    api = setup_api(
        username=config['username'],
        password=config['password'],
        oauthkey=config['oauthkey'],
        oauthsec=config['oauthsec'])
    bookmarks = fetch_all_bookmarks(api)
    json.dump(bookmarks, open(config['output'], 'w'), sort_keys=True)


if __name__ == '__main__':
    main()
