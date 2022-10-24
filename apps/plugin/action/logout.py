# -*- coding: utf-8 -*-
"""
    MoinMoin - logout action

    The real logout is done in MoinMoin.request.
    Here is just some stuff to notify the user.

    @copyright: 2005-2006 Radomirs Cirskis <nad2000@gmail.com>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.Page import Page


def execute(pagename, request):
    return LogoutHandler(pagename, request).handle()


class LogoutHandler:
    def __init__(self, pagename, request):
        self.request = request
        self._ = request.getText
        self.page = Page(request, pagename)

    def handle(self):
        _ = self._
        request = self.request
        # if the user really was logged out say so,
        # but if the user manually added ?action=logout
        # and that isn't really supported, then don't
        if not self.request.user.valid:
            self.request.theme.add_msg(_("You are now logged out."), "info")
            # self.request.theme.add_msg(_("To protect your privacy:<br>If you are using a shared/public computer, please close all open browser windows and start a new session by opening a new browser window."), "warning")
            if getattr(request.cfg, 'logout_service', None):
                next_page = request.cfg.logout_service
                request.theme.send_title(_("Logout"), pagename=self.page.page_name,
                                         pi_refresh=(0, next_page))
                request.write("<p>You will be redirected to <a href='%s'>%s</a>. </p>" %
                              (next_page, "If not click the link"))
                request.theme.send_footer(self.page.page_name)
                request.theme.send_closing_html()
                return

        return self.page.send_page()
