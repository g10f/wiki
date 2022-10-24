# -*- coding: utf-8 -*-
"""
    MoinMoin - PageLink Macro
    
    Create the Page Link only if the user has read access to the page

    @copyright: 2014 Gunnar Scherf <gunnar@g10f.de>
    @license: GNU GPL, see COPYING for details.
"""
from MoinMoin.Page import Page


def macro_PageLink(macro, pagename):
    request = macro.request

    page = Page(request, pagename)
    if page.exists() and request.user.may.read(pagename):
        f = macro.formatter
        return f.pagelink(1, pagename, generated=1) + f.text(pagename) + f.pagelink(0, pagename)
    else:
        return ''
