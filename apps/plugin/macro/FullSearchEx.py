# -*- coding: utf-8 -*-
"""
    MoinMoin - FullSearchEx Macro

    <<FullSearchEx(Test)>>
        displays a search dialog

"""

from MoinMoin import wikiutil

Dependencies = ["pages"]


def search_box(title, macro):
    """ Make a search box


    @param title: search box type: 'titlesearch' or 'fullsearch'
    @rtype: unicode
    @return: search box html fragment
    """
    _ = macro._
    if 'value' in macro.request.values:
        default = wikiutil.escape(macro.request.values["value"], quote=1)
    else:
        default = ''

    boxes = [
        u'<br>',
        u'<input type="checkbox" name="context" value="160" checked="checked">',
        _('Display context of search results'),
        u'<br>',
        u'<input type="checkbox" name="case" value="1">',
        _('Case-sensitive searching'),
    ]
    boxes = u'\n'.join(boxes)
    button = _("Search Text")
    if title:
        title_input = u'<input type="hidden" name="title" value="%s">' % title
    else:
        title_input = ''
    # Format
    html = [
        u'<form method="get" action="%s">' % macro.request.href(macro.request.formatter.page.page_name),
        u'<div>',
        u'<input type="hidden" name="action" value="fullsearchex">',
        u'<input type="hidden" name="titlesearch" value="0">',
        u'<input type="hidden" name="advancedsearch" value="1">',
        title_input,
        u'<input type="text" name="and_terms" size="30" value="%s">' % default,
        u'<input type="submit" value="%s">' % button,
        boxes,
        u'</div>',
        u'</form>',
    ]
    html = u'\n'.join(html)
    return macro.formatter.rawHTML(html)


def execute(macro, title):
    request = macro.request
    _ = request.getText

    return search_box(title, macro)
