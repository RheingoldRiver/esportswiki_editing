from .wiki_client import WikiClient
from .gamepedia_client import GamepediaClient
from .cargo_client import CargoClient
from .auth_credentials import AuthCredentials


class EsportsSessionManager(object):
    """Manages instances of EsportsClient
    """
    existing_wikis = {}

    def get_client(self, url: str = None, credentials: AuthCredentials = None, **kwargs):
        if url in self.existing_wikis:
            return self.existing_wikis[url]['client'], self.existing_wikis[url]['cargo_client']
        client = WikiClient(url, path='/', credentials=credentials, **kwargs)
        cargo_client = CargoClient(client)
        self.existing_wikis[url] = {'client': client, 'cargo_client': cargo_client}
        return client, cargo_client


session_manager = EsportsSessionManager()
