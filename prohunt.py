#!/usr/bin/env python
import requests
import argparse
import socket
import sys
import time
import subprocess
from bs4 import BeautifulSoup

def TOOL_NAME():
    return f"""
    {R}{Y}{G}
             _____           _    _             _   
            |  __ \         | |  | |           | |  
            | |__) | __ ___ | |__| |_   _ _ __ | |_ 
            |  ___/ '__/ _ \|  __  | | | | '_ \| __|
            | |   | | | (_) | |  | | |_| | | | | |_ 
            |_|   |_|  \___/|_|  |_|\__,_|_| |_|\__|@{VERSION}
    
              # Coded By Nikhil Dwivedi - @afloxy
    """

G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

# VERSION of tool
VERSION = "v1.0.0"

# GitHub repository information
GITHUB_REPO = "afloxy/prohunt"
GITHUB_API = "https://api.github.com/repos/afloxy/prohunt/releases/latest"


# Default wordlist file for dorking
DEFAULT_WORDLIST = '''site:{target}
site:*.{target}
site:*.*.{target}
site:{target} -www
site:*.{target} -www
site:*.*.{target} -www
site:{target} -www -public
site:{target} -www -public -internal
site:*.{target} -www -public
site:*.{target} -www -public -internal
site:*.*.{target} -www -public
site:*.*.{target} -www -public -internal
intitle:"Welcome to {target}"
intitle:"Index of /" site:{target}
intext:"403 Forbidden" site:{target}
intext:"404 Not Found" site:{target}
intext:"500 Internal Server Error" site:{target}
intext:"Page cannot be displayed" site:{target}
intext:"Directory Listing" site:{target}
intext:"Directory Listing of" site:{target}
intext:"Directory of" site:{target}
intext:"Index of /" site:{target}
intext:"Parent Directory" site:{target}
intext:"Apache 2 Test Page" site:{target}
intext:"Apache HTTP Server Test Page powered by CentOS" site:{target}
intext:"Welcome to nginx!" site:{target}
intext:"Welcome to LiteSpeed Web Server!" site:{target}
intext:"Microsoft SharePoint" site:{target}
intext:"Powered by WordPress" site:{target}
intext:"Powered by Drupal" site:{target}
intext:"Powered by Joomla!" site:{target}
intext:"Powered by Magento" site:{target}
intext:"Powered by vBulletin" site:{target}
intext:"Powered by phpBB" site:{target}
intext:"Powered by MediaWiki" site:{target}
intext:"Powered by DokuWiki" site:{target}
intext:"Powered by MoinMoin" site:{target}
intext:"Powered by Tiki Wiki CMS Groupware" site:{target}
intext:"Powered by Liferay" site:{target}
intext:"Powered by OpenCart" site:{target}
intext:"Powered by PrestaShop" site:{target}
intext:"Powered by Zen Cart" site:{target}
intext:"Powered by osCommerce" site:{target}
intext:"Powered by Typo3" site:{target}
intext:"Powered by bbPress" site:{target}
intext:"Powered by MyBB" site:{target}
intext:"Powered by Vanilla" site:{target}
intext:"Powered by ExpressionEngine" site:{target}
intext:"Powered by MODX" site:{target}
intext:"Powered by SilverStripe" site:{target}
intext:"Powered by Concrete5" site:{target}
intext:"Powered by dotCMS" site:{target}
intext:"Powered by Ghost" site:{target}
intext:"Powered by Umbraco" site:{target}
intext:"Powered by Xoops" site:{target}
intext:"Powered by Mambo" site:{target}
intext:"Powered by TikiWiki" site:{target}
intext:"Powered by Textpattern" site:{target}
intext:"Powered by GetSimple CMS" site:{target}
intext:"Powered by Plone" site:{target}
intext:"Powered by SilverStripe CMS" site:{target}
intext:"Powered by CMS Made Simple" site:{target}
intext:"Powered by LifeRay" site:{target}
intext:"Powered by PyroCMS" site:{target}
intext:"Powered by ocPortal" site:{target}
intext:"Powered by Croogo" site:{target}
intext:"Powered by BIGACE" site:{target}
intext:"Powered by Contao" site:{target}
intext:"Powered by Sitefinity" site:{target}
intext:"Powered by WebGUI" site:{target}
intext:"Powered by SilverStripe CMS" site:{target}
intext:"Powered by CMS Made Simple" site:{target}
intext:"Powered by ImpressCMS" site:{target}
intext:"Powered by PHP-Fusion" site:{target}
intext:"Powered by DokuWiki" site:{target}
intext:"Powered by MoinMoin" site:{target}
intext:"Powered by Tiki Wiki CMS Groupware" site:{target}
intext:"Powered by Liferay" site:{target}
intext:"Powered by OpenCart" site:{target}
intext:"Powered by PrestaShop" site:{target}
intext:"Powered by Zen Cart" site:{target}
intext:"Powered by osCommerce" site:{target}
intext:"Powered by X-Cart" site:{target}
intext:"Powered by Plone" site:{target}
intext:"Powered by BigCommerce" site:{target}
intext:"Powered by Shopware" site:{target}
intext:"Powered by Shop-Script" site:{target}
intext:"Powered by LiteCart" site:{target}
intext:"Powered by Jigoshop" site:{target}
intext:"Powered by WPeCommerce" site:{target}
intext:"Powered by CubeCart" site:{target}
intext:"Powered by VirtueMart" site:{target}
intext:"Powered by TomatoCart" site:{target}
intext:"Powered by Quick.Cart" site:{target}
intext:"Powered by Arastta" site:{target}
intext:"Powered by AbanteCart" site:{target}
intext:"Powered by CS-Cart" site:{target}'''

# warning
WAR = [
    "The ProHunt tool is provided for educational and ethical purposes only.",
    "Usage of ProHunt for any unauthorized activities is strictly prohibited.",
    "You are solely responsible for your actions and the consequences of using this tool."
]

# Cool animation
ANIMATION_FRAMES = ["/-/", "/^/", "/*/"]


def show_animation():
    for i in range(len(ANIMATION_FRAMES)):
        sys.stdout.write(f"{Y}{ANIMATION_FRAMES[i]}{G} {WAR[i]}\n")
        sys.stdout.flush()
        time.sleep(0.1)


def check_latest_version():
    try:
        response = requests.get(GITHUB_API)
        response.raise_for_status()
        data = response.json()
        latest_version = data["tag_name"]
        return latest_version
    except (requests.RequestException, KeyError):
        return None


def load_wordlist(wordlist):
    if wordlist:
        with open(wordlist, "r") as f:
            dorks = f.read().splitlines()
            return dorks
    else:
        return DEFAULT_WORDLIST.splitlines()


def find_subdomains(domain, wordlist):
    subdomains = []

    dorks = load_wordlist(wordlist)

    for dork in dorks:
        if "{target}" not in dork:
            dork = dork + " site:" + domain
        else:
            dork = dork.replace("{target}", domain)

        url = f"https://www.google.com/search?q={dork}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('a')

        for result in results:
            link = result.get('href')
            if link.startswith('/url?q='):
                subdomain = link.split('/')[2]
                subdomains.append(subdomain)

    return subdomains


def get_ip(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return ip
    except socket.error:
        return None


def scan_ports(subdomains, ports, timeout, verbose):
    open_ports = {}
    total_subdomains = len(subdomains)
    current_subdomain = 0

    for subdomain in subdomains:
        current_subdomain += 1
        open_ports[subdomain] = []
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((subdomain, port))
                if result == 0:
                    open_ports[subdomain].append(port)
                sock.close()
                if verbose:
                    print(f"Port {port} on {subdomain} is open")
            except socket.error:
                pass

        if verbose:
            progress = current_subdomain / total_subdomains * 100
            sys.stdout.write(f"\rScanning subdomains... {current_subdomain}/{total_subdomains} ({progress:.2f}%)")
            sys.stdout.flush()

    return open_ports


def save_results(filename, target, subdomains, open_ports, include_ips):
    with open(filename, 'w') as file:
        file.write(f"{target}\n\n")

        file.write("\n")
        for subdomain in subdomains:
            ip = get_ip(subdomain) if include_ips else None
            if ip:
                file.write(f"{subdomain} ({ip})\n")
            else:
                file.write(f"{subdomain}\n")

        file.write("\n\n")
        for subdomain, ports in open_ports.items():
            if ports:
                file.write(f"{subdomain}: {', '.join(map(str, ports))}\n")
            else:
                file.write(f"{subdomain}: No open ports found\n")


def main(domain, ports, timeout, verbose, output, include_ips, ips_only, wordlist, update):
    if not domain:
        print("Error: Please provide a target domain.")
        return
    if update:
        latest_version = check_latest_version()
        if latest_version and latest_version != VERSION:
            print(f"Updating ProHunt to version {latest_version}...")
            subprocess.call(["git", "pull"])
            print("Update completed.")
        else:
            print(f"ProHunt is already up to date.")

        sys.exit(0)

    print(TOOL_NAME())
    show_animation()
    print("\n")

    latest_version = check_latest_version()
    if latest_version and latest_version != VERSION:
        print(f"\nA new version ({latest_version}) of ProHunt is available on GitHub.")
        print(f"Please update your tool to access the latest features and improvements.")
        print(f"GitHub repository: https://github.com/{GITHUB_REPO}\n")

    subdomains = find_subdomains(domain, wordlist)
    if not subdomains:
        print("No subdomains found for the target domain.")
        return

    open_ports = scan_ports(subdomains, ports, timeout, verbose)

    print(f"\n\nSubdomains of {domain}:")
    for subdomain in subdomains:
        ip = get_ip(subdomain) if include_ips or ips_only else None
        if ips_only:
            if ip:
                print(ip)
        else:
            if ip:
                print(f"{subdomain} ({ip})")
            else:
                print(subdomain)

    print("\nOpen ports:")
    for subdomain, ports in open_ports.items():
        if ports:
            print(f"{subdomain}: {', '.join(map(str, ports))}")
        else:
            print(f"{subdomain}: No open ports found")

    if output:
        save_results(output, domain, subdomains, open_ports, include_ips)
        print(f"\nResults saved to {output}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=WAR)
    parser.add_argument('-d', '--domain', help='Target domain')
    parser.add_argument('-u', '--update', action='store_true', help='Update Prohunt tool')
    parser.add_argument('-p', '--ports', nargs='+', type=int, default=[80, 443],
                        help='TCP ports to scan (space-separated) (default: 80 443)')
    parser.add_argument('-t', '--timeout', type=float, default=2.0,
                        help='Timeout value for port scanning (in seconds) (default: 2.0)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-o', '--output', help='Output file to save the results')
    parser.add_argument('-ip', '--include-ips', action='store_true', help='Include IP addresses along with subdomain names')
    parser.add_argument('-ip-only', '--ips-only', action='store_true', help='Display only the IP addresses of subdomains')
    parser.add_argument('-w', '--wordlist', help='Specify a wordlist file for dorking')
    args = parser.parse_args()

    main(args.domain, args.ports, args.timeout, args.verbose, args.output, args.include_ips, args.ips_only, args.wordlist, args.update)
