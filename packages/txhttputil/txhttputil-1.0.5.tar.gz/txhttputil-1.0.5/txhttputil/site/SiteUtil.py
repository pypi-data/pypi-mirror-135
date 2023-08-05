"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import pem
import logging
import platform
from typing import Optional

from twisted.internet import reactor
from twisted.internet.ssl import DefaultOpenSSLContextFactory
from twisted.web import server

from txhttputil.login_page.LoginElement import LoginElement
from txhttputil.site.AuthCredentials import (
    AllowAllAuthCredentials,
    AuthCredentials,
)
from txhttputil.site.AuthSessionWrapper import FormBasedAuthSessionWrapper
from txhttputil.site.FileUploadRequest import FileUploadRequest
from txhttputil.site.RedirectToHttpsResource import RedirectToHttpsResource
from txwebsocket.txws import WebSocketUpgradeHTTPChannel

logger = logging.getLogger(__name__)


def setupSite(
    name: str,
    rootResource,
    portNum: int = 8000,
    credentialChecker: AuthCredentials = AllowAllAuthCredentials(),
    enableLogin=True,
    SiteProtocol=WebSocketUpgradeHTTPChannel,
    redirectFromHttpPort: Optional[int] = None,
    sslBundleFilePath: Optional[str] = None,
):
    """Setup Site
    Sets up the web site to listen for connections and serve the site.
    Supports customisation of resources based on user details

    @return: Port object
    """
    if redirectFromHttpPort is not None:
        setupSite(
            name="%s https redirect" % name,
            portNum=redirectFromHttpPort,
            rootResource=RedirectToHttpsResource(portNum),
            enableLogin=False,
        )

    LoginElement.siteName = name

    if enableLogin:
        protectedResource = FormBasedAuthSessionWrapper(
            rootResource, credentialChecker
        )
    else:
        logger.critical("Resource protection disabled NO LOGIN REQUIRED")
        protectedResource = rootResource

    site = server.Site(protectedResource)
    site.protocol = SiteProtocol
    site.requestFactory = FileUploadRequest

    if sslBundleFilePath:
        proto = "https"
        contextFactory = pem.twisted.certificateOptionsFromFiles(
            sslBundleFilePath
        )
        sitePort = reactor.listenSSL(portNum, site, contextFactory)

    else:
        proto = "http"
        sitePort = reactor.listenTCP(portNum, site)

    if platform.system() is "Linux":
        import subprocess

        ip = (
            subprocess.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
        )
    else:
        ip = "0.0.0.0"

    logger.info(
        "%s is alive and listening on %s://%s:%s",
        name,
        proto,
        ip,
        sitePort.port,
    )
    return sitePort


class RedirectionRule:
    def __init__(self, origin: str = "", destination: str = ""):
        """A definition of Resource redirection rule
        :param str from: a source uri as in twisted.web.http.Request
        :param str to: a destination url.
        """
        self._origin: str = origin
        self._destination: str = destination

    @property
    def origin(self) -> bytes:
        return self._origin.encode()

    @property
    def destination(self) -> bytes:
        return self._destination.encode()
