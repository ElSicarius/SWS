
import argparse
from loguru import logger
from src.session import Session
import src.utils as utils
import requests
from requests_threads import AsyncSession

httpsession = AsyncSession(n=10)

async def threading_http(urls, payload: dict=None, method: str="GET") -> tuple:
    """
    """
    responses = list()
    match method:
        case "GET":
            for u in urls:
                responses.append(await httpsession.get(u))
                logger.info(u)
                logger.info(responses)
        case _:
            logger.error(f"Unrecognized method \"{method}\"")

def main(args: argparse.Namespace, session: Session) -> None:
    """
    """
    wordlist = utils.load_file(args.wordlist_path).splitlines()
    logger.debug(f"Loaded Wordlist with {len(wordlist)} items")

    hosts = utils.load_file(args.network_path).splitlines()
    logger.debug(f"Loaded hosts file with {len(hosts)} items")

    session.set_hosts(hosts)

    httpsession.run(threading_http(hosts, method="GET"))
