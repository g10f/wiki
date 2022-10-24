# -*- coding: utf-8 -*-
u"""
    MoinMoin - YouTube macro Version 0.1
               Displays an iframe with the wanted video.

    <<YouTube(id="YouTubeID")>>

    Examples:
     * <<YouTube(id=2SXKM-dLJV8)>>

    @copyright: 2014 by GunnarScherf (https://g10f.de),
    @license: GNU GPL, see COPYING for details.


    @TODO:
     * Check if youtube videos are disabled (mimetypes_xss).

"""

from MoinMoin import wikiutil


def macro_YouTube(macro, target=wikiutil.required_arg(unicode)):
    parameters = {
        "target": wikiutil.escape(target),
    }
    html = u"""<iframe width="640" height="360" src="//www.youtube.com/embed/%(target)s?feature=player_embedded" frameborder="0" allowfullscreen></iframe>""" % parameters

    return macro.formatter.rawHTML(html)
