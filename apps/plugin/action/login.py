# -*- coding: utf-8 -*-
"""
    MoinMoin - login action

    The real login is done in MoinMoin.request.
    Here is only some user notification in case something went wrong.

    @copyright: 2005-2006 Radomirs Cirskis <nad2000@gmail.com>,
                2006 MoinMoin:ThomasWaldmann
    @license: GNU GPL, see COPYING for details.
    
    G. Scherf:
    redirect after successfull login, that we dont get problems with F5 Refresh
"""

from MoinMoin import userform, wikiutil
from MoinMoin.Page import Page
from MoinMoin.action.login import LoginHandler


def execute(pagename, request):
    return SSOLoginHandler(pagename, request).handle()


class SSOLoginHandler(LoginHandler):

    def handle(self):
        _ = self._
        request = self.request
        form = request.values

        islogin = form.get('login', '')

        if islogin:  # user pressed login button
            if request._login_multistage:
                return self.handle_multistage()
            if hasattr(request, '_login_messages'):
                for msg in request._login_messages:
                    request.theme.add_msg(wikiutil.escape(msg), "error")
            # redirect to the start page after login
            if request.user.valid:
                next_page = "/"
                pagename = self.page.page_name
                
                try:
                    # The Oauth2 SSO Login stores the next url in the user attribute
                    next_page = request.user.next_url
                except AttributeError:
                    next_page = Page(request, pagename).url(request, querystr={})

                request.theme.send_title(_("Login"), pagename=self.pagename,
                                         pi_refresh=(0, next_page))
                request.write("<p>You will be redirected to <a href='%s'>%s</a>. </p>" % 
                              (next_page, "If not click the link"))
                request.theme.send_footer(self.pagename)
                request.theme.send_closing_html()
                return
            else:
                return self.page.send_page()

        else:  # show login form
            request.theme.send_title(_("Login"), pagename=self.pagename)
            # Start content (important for RTL support)
            request.write(request.formatter.startContent("content"))

            request.write(userform.getLogin(request))

            request.write(request.formatter.endContent())
            request.theme.send_footer(self.pagename)
            request.theme.send_closing_html()
