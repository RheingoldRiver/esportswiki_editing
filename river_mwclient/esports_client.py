from .cargo_client import CargoClient
from .wiki_client import WikiClient
from .esports_session_manager import session_manager
from .auth_credentials import AuthCredentials

ALL_ESPORTS_WIKIS = ['lol', 'halo', 'smite', 'vg', 'rl', 'pubg', 'fortnite',
                     'apexlegends', 'fifa', 'gears', 'nba2k', 'paladins', 'siege',
                     'default-loadout', 'commons', 'teamfighttactics']


class EsportsClient(object):
    """
    Functions for connecting to and editing specifically to Gamepedia esports wikis.

    If not using an esports wiki, please use GamepediaSite instead.
    """
    ALL_ESPORTS_WIKIS = ALL_ESPORTS_WIKIS
    cargo_client: CargoClient = None
    client: WikiClient = None
    wiki: str = None

    def __init__(self, wiki: str, client: WikiClient = None,
                 credentials: AuthCredentials = None, stg: bool = False,
                 **kwargs):
        """
        Create a site object.
        :param wiki: Name of a wiki
        :param client: WikiClient object. If this is provided, SessionManager will not be used.
        :param credentials: Optional. Provide if you want a logged-in session.
        :param stg: if it's a staging wiki or not
        """
        self.wiki = self.get_wiki(wiki)
        if client:
            # completely skip the session manager
            self.cargo_client = CargoClient(client)
            self.client = client
            return

        suffix = 'io' if stg else 'com'
        url = '{}.gamepedia.{}'.format(wiki, suffix)

        self.client, self.cargo_client = session_manager.get_client(url=url,
                                                                    credentials=credentials,
                                                                    **kwargs
                                                                    )

    @staticmethod
    def get_wiki(wiki):
        if wiki in ['lol', 'teamfighttactics'] or wiki not in ALL_ESPORTS_WIKIS:
            return wiki
        return wiki + '-esports'

    def standard_name_redirects(self):
        """
        TODO: move this to a separate library, this is too specific for inclusion here
        :return:
        """
        for item in self.cargo_client.query(
                tables="Tournaments,_pageData",
                join_on="Tournaments.StandardName_Redirect=_pageData._pageName",
                where="_pageData._pageName IS NULL AND Tournaments.StandardName_Redirect IS NOT NULL",
                fields="Tournaments.StandardName_Redirect=Name,Tournaments._pageName=Target",
                limit="max"
        ):
            page = self.client.pages[item['Name']]
            target = item['Target']
            page.save('#redirect[[%s]]' % target, summary="creating needed CM_StandardName redirects")

    def other_wikis(self):
        """
        :return: Generator of wiki names as strings, not site objects
        """
        for wiki in ALL_ESPORTS_WIKIS:
            if wiki == self.wiki:
                continue
            yield wiki

    def other_sites(self):
        for wiki in self.other_wikis():
            yield EsportsClient(wiki)

    @staticmethod
    def all_wikis():
        for wiki in ALL_ESPORTS_WIKIS:
            yield wiki

    @staticmethod
    def all_sites():
        """
        Use self.all_sites_logged_in() if you want to log in; this is deliberately static
        :return: Generator of all esports wikis as site objects
        """
        for wiki in ALL_ESPORTS_WIKIS:
            yield EsportsClient(wiki)

    def all_sites_logged_in(self):
        for wiki in ALL_ESPORTS_WIKIS:
            yield EsportsClient(wiki, username=self.client.username, password=self.client.password)
