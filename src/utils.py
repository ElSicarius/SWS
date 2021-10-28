
from loguru import logger
import os
import re
from urllib.parse import urlparse

def load_file(path: str) -> str:
    """
    Loads a file with the context manager and reads it.
    """
    if not os.path.exists(path):
        logger.error(f"File \"{path}\" does not exists. Exiting !")
        exit()
    logger.info(f"Loading file \"{path}\".")
    with open(path, "r") as f:
        content = f.read()
    return content

def sane_host(host: str) -> str:
    """
    Append the protocal to a given host if needed
    """
    host = host.strip()
    type = None

    if not host.startswith("http"):
        if re.findall(r"^[\d]+.[\d]+.[\d]+.[\d]+$", host):
            host = f"http://{host}"
        elif re.findall(r"^[A-Za-z_\-\.]+\.[\w]+$", host):
            host = f"https://{host}"
        else:
            logger.error(f"Provided host is weird, Skipping this one ! (not an URI or IP), host: {host}")
            return None
    if not host.endswith("/") and not len(urlparse(host).path) > 0:
        host += "/"
    return host
