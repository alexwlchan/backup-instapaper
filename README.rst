backup-instapaper
=================

This is a script for backing up your bookmarks from Instapaper.

It mimics the `HTML/CSV export function
<https://instapaper.zendesk.com/hc/en-us/articles/227342807-How-to-export-your-saved-articles>`_
provided by Instapaper, but in script form.

Installation
************

To install this script, use pip:

.. code-block:: console

   $ pip install -e git+git://github.com/alexwlchan/backup-instapaper.git#egg=backup_instapaper

or `pipsi <https://github.com/mitsuhiko/pipsi>`_:

.. code-block:: console

   $ pipsi install -e git+git://github.com/alexwlchan/backup-instapaper.git#egg=backup_instapaper


You can use Python 2.7 and Python 3.3+.

You also need to get an OAuth key/secret for the Instapaper API.  You can
register for these `on the Instapaper website <https://www.instapaper.com/main/request_oauth_consumer_token>`_.

Usage
*****

Run the script, passing your username, password, and API keys as command-line
flags:

.. code-block:: console

   $ backup_instapaper --username=USERNAME --password=PASSWORD --oauthkey=OAUTHKEY --oauthsec=OAUTHSEC

This will write your bookmarks to ``instapaper_bookmarks.json``.

For all the options, use the ``--help`` flag:

.. code-block:: console

   $ backup_instapaper --help

License
*******

This script is licensed under the MIT license.
