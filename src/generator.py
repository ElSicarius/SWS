


class Generation(object):

    def __init__(self, session, hosts: list, wordlist: list) -> None:
        """
        Init of the wordlist generator object
        """
        self.session = session
        self.hosts = hosts
        self.wordlist = wordlist
        self.set_hosts_generators()

    def set_hosts_generators(self) -> list:
        """
        Creates a list of generators with the hosts and wordlists items together
        """
        sane_hosts = set()
        for host in self.hosts:
            if not host.endswith("/"):
                sane_hosts.add(host+"/")
                continue
            sane_hosts.add(host)
        self.generators = [self.create_generator(
                                host,
                                self.wordlist,
                                self.session.payload_index) for host in sane_hosts]

    @staticmethod
    def create_generator(host: str, wordlist: list, offset: int=0):
        """
        creates a generator object for a host and it's associated wordlist
        """
        for item in wordlist[offset:]:
            if item.startswith("/"):
                item = item[1:]
            yield f"{host}{item}"

    def get_next_salve(self):
        """
        Iters through the generators and gets next salve of requests
        """
        salve = set()
        for generator in self.generators:
            try:
                salve.add(next(generator, None))
            except Exception as e:
                logger.error(e)
        self.session.payload_index += 1

        if len(list(salve)) == 1 and list(salve)[0] is None:
            return None
        return salve
