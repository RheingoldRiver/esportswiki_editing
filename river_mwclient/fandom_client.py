from .wiki_client import WikiClient
from .esports_session_manager import session_manager
from .auth_credentials import AuthCredentials


class FandomClient(object):
    """
    Functions for connecting to and editing specifically Gamepedia wikis.
    """
    client: WikiClient = None
    wiki: str = None

    def __init__(self, wiki: str, client: WikiClient = None,
                 credentials: AuthCredentials = None,
                 **kwargs):
        """
        Create a site object. Credentials are optional.
        :param wiki: Name of a wiki
        :param client: WikiClient object. If this is provided, SessionManager will not be used.
        :param credentials: Optional. Provide if you want a logged-in session.
        """
        self.wiki = wiki
        if client:
            # completely skip the session manager
            self.client = client
            return

        url = '{}.fandom.com'.format(wiki)

        self.client, session_manager.get_client(url=url,
                                                credentials=credentials,
                                                **kwargs
                                                )
