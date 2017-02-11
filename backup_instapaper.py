# -*- encoding: utf-8
"""
This script backs up my Instapaper bookmarks.
"""

import argparse
import json

from instapaper import Instapaper
import keyring


def dump_attributes(obj):
    return {attr: getattr(obj, attr)
            for attr in dir(obj)
            if not attr.startswith('_') and not callable(getattr(obj, attr))}


class KeychainError(Exception):
    pass


def load_credentials(service, keys):
    """Load credentials from the system keychain.

    :param service: The name of the service. e.g. 'instapaper'
    :param keys: A list of credentials to look up.
        e.g. ['username', 'password']

    """
    if isinstance(keys, str):
        keys = [keys]

    credentials = {key: keyring.get_password(service, key) for key in keys}
    for key, value in credentials.items():
        if value is None:
            raise KeychainError(
                'Empty keychain item: (%r, %r)' % (service, key))
    return credentials


def fetch_all_bookmarks(api, folder_id):
    """Retrieves all the bookmarks for an Instapaper folder, ready for
    JSON serialisation."""
    bookmarks = []
    while True:
        new_bookmarks = api.bookmarks(
            folder=folder_id,
            have=','.join(b['bookmark_id'] for b in bookmarks),
            limit=500)
        if not new_bookmarks:
            break
        new_bookmarks = [dump_attributes(b) for b in new_bookmarks]
        if all(b in bookmarks for b in new_bookmarks):
            break
        bookmarks.extend(new_bookmarks)
        if len(new_bookmarks) < 500:
            break

    for b in bookmarks:
        del b['parent']

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

    data = {}

    folders = api.folders()
    data['folders'] = folders

    data['bookmarks'] = {}
    for folder_id in ('unread', 'archive'):
        data['bookmarks'][folder_id] = fetch_all_bookmarks(
            api=api, folder_id=None)

    for folder in folders:
        bookmarks = fetch_all_bookmarks(api=api, folder_id=folder['folder_id'])
        data['bookmarks'][folder['title']] = bookmarks

    json.dump(data, open(path, 'w'), indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
