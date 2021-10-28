
from datetime import datetime
from loguru import logger
import src.consts as consts
import src.utils as utils
from urllib.parse import urlparse, urlunparse
from src.output import Out
import os
import json
import hashlib

class Session(object):

    status = "Running"
    time_start = datetime.now()
    time_stop = None
    requests_made = 0
    hosts_status = dict()
    project_path = None
    payload_index = 0
    wordlist_name = str()

    def __init__(self, args):
        self.project_path = args.project_path
        self.configure_logger()
        self.out = Out(self.project_path, args.out_format)
        self.out_format = args.out_format.upper()
        self.wordlist_name = os.path.split(args.wordlist_path)[-1]
        try:
            os.mkdir(os.path.join(self.project_path,"output"))
        except FileExistsError:
            pass

    def configure_logger(self):
        """
        Configure loguru
        """
        logger.add(
            os.path.join(self.project_path,"logs.log"),
            #compression="zip"
            )

    def save(self) -> None:
        """
        """
        self.write_session(os.path.join(self.project_path,"session.json"))

    def write_session(self, path: str) -> None:
        """
        Write the session file to the project folder
        """
        session = self.hosts_status
        session["payload_index"] = self.payload_index
        session["wordlist_name"] = self.wordlist_name
        with open(path, "w+") as file:
            json.dump(session, file, indent=4)

    def load_session(self) -> None:
        """
        Write the session file to the project folder
        """
        try:
            with open(os.path.join(self.project_path,"session.json"), "r") as file:
                content = json.loads(file.read())
                # if we're trying a different wordlist, just return
                if self.wordlist_name != content["wordlist_name"]:
                    return
                self.payload_index = content["payload_index"]
                del content["payload_index"]
                del content["wordlist_name"]
                self.hosts_status = content
                # session resumed
                logger.success(f"Resuming previous session, database {self.wordlist_name}, payload index {self.payload_index}")

        except FileNotFoundError:
            pass

    def set_hosts(self, hosts: list) -> None:
        """
        Add hosts to the internal config
        """
        for h in hosts:
            h = utils.sane_host(h)
            if not h:
                continue
            hash = hashlib.md5(h.encode()).hexdigest()
            self.hosts_status.setdefault(h, {
                "link": h,
                "hash": hash
            })
            try:
                os.mkdir(os.path.join(
                            self.project_path,
                            "output",
                            hash))
            except FileExistsError:
                pass

            try:
                os.mkdir(os.path.join(
                            self.project_path,
                            "output",
                            hash,
                            "files"))
            except FileExistsError:
                pass
        if self.out_format == "CSV":
            self.out.write_headers([x["hash"] for _,x in self.hosts_status.items()])

    def process_responses(self, responses: list, dump: bool=False) -> None:
        """
        Registers the useful responses in the project folder
        """
        for e in responses:

            if e["response"] is None:
                logger.error(f'Error while requesting: {e["link"]}')
                continue
            parsed_host = urlparse(e["link"])
            real_host = urlunparse(parsed_host._replace(path="/"))
            if dump:
                self.out.write_response(
                            e["link"],
                            self.hosts_status[real_host]["hash"],
                            e["response"].text)

            self.out.write(self.hosts_status[real_host]["hash"], e["response"])

    def stop(self) -> None:
        """
        Define the time were we ended the program
        """
        self.time_stop = datetime.now()
        self.status = "Off"

    def add_request(self, count: int=1) -> None:
        """
        Add x requests to the counter
        """
        self.requests_made += int(count)

    def __str__(self):
        return f"/!\ Session /!\ Status: {self.status}, Requests made: {self.requests_made}, Started @: {self.time_start.strftime('%m/%d/%Y %H:%M:%S')}"
