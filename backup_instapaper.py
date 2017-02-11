# -*- encoding: utf-8
"""
This script backs up my Instapaper bookmarks.
"""

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


def backup_instapaper(path):
    credentials = load_credentials(
        service='instapaper',
        keys=['oauth_key', 'oauth_secret', 'username', 'password'])

    ip = Instapaper(
        oauthkey=credentials['oauth_key'],
        oauthsec=credentials['oauth_secret'])
    ip.login(
        username=credentials['username'],
        password=credentials['password'])

    data = {}

    folders = ip.folders()
    data['folders'] = folders

    data['bookmarks'] = {}
    for folder_id in ('unread', 'archive'):
        data['bookmarks'][folder_id] = fetch_all_bookmarks(
            api=ip, folder_id=None)

    for folder in folders:
        bookmarks = fetch_all_bookmarks(api=ip, folder_id=folder['folder_id'])
        data['bookmarks'][folder['title']] = bookmarks

    json.dump(data, open(path, 'w'), indent=2, sort_keys=True)
