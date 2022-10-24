# -*- coding: utf-8 -*-
"""
changed the moin code, that the cookie is deleted with a browser close
"""

import time
from MoinMoin import log

logging = log.getLogger(__name__)

from MoinMoin.web.session import FileSessionService, _get_session_lifetime, get_cookie_name


class MyFileSessionService(FileSessionService):
    def finalize(self, request, session):
        if request.user.auth_method == 'setuid':
            userobj = request._setuid_real_user
            setuid = request.user.id
        else:
            userobj = request.user
            setuid = None
        logging.debug("finalize userobj = %r, setuid = %r" % (userobj, setuid))

        cfg = request.cfg
        # we use different cookie names for different wikis:
        cookie_name = get_cookie_name(request, name=cfg.cookie_name, usage=self.cookie_usage)
        # we always use path='/' except if explicitly overridden by configuration,
        # which is usually not needed and not recommended:
        cookie_path = cfg.cookie_path or '/'
        # a secure cookie is not transmitted over unsecure connections:
        cookie_secure = (cfg.cookie_secure or  # True means: force secure cookies
                         cfg.cookie_secure is None and request.is_secure)  # None means: https -> secure cookie

        cookie_lifetime = _get_session_lifetime(request, userobj)
        # we use 60s granularity, so we don't trigger session storage updates too often
        cookie_expires = int(time.time() / 60) * 60 + cookie_lifetime
        # when transiting logged-in -> logged out we want to kill the session
        # to protect privacy (do not show trail, even if anon sessions are on)
        kill_session = not userobj.valid and 'user.id' in session
        if kill_session:
            logging.debug("logout detected, will kill session")
        if cookie_lifetime and not kill_session:
            logging.debug("setting session cookie: %r" % (session.sid,))
            request.set_cookie(cookie_name, session.sid,
                               max_age=None, expires=None,
                               # changed this to None because i want to have the seesion expire on close
                               path=cookie_path, domain=cfg.cookie_domain,
                               secure=cookie_secure, httponly=cfg.cookie_httponly)
        elif not session.new:
            # we still got a cookie, but we don't want it. kill it.
            logging.debug("deleting session cookie!")
            request.delete_cookie(cookie_name, path=cookie_path, domain=cfg.cookie_domain)

        def update_session(key, val):
            """ put key/val into session, avoid writing if it is unchanged """
            try:
                current_val = session[key]
            except KeyError:
                session[key] = val
            else:
                if val != current_val:
                    session[key] = val

        if not session.new:
            # add some info about expiry to the sessions, so we can purge them.
            # also, make sure we notice server-side if a session is expired, do
            # not rely on the client to expire the cookie.
            update_session('expires', cookie_expires)

        if cookie_lifetime and not kill_session:
            # we have set the cookie, now update the session store

            if userobj.valid:
                # we have a logged-in user
                update_session('user.id', userobj.id)
                update_session('user.auth_method', userobj.auth_method)
                update_session('user.auth_attribs', userobj.auth_attribs)
                if setuid:
                    update_session('setuid', setuid)
                elif 'setuid' in session:
                    del session['setuid']
                logging.debug("storing valid user into session: %r" % userobj.name)
            else:
                # no logged-in user (not logged in or just has logged out)
                for key in ['user.id', 'user.auth_method', 'user.auth_attribs',
                            'setuid', ]:
                    if key in session:
                        del session[key]
                logging.debug("no valid user, cleaned user info from session")

            if ((not userobj.valid and not session.new  # anon users with a cookie (not first request)
                 or userobj.valid)  # logged-in users, even if THIS was the first request (no cookie yet)
                    # XXX if UA doesn't support cookies, this creates 1 session file per request
                    and
                    session.should_save):  # only if we really have something (modified) to save
                store = self._store_get(request)
                logging.debug("saving session: %r" % session)
                store.save(session)
        elif not session.new:
            # we killed the cookie (see above), so we can kill the session store, too
            logging.debug("destroying session: %r" % session)
            self.destroy_session(request, session)
