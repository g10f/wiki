# -*- coding: utf-8 -*-
"""
    MoinMoin - Video

    Usage:
        <<Video(target, pagename)>>    

    Examples:
     * <<Video(video.webm)>>
     * <<Video(video.webm, PageName)>>

    @copyright: 2014 by GunnarScherf (https://g10f.de),
    @license: GNU GPL, see COPYING for details.

    changes:

"""

from MoinMoin import wikiutil
from MoinMoin.action import AttachFile


def macro_Video(macro, target=u"", pagename=None):
    request = macro.request
    _ = macro.request.getText
    fmt = macro.formatter

    # AttachFile calls always with pagename. Users can call the macro from a different page as the attachment is saved.
    if not pagename:
        pagename = fmt.page.page_name

    if not wikiutil.is_URL(target):
        pagename, fname = AttachFile.absoluteName(target, pagename)

        if not AttachFile.exists(request, pagename, fname):
            linktext = _('Upload new attachment "%(filename)s"') % {'filename': fname}
            target = AttachFile.getAttachUrl(pagename, fname, request, do='upload_form')
            return (fmt.url(1, target) +
                    fmt.text(linktext) +
                    fmt.url(0))

        url = AttachFile.getAttachUrl(pagename, fname, request)
    else:
        url = target

    video_src = "<video src=\"%s\" controls></video>" % url
    return fmt.rawHTML(video_src)
