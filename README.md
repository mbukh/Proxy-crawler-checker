# Russian Anonymous Proxy Server Scraper

This project aims to gather working anonymous proxy servers in Russia and put down Russian propaganda websites that are closed outside of Russia in the hope of stopping the war Russia started in Ukraine.

The `proxy.py` script is the main component of this project. It has the following command-line options:

### Usage
```bash
proxy.py [-h] [--force_online_crawl] [--minimum_proxy_for_recheck MINIMUM_PROXY_FOR_RECHECK]
                [--clear_queue] [--accumulate_queue] [--country_code COUNTRY_CODE] [--country_name COUNTRY_NAME]
```

### Crawl and parse proxies.

```bash
optional arguments:
  -h, --help            show this help message and exit
  --force_online_crawl  force to crawl online proxy services even if it is not needed
  --minimum_proxy_for_recheck MINIMUM_PROXY_FOR_RECHECK
                        the minimum number of proxies to accumulate before waiting to recheck
  --clear_queue         clear the proxy queue before starting
  --accumulate_queue    save proxy queue history
  --country_code COUNTRY_CODE
                        the country code to filter the proxy servers
  --country_name COUNTRY_NAME
                        the country name to filter the proxy servers
```

## Getting Started

Clone the repository to your local machine.

```bash
git clone https://github.com/mbukh/Russian-Anonymous-Proxy-Server-Scraper.git
```

## Install the required dependencies.

```bash
pip install -r requirements.txt
```

Run the `proxy.py` script with the desired command-line options.

```bash
python proxy.py --force_online_crawl --minimum_proxy_for_recheck 70 --accumulate_queue --country_code ru --country_name russia
```