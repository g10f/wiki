# -*- coding: utf-8 -*-
"""
    MoinMoin - Password change preferences plugin

    @copyright: 2012 Gunnar Scherf <gunnar@g10f.de>,
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.userprefs import UserPrefBase
from MoinMoin.widget import html


class Settings(UserPrefBase):
    def __init__(self, request):
        UserPrefBase.__init__(self, request)
        self.request = request
        self._ = request.getText
        _ = request.getText
        self.cfg = request.cfg
        self.title = _("Single Sign On Settings")
        self.name = 'diamondway_sso'

    @property
    def url(self):        
        return self.cfg.forced_service_settings
    
    def allowed(self):
        return (not 'diamondway_sso' in self.cfg.user_form_remove and
                not 'diamondway_sso' in self.cfg.user_form_disable and
                UserPrefBase.allowed(self) and
                not 'diamondway_sso' in self.request.user.auth_attribs)

    def create_form(self, create_only=False, recover_only=False):
        _ = self._
        ret = html.P()
        ret.append(html.Text(_("Please choose:")))
        ret.append(html.BR())
        items = html.UL()
        ret.append(items)

        lnk = html.LI().append(html.A(href=self.url).append(html.Text(self.title)))
        items.append(lnk)
        return unicode(ret)
