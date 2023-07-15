# ProHunt
ProHunt Is a Subdomain Finder Tool By Google Dorking
Sure! Here's an example of a README file for your ProHunt tool on GitHub:

```
# ProHunt

![ProHunt](prohunt_logo.png)

ProHunt is a powerful tool designed for educational and ethical purposes. It allows you to discover subdomains of a target domain and scan for open ports on those subdomains. Please note that ProHunt should only be used responsibly and with proper authorization.

## Features

- Subdomain discovery using Google dorks
- Port scanning on discovered subdomains
- Optional inclusion of IP addresses for subdomains
- Customizable port list and timeout value
- Verbose mode for detailed output
- Save results to a file

## Usage

```bash
python prohunt.py target [options]
```

- `target`: The target domain to scan for subdomains.

### Options

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

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Examples

- Discover subdomains and scan open ports:

```bash
python prohunt.py example.com
```

- Save results to a file:

```bash
python prohunt.py example.com -o results.txt
```

- Include IP addresses along with subdomain names:

```bash
python prohunt.py example.com -ip
```

- Display only the IP addresses of subdomains:

```bash
python prohunt.py example.com -ip-only
```

## Contributing

Contributions to ProHunt are welcome! If you have any bug reports, feature requests, or suggestions, please open an issue on the GitHub repository.

## Disclaimer

ProHunt is intended for educational and ethical use only. The authors are not responsible for any illegal or unauthorized activities performed with this tool. Use it at your own risk.

## License

ProHunt is licensed under the [MIT License](LICENSE).
```

You can customize and enhance this README file based on your tool's specific features, instructions, and licensing information. Don't forget to replace `prohunt_logo.png` with your tool's logo or an appropriate image.
