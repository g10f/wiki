# -*- coding: utf-8 -*-

from custom.baseconfig import BaseConfig


class FarmConfig(BaseConfig):
    base_sso_uri = 'https://sso.g10f.de'
    logout_service = base_sso_uri + '/accounts/logout/'
    # link for sso userprefs plugin
    forced_service_settings = base_sso_uri + '/accounts/me/'

    # Security Settings
    superuser = [u"GunnarScherf"]
    acl_rights_default = u"GunnarScherf:admin,read,write,delete,revert UserGroup:admin,read,write,delete,revert GuestGroup:read"
    acl_rights_before = u"GunnarScherf:admin,read,write,delete,revert AdminGroup:admin,read,write,delete,revert +UserGroup:admin"
    acl_hierarchic = True

    theme_default = 'memodump'
    logo_string = None
    language_default = 'de'
    page_front_page = u'StartSeite'
    page_jump_start = u'StartHilfe'
    navi_bar = [
        page_front_page,
        page_jump_start,
        u'RecentChanges',
        u'FindPage',
        u'HelpContents',
    ]


wikis = [
    ("g10f", r"^http(s?)://(localhost:\d+|wiki.g10f.de)/.*"),
]
