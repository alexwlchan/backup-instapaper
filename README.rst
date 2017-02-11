backup-instapaper
=================

This is a Python script for backing up your bookmarks from Instapaper.  It
mimics
the `HTML/CSV export function <https://instapaper.zendesk.com/hc/en-us/articles/227342807-How-to-export-your-saved-articles>`_
provided by Instapaper, but in script form.

Installation
************

This script can run in Python 2 or Python 3.  Create a virtualenv and install
dependencies:

.. code-block:: console

   $ git clone git@github.com:alexwlchan/backup-instapaper.git
   $ cd backup-instapaper
   $ virtualenv env
   $ source env/bin/activate
   $ pip install -r requirements.txt

You also need to get an OAuth key/secret for the Instapaper API.  You can
register for these `on the Instapaper website <https://www.instapaper.com/main/request_oauth_consumer_token>`_.

Usage
*****

Run the script, passing your username, password, and API keys as command-line
flags:

.. code-block:: console

   $ python backup_instapaper.py --username=USERNAME --password=PASSWORD --oauthkey=OAUTHKEY --oauthsec=OAUTHSEC

This will write your bookmarks to ``instapaper_bookmarks.json``.

For all the options, use the ``--help`` flag:

.. code-block:: console

   $ python backup_instapaper.py --help

License
*******

This script is licensed under the MIT license.
