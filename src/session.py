
from datetime import datetime
from loguru import logger
import src.consts as consts
import src.utils as utils
import os
import json

class Session(object):

    status = "Running"
    time_start = datetime.now()
    time_stop = None
    requests_made = 0
    hosts_status = dict()
    project_path = None

    def __init__(self, project_path):
        self.project_path = project_path
        self.configure_logger()
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
        
        with open(path, "w+") as file:
            json.dump(session, file, indent=4)

    def set_hosts(self, hosts: list) -> None:
        """
        Add hosts to the internal config
        """
        for h in hosts:
            h = utils.sane_host(h)
            if not h:
                continue
            self.hosts_status.setdefault(h, {
                "link": h,
                "payload_index": 0,
            })

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
        return f"/!\ Session /!\ Status: {self.status}, Requests made: {self.requests_made}, Time started: {self.time_start.strftime('%m/%d/%Y %H:%M:%S')}"
