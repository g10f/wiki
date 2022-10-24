# -*- coding: utf-8 -*-

import os
import sys

from MoinMoin.web.serving import make_application
from whitenoise import WhiteNoise

DIRNAME = os.path.dirname(os.path.dirname(__file__))

# Debug mode - show detailed error reports
# os.environ['MOIN_DEBUG'] = '1'

sys.path.insert(0, os.path.join(DIRNAME, 'config'))

# Creating the WSGI application
# use shared=True to have moin serve the builtin static docs
# use shared=False to not have moin serve static docs
# use shared='/my/path/to/htdocs' to serve static docs from that path
apps_static_files = os.path.join(DIRNAME, 'static')
root_static_files = os.path.join(DIRNAME, 'static/root')
moin_static_files = os.path.join(os.path.dirname(DIRNAME), 'venv/lib/python2.7/site-packages/MoinMoin/web/static/htdocs/')
data_static_files = os.path.join(os.getenv('WIKI_BASE_DIR', "/opt/g10f/wiki/"), 'data/static')

moin_app = make_application(shared=False)
application = WhiteNoise(moin_app, root=root_static_files)
application.add_files(root=apps_static_files, prefix='moin_static1911/')
application.add_files(root=moin_static_files, prefix='moin_static1911/')
application.add_files(root=data_static_files, prefix='moin_static1911/')
