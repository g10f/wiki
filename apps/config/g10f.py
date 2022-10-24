# -*- coding: utf-8 -*-
import os
from custom.oauth2 import OpenIDConnectAuth
from farmconfig import FarmConfig


class Config(FarmConfig):
    auth = [OpenIDConnectAuth(
        auth_uri=FarmConfig.base_sso_uri + '/oauth2/authorize/',
        token_uri=FarmConfig.base_sso_uri + '/oauth2/token/',
        userinfo_uri=FarmConfig.base_sso_uri + '/api/v2/users/me/',
        cert_uri=FarmConfig.base_sso_uri + '/oauth2/certs/',
        application="d22e58c18f294cb09d1bd4878307bebd",
        client_id='109d95da417449b0b1509e2649ab7f34',
        client_secret=os.getenv('G10F_CLIENT_SECRET'))
    ]
    data_dir = FarmConfig.farm_dir + '/g10f/data/'
    sitename = u'G10F Wiki'
    html_head = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-YBNTRHE6MT"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
    
      gtag('config', 'G-YBNTRHE6MT');
    </script>
    <link rel="shortcut icon" href="/favicon.ico">
    <meta name="description" content="G10F Wiki">    
    """
    interwikiname = u'G10F'
    show_interwiki = 0
    openid_application = u"d22e58c18f294cb09d1bd4878307bebd"
