import os
import requests

# Last Updated on 26/4/2024 - Cherry

url = 'https://raw.githubusercontent.com/moziIIa/blocker/main/domains.txt'

hosts_file_path = '/etc/hosts'

def fetch_blocklist(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch blocklist from {url}!")
            exit(1)
    except Exception as e:
        print(f"An error occurred while fetching the blocklist: {str(e)}.")
        exit(1)

def is_domain_blocked(domain):
    with open(hosts_file_path, 'r', encoding='utf-8') as hosts_file:
        for line in hosts_file:
            if domain in line:
                return True
    return False

def block_websites(blocklist):
    try:
        print("Blocking websites:")
        with open(hosts_file_path, 'a', encoding='utf-8') as hosts_file:
            hosts_file.write('\n# Blocked websites\n')
            for website in blocklist.split('\n'):
                if website.strip() and not is_domain_blocked(website.strip()):
                    blocked_website = website.strip()
                    hosts_file.write(f'127.0.0.1 {blocked_website}\n')
                    print(f"{blocked_website} has been blocked.")
        print("\nSuccessfully blocked websites!")
    except Exception as e:
        print(f"An error occurred while blocking websites: {str(e)}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run this script as root (sudo).")
        exit(1)
    
    blocklist = fetch_blocklist(url)
    block_websites(blocklist)

    input("Press Enter to exit...")
