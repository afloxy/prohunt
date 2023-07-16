#!/usr/bin/env python
import requests
import argparse
import socket
import sys
import time
from bs4 import BeautifulSoup

def TOOL_NAME():
  print("""%s%s%s
                 _____           _    _             _   
                |  __ \         | |  | |           | |  
                | |__) | __ ___ | |__| |_   _ _ __ | |_ 
                |  ___/ '__/ _ \|  __  | | | | '_ \| __|
                | |   | | | (_) | |  | | |_| | | | | |_ 
                |_|   |_|  \___/|_|  |_|\__,_|_| |_|\__|@v1.0.0

                  # Coded By Nikhil Dwivedi - @afloxy
    """ % (R, G, Y))
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

# Version information
VERSION = "https://api.github.com/repos/afloxy/prohunt/releases/latest"

# warning
WAR = ["The ProHunt tool is provided for educational and ethical purposes only.", "Usage of ProHunt for any unauthorized activities is strictly prohibited.", "You are solely responsible for your actions and the consequences of using this tool."]

# GitHub repository information
GITHUB_REPO = "afloxy/prohunt"
GITHUB_API = f"https://api.github.com/repos/afloxy/prohunt/releases/latest"

# Default wordlist file for dorking
DEFAULT_WORDLIST = "default_wordlist.txt"

# Cool animation
ANIMATION_FRAMES = ["-", "\\", "/"]


def check_latest_version():
    try:
        response = requests.get(GITHUB_API)
        response.raise_for_status()
        data = response.json()
        latest_version = data["tag_name"]
        return latest_version
    except (requests.RequestException, KeyError):
        return None


def show_animation():
    for frame in ANIMATION_FRAMES and for frame in WAR:
        sys.stdout.write(f"\r{frame} {WAR}")
        sys.stdout.flush()
        time.sleep(0.1)


def load_wordlist(wordlist):
    if wordlist:
        with open(wordlist, "r") as f:
            custom_dorks = f.read().splitlines()
            return custom_dorks
    else:
        with open(DEFAULT_WORDLIST, "r") as f:
            default_dorks = f.read().splitlines()
            return default_dorks


def find_subdomains(target, wordlist):
    dorks = load_wordlist(wordlist)
    subdomains = []

    for dork in dorks:
        url = f"https://www.google.com/search?q={dork}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
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
    if update:
        latest_version = check_latest_version()
        if latest_version and latest_version != VERSION:
            print(f"Updating {TOOL_NAME()} to version {latest_version}...")
            subprocess.call(["git", "pull"])
            print("Update completed.")
        else:
            print(f"{TOOL_NAME()} is already up to date.")

        sys.exit(0)

    print(TOOL_NAME())
    print(DESCRIPTION)
    show_animation()
    print("\n")

    latest_version = check_latest_version()
    if latest_version and latest_version != VERSION:
        print(f"\nA new version ({latest_version}) of {TOOL_NAME()} is available on GitHub.")
        print(f"Please update your tool to access the latest features and improvements.")
        print(f"GitHub repository: https://github.com/{GITHUB_REPO}\n")

    subdomains = find_subdomains(domain, wordlist)

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
    parser = argparse.ArgumentParser(description=DESCRIPTION)
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

    main(args.domain, args.ports, args.timeout, args.verbose, args.output, args.include_ips, args.ips_only,
         args.wordlist, args.update)
