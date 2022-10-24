# -*- coding: utf-8 -*-
"""
    MoinMoin - LoginLink

    Usage:
        <<LoginLink('Please login')>>

    @copyright: 2010 Gunnar Scherf
    @license: GNU GPL, see COPYING for details

    changes:

"""

Dependencies = ["language"]


def macro_LoginLink(macro, text=u"Login"):
    if macro.request.user.valid:
        return ''

    _ = macro.request.getText
    text = _(text)
    page = macro.formatter.page
    url = page.url(macro.request, {'action': 'login', 'login': '1'})
    if hasattr(macro.request.cfg, 'autologin') and macro.request.cfg.autologin:
        script = '<script>window.location.href = "%s";</script>' % url
    else:
        script = ''

    return ''.join([macro.formatter.url(1, url, css='action'), macro.formatter.text(text), macro.formatter.url(0),
                   script])
