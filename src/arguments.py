
import argparse
from .main import main

def get_parser() -> argparse.Namespace:
    """
    Parses the argparse object
    :returns the arguments object
    """
    parser = argparse.ArgumentParser(description='Slow Web Scanner', epilog="A scanner that runs against an entire network, but slowly and undercover (hopefully).")
    parser.add_argument("-p", "--project", required=True, help="Specify the project path", dest="project_path")
    parser.add_argument("-w", "--wordlist", required=True, help="Specify the path to a wordlist of webpaths", dest="wordlist_path")
    parser.add_argument("-l", "--hosts", required=True, help="Specify the path to a list of hosts/urls/ips to scan", dest="network_path")
    parser.add_argument("-o", "--outFile", default="output", help="Specify the output file name", dest="out_file")
    parser.add_argument("-of", "--outFormat", default="json", help="Specify format of the output (json,csv)", dest="out_format")
    parser.add_argument("-t", "--threads", default=100, type=int, help="Specify the numbers of threads to use (default 100)", dest="threads")
    parser.add_argument("--time", type=int, default=1, help="Specify the to wait between requests (default 1)", dest="time")
    parser.add_argument("--dump", action="store_true", default=False, help="Dump all the responses from the hosts in the project folder", dest="dump")
    parser.set_defaults(func=main)
    return parser.parse_args()
