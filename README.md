<h1 align="center">ProHunt</h1>
<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Install</a> •
  <a href="#usage">Usage</a> •
  <a href="#options">Options</a> •
  <a href="#recommendedpythonversion">Python version</a> •
  <a href="Examples">Examples</a>
</p>

ProHunt Is a Subdomain Finder Tool using Google Dorking and it designed for educational and ethical purposes. It allows you to discover subdomains of a target domain and scan for open ports on those subdomains. Please note that ProHunt should only be used responsibly and with proper authorization.

## Features

- Subdomain discovery using Google dorks
- Port scanning on discovered subdomains
- Optional inclusion of IP addresses for subdomains
- Customizable port list and timeout value
- Verbose mode for detailed output
- Save results to a file

## Usage

```bash
prohunt -d target [options]
```

- target: The target domain to scan for subdomains.

### Options

- `-d`, `--domain`: domain to find subdomains for.
- `-u`, `--update`: Update ProHunt to the latest version.
- `-p`, `--ports`: Specify the TCP ports to scan. Default: 80 and 443.
- `-t`, `--timeout`: Set the timeout value for port scanning (in seconds). Default: 2.0.
- `-v`, `--verbose`: Enable verbose mode.
- `-o`, `--output`: Save the results to a file.
- `-ip`, `--include-ips`: Include IP addresses along with subdomain names.
- `-ip-only`, `--ips-only`: Display only the IP addresses of subdomains.
- `-w`, `--wordlist`: Specify a wordlist file for dorking.

## Installation

1. Clone the ProHunt repository:

```bash
git clone https://github.com/afloxy/prohunt.git
```
2. Open the ProHunt repository:

```bash
cd prohunt
```

3. Install the required dependencies:

```bash
sudo python setup.py 
```
## Recommended Python Version:

ProHunt currently supports **Python 3**.

* The recommended version for Python 3 is **3.4.x**
  
## Examples

- Discover subdomains:

```bash
prohunt -d example.com
```
- Discover subdomains with open ports:

```bash
prohunt -d example.com -p 80 443
```
  
- Save results to a file:

```bash
prohunt -d example.com -o results.txt
```

- Include IP addresses along with subdomain names:

```bash
prohunt -d example.com -ip
```

- Display only the IP addresses of subdomains:

```bash
prohunt -d example.com -ip-only
```
- You can add your own wordlist
  
```bash
prohunt -d example.com -w /path/to/wordlist.txt
```

## Contributing

Contributions to ProHunt are welcome! If you have any bug reports, feature requests, or suggestions, please open an issue on the GitHub repository.

## Disclaimer

ProHunt is intended for educational and ethical use only. The authors are not responsible for any illegal or unauthorized activities performed with this tool. Use it at your own risk.

