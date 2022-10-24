# -*- coding: utf-8 -*-
import base64
import httplib2
import json
import urllib

from MoinMoin import log
from MoinMoin import user
from MoinMoin.auth import BaseAuth, LoginReturn, CancelLogin, ContinueLogin, get_multistage_continuation_url
from MoinMoin.auth import MultistageRedirectLogin
from MoinMoin.util import random_string

logging = log.getLogger(__name__)

http = httplib2.Http(disable_ssl_certificate_validation=True)


class OpenIDConnectError(Exception):
    error = {'error': None}
    descriptions = {
        'access_denied': "Access denied"  # User cancelled authentication
    }

    def __init__(self, error, description=None):
        self.error = error
        self.description = description

    def __str__(self):
        description = self.descriptions.get(self.error, self.description)
        if description:
            return '%s, error: %s' % (description, self.error)
        else:
            return 'error: %s' % self.error


def load_jwt(jwt, audience=None):
    """
    load jwt without signature check, because we get the jwt direct from the ID provider
    """
    segments = jwt.split('.')

    if len(segments) != 3:
        raise OpenIDConnectError('id_token_error', 'Wrong number of segments in token: %s' % jwt)

    # signed = '%s.%s' % (segments[0], segments[1])
    # signature = urlsafe_b64decode(segments[2])

    # Parse token.
    json_body = urlsafe_b64decode(segments[1])
    try:
        parsed = json.loads(json_body)
    except:
        raise OpenIDConnectError('id_token_error', 'Can\'t parse token: %s' % json_body)

    # Check audience.
    if audience is not None:
        aud = parsed.get('aud')
        if aud is None:
            raise OpenIDConnectError('id_token_error', 'No aud field in token: %s' % json_body)
        if aud != audience:
            raise OpenIDConnectError('id_token_error', 'Wrong recipient, %s != %s: %s' % (aud, audience, json_body))

    return parsed


def _json_encode(data):
    return json.dumps(data, separators=(',', ':'))


def urlsafe_b64encode(raw_bytes):
    return base64.urlsafe_b64encode(raw_bytes).rstrip('=')


def urlsafe_b64decode(b64string):
    # Guard against unicode strings, which base64 can't handle.
    b64string = b64string.encode('ascii')
    padded = b64string + '=' * (4 - len(b64string) % 4)
    return base64.urlsafe_b64decode(padded)


def get_state(request):
    state = request.request.args.get('state', '')
    try:
        data = json.loads(urlsafe_b64decode(state))
    except Exception as e:
        raise OpenIDConnectError('invalid_state', "State '%s' can't be load in to JSON. '%s'" % (state, e))
    """
    if 'oidc_nonce' in request.session:
        nonce = request.session['oidc_nonce']  
        del request.session['oidc_nonce']
        if (nonce == data.get('nonce')):
            return data        
        raise OpenIDConnectError('invalid_state', 'nonce %s invalid' % data.get('nonce'))
    else:
        raise OpenIDConnectError('invalid_state', 'nonce not found in session')
    """
    return data


def build_state(request, data=None):
    """
    data can be a dict with additional information
    """
    if data is None:
        data = {}
    nonce = random_string(64, "abcdefghijklmnopqrstuvwxyz0123456789")
    request.session['oidc_nonce'] = nonce

    # save the session. This is needed because MultistageRedirectLogin calls abort(rederict_uri) 
    # and then the sessin is not saved
    # request.cfg.session_service.finalize(request, request.session)

    # data.update({'nonce': nonce})
    return urlsafe_b64encode(_json_encode(data))


class OpenIDConnectAuth(BaseAuth):
    name = 'oauth2'
    login_inputs = ['special_no_input']
    logout_possible = True
    response_type = 'code'

    def __init__(self, client_id, client_secret, application, auth_uri, token_uri, userinfo_uri,  # not used
                 cert_uri, scope='openid profile email'):
        self.application = application
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_uri = auth_uri
        self.token_uri = token_uri
        self.userinfo_uri = userinfo_uri
        self.cert_uri = cert_uri

    @property
    def certs(self):
        if not self.cert_uri:
            return None

        if not hasattr(self, '_certs'):
            content = http.request(self.cert_uri)[1]
            self._certs = json.loads(content)
        return self._certs

    def get_userinfo(self, token):
        headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip',
            'authorization': '%s %s' % (token.get('token_type', ''), token['access_token']),
        }
        response, content = http.request(self.userinfo_uri, headers=headers)
        if response.status != 200:
            raise OpenIDConnectError("invalid_response", response)

        userinfo = json.loads(content)
        return userinfo

    def get_access_token_from_code(self, redirect_uri, code):
        query = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }

        body = urllib.urlencode(query)
        response, content = http.request(self.token_uri, method='POST', body=body, headers=headers)
        if response.status != 200:
            raise OpenIDConnectError("invalid_response", response)

        content = json.loads(content)

        if content.get('error'):
            description = content.get('error_description')
            error = content.get('error')
            raise OpenIDConnectError(error, description)

        return content

    def get_authentication_uri(self, request):
        data = {'next': request.request.base_url}
        redirect_uri = get_multistage_continuation_url(request, self.name)
        query = {
            'scope': self.scope,
            'client_id': self.client_id,
            'state': build_state(request, data),
            'response_type': self.response_type,
            'redirect_uri': redirect_uri,
        }

        return "%s?%s" % (self.auth_uri, urllib.urlencode(query))

    def update_or_create_user(self, request, userinfo):
        # workaround for moin 1.9.8
        if (getattr(user, 'CACHED_USER_ATTRS', None) is not None) and 'uuid' not in user.CACHED_USER_ATTRS:
            user.CACHED_USER_ATTRS += ['uuid']

        user_id = user._getUserIdByKey(request, 'uuid', userinfo['sub'])
        user_obj = user.User(request, id=user_id, auth_method=self.name, name=userinfo['name'],
                             auth_username=userinfo['name'])
        user_obj.uuid = userinfo['sub']
        user_obj.email = userinfo['email']
        user_obj.name = userinfo['name']

        try:
            roles = userinfo['roles'].split()
        except KeyError:
            roles = ''

        user_obj.disabled = False
        user_obj.roles = roles
        user_obj.save()
        return user_obj

    def _connect_user(self, request):
        _ = request.getText
        try:
            error = request.request.args.get('error')
            if error:
                raise OpenIDConnectError(error)

            state = get_state(request)
            next_url = state['next']
            code = request.request.args.get('code')

            # We need the redirect uri for the token request
            redirect_uri = get_multistage_continuation_url(request, self.name)

            # get the auth token       
            token = self.get_access_token_from_code(redirect_uri, code)

            # get the userdate with the token
            userinfo = load_jwt(token['id_token'], self.client_id)

            # update or create the user
            user_obj = self.update_or_create_user(request, userinfo)

            # hack to redirect to the original requested uri  
            user_obj.next_url = next_url

            if user_obj.valid:
                return LoginReturn(user_obj, True)
        except OpenIDConnectError as e:
            return CancelLogin(_('OpenID Connect failure. %s') % e)

        return CancelLogin(_('Sorry, your account is currently not registered for this Wiki.'))

    def login(self, request, user_obj, **kw):
        continuation = kw.get('multistage')
        if continuation:
            return self._connect_user(request)

        # simply continue if something else already logged in successfully
        if user_obj and user_obj.valid:
            return ContinueLogin(user_obj)

        redirect_uri = self.get_authentication_uri(request)

        return MultistageRedirectLogin(redirect_uri)
