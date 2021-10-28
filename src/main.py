
import argparse
from loguru import logger
from src.session import Session
import src.utils as utils
import requests
import time
from pprint import pprint
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from requests.packages import urllib3
from src.generator import Generation

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def threading_http(httpsession, urls, payload: dict=None, method: str="GET") -> tuple:
    """
    """
    futures = set()
    match method:
        case "GET":
            for u in urls:
                futures.add(httpsession.get(u, timeout=1, verify=False, allow_redirects=False))
        case _:
            logger.error(f"Unrecognized method \"{method}\"")
    responses = list()
    for future in as_completed(futures):
        try:
            resp = future.result()
        except requests.exceptions.ConnectTimeout:
            #logger.error("Connection timed out.")
            continue
        except requests.exceptions.ReadTimeout:
            #logger.error("Read timed out.")
            continue
        except Exception as e:
            logger.error(e)
            continue

        responses.append({"link": resp.request.url, "response": resp})
    # adding timed_out requests to the final object
    successful = [x["link"] for x in responses]
    responses.extend([{"link": x, "response": None} for x in urls if not x in successful])
    return responses

def main(args: argparse.Namespace, session: Session) -> None:
    """
    """
    wordlist = utils.load_file(args.wordlist_path).splitlines()
    logger.debug(f"Loaded Wordlist with {len(wordlist)} items")

    hosts = utils.load_file(args.network_path).splitlines()
    logger.debug(f"Loaded hosts file with {len(hosts)} items")

    session.set_hosts(hosts)
    hosts = [x["link"] for _,x in session.hosts_status.items()]

    httpsession = FuturesSession(max_workers=args.threads)
    logger.info("Generating wordlist")

    gen_hosts = Generation(session, hosts, wordlist)
    requests_hosts = gen_hosts.get_next_salve()
    while requests_hosts:
        try:
            logger.warning(session)
            time.sleep(args.time)
            responses = threading_http(httpsession, requests_hosts, method="GET")
            session.process_responses(responses, dump=args.dump)
            session.add_request(len(requests_hosts))
            session.save()
            requests_hosts = gen_hosts.get_next_salve()
        except KeyboardInterrupt:
            logger.error("Saving and exiting session.")
            session.save()
            exit(0)
    session.stop()
    session.save()
