# -*- coding: utf-8 -*-
import os
from MoinMoin.config import multiconfig
from MoinMoin.datastruct.backends.composite_groups import CompositeGroups
from MoinMoin.datastruct.backends.wiki_groups import WikiGroups
from session import MyFileSessionService
from wiki_groups import SSOGroups


class BaseConfig(multiconfig.DefaultConfig):
    base_dir = os.getenv('WIKI_BASE_DIR', "/opt/g10f/wiki/")
    mail_smarthost = os.getenv('WIKI_MAIL_SMARTHOST', "localhost")
    mail_from = os.getenv('WIKI_MAIL_FROM', "Wiki <noreply@g10f.de>")

    default_attachment_link = 'get'  # default for Attachment links is a get
    cookie_lifetime = (0.5, -1)  # anonymous_session_lifetime, logged_in_lifetime in hours
    default_do_action = 'get'
    # link for sso userprefs plugin
    session_service = MyFileSessionService()

    # don't let users change password or have multiple openid's
    userprefs_disabled = ['password', 'oid']
    user_form_disable = ['name', 'email']
    # remove some options from the large user preferences form
    user_form_remove = ['css_url', 'password', 'jid']

    farm_dir = base_dir + 'data/wikifarm/'
    plugin_dirs = [base_dir + 'apps/plugin']
    shared_intermap = base_dir + 'apps/config/interwikimap.txt'
    data_underlay_dir = base_dir + 'data/underlay/'
    xapian_index_dir = base_dir + 'data/xapian_index/'
    cache_dir = base_dir + 'data/cache'

    url_prefix = '/moin_static1911'

    # Security Settings
    groups = lambda cfg, request: CompositeGroups(request, SSOGroups(request), WikiGroups(request))
    acl_hierarchic = True

    page_front_page = u"FrontPage"
    navi_bar = [
        u'%(page_front_page)s',
        u'RecentChanges',
        u'FindPage',
        u'HelpContents',
    ]
    chart_options = {'width': 600, 'height': 300}
    xapian_search = True
    xapian_stemming = True
    cookie_httponly = True
    edit_locking = 'lock 5'
    tz_offset = 2.0
    surge_action_limits = {  # allow max. <count> <action> requests per <dt> secs
        # action: (count, dt)
        'show': (40, 60),
        'raw': (40, 40),  # some people use this for css
        'AttachFile': (640, 60),
        'diff': (60, 60),
        'fullsearch': (20, 60),
        'edit': (20, 120),
        'rss_rc': (2, 60),
        'default': (60, 60),
    }
    # surge_action_limits = None # disable surge protection
    # surge_lockout_time = 3600 # secs you get locked out when you ignore warnings
    user_checkbox_defaults = {'remember_me': 0, 'edit_on_doubleclick': 0}
    actions_excluded = multiconfig.DefaultConfig.actions_excluded + ['SyncPages', 'Despam', 'PackagePages', 'Load',
                                                                     'Save', 'RenderAsDocbook', 'MyPages', 'CopyPage',
                                                                     'moinexec', 'twikidraw', 'anywikidraw']
    editor_force = False
    editor_ui = 'freechoice'
    autologin = True
