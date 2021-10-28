from loguru import logger
import json
import asyncio
from urllib.parse import urlparse
import src.consts as consts
import os
import aiofiles
import requests

class Out(object):

    def __init__(self, project_path, mode):
        self.project_path = project_path
        self.mode = mode.upper()
        pass

    async def write_csv_format(self, hash: str, text: str) -> None:
        """
        Writes the results in a CSV format
        """
        out_file = os.path.join(self.project_path, "output", hash, "result.csv")

        async with aiofiles.open(out_file, mode='a+') as f:
            await f.write(text)

    def write_response(self, host: str, hash: str, text: str) -> None:
        """
        Writes the text response from the host in the project folder
        """
        parsed_host = urlparse(host)
        file_checked = os.path.split(parsed_host.path)[-1]
        if len(file_checked) == 0:
            file_checked = parsed_host.netloc
        with open(
                os.path.join(
                    self.project_path,
                    "output",
                    hash,
                    "files",
                    file_checked), "w+") as file:
            file.write(text)

    def write_headers(self, hashes) -> None:
        """
        Writes the CSV headers of the results files
        """
        for h in hashes:
            path = os.path.join(self.project_path, "output", h, "result.csv")
            try:
                with open(path, "r") as f:
                    if len(f.read()) > 0:
                        continue
            except:
                pass
            asyncio.run(self.write_csv_format(h, consts.csv_header))


    async def write_json_format(self, hash: str, content: dict) -> None:
        """
        Writes the results in a JSON format
        """
        out_file = os.path.join(self.project_path, "output", hash, "result.json")
        async with aiofiles.open(out_file, mode='a+') as f:
            await f.write(json.dump(content, indent=4))

    def write(self, host_hash: str, http_response: requests.Response()) -> None:
        """
        Writes the informations of the request made to the privilegied output
        """
        match self.mode.upper():
            case 'CSV':
                url = http_response.request.url
                parsed_url = urlparse(http_response.request.url)

                text = f"{url},{parsed_url.path},{http_response.status_code},{len(http_response.text)},{http_response.elapsed},{http_response.request.method}\n"
                """URL,PATH,STATUS_CODE,CONTENT_LENGTH,TIME,METHOD\n"""
                asyncio.run(self.write_csv_format(host_hash, text))
            case "JSON":
                pass
            case _:
                logger.error(f"Unrecognized output {self.mode}")
