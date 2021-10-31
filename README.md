# SWS
Slow Web Scanner, or in other words, a tool that helps you spread a wordlist across hundreds of websites, without requesting one host more than 1 time per second (default setting).

# Why the F* ?
Good question.
First answer: do you know WAFs ?
Second answer: you might want to stay undercover across a large number of assets
third answer: Because, why not

# Basic usage

## hosts list
```bash
sicarius@komputer:/mnt/hgfs/projets/SWS$ cat tests/hosts_tests
elsicarius.fr
192.168.1.1
https://google.fr
```

## command line

```bash
python3.10 sws.py -p tests/test_project/ -w files/dirbuster-top1000.txt -l tests/targets_tests --time 1 -of csv --dump
```
- -p is your project path. You don't need to create the directory. In this directory will be placed all the output file of the program
- -w is your wordlist
- -l is your targets file
- --time sets the waiting time between requests
- -of = output format
- --dump = dump all the responses to the corresponding filename

## Results

Once finished, the project folder will look like this:

```
tests/test_project/
├── logs.log
├── output
│ ├── 3535f7ff849d27b3899acbccd35b7aee
│ │ ├── files
│ │ │ ├── 1
│ │ │ ├── 1014943
│ │ │ ├── 3
│ │ │ ├── .....
│ │ │ └── xmlrpc.php
│ │ └── result.csv
│ └── a6cc2eeab03d17b6f5832374a82c5e1d
│     ├── files
│     │ ├── ....
│     └── result.csv
└── session.json

7 directories, xx files
```

- You have all the logs in logs.log
- The session.json is used to store and retrieve the urls's hashs and some extra infos
- for each valid host, we're creating a dir based on the md5 of the name of the host inside the output directory, then we store the result file (CSV or JSON) in the corresponding dir.
- If the --dump option is added, we'll dump all the files in the <project_path>/output/<hash>/files directory.


# Usage

```
usage: sws.py [-h] -p PROJECT_PATH -w WORDLIST_PATH -l NETWORK_PATH [-o OUT_FILE] [-of OUT_FORMAT] [-t THREADS] [--time TIME] [--dump]

Slow Web Scanner

options:
  -h, --help            show this help message and exit
  -p PROJECT_PATH, --project PROJECT_PATH
                        Specify the project path
  -w WORDLIST_PATH, --wordlist WORDLIST_PATH
                        Specify the path to a wordlist of webpaths
  -l NETWORK_PATH, --hosts NETWORK_PATH
                        Specify the path to a list of hosts/urls/ips to scan
  -of OUT_FORMAT, --outFormat OUT_FORMAT
                        Specify format of the output (json,csv)
  -t THREADS, --threads THREADS
                        Specify the numbers of threads to use (default 100)
  --time TIME           Specify the to wait between requests (default 1)
  --dump                Dump all the responses from the hosts in the project folder

A scanner that runs against an entire network, but slowly and undercover (hopefully).
```

# Todo

- Format session messages
- Add json output
- filter output requests, do not output everything
