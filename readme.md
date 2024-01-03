# New Gen 2FA

This is just a concept I have, no guarantees that it will be 100% secure, but might be secure enough for me to publish this. Written in python.

## Installation
Get Python `winget install python -s winget` or `sudo apt install python3.12` <br>
Download the source <br>
Extract source <br>
Install Requirements `pip install -r  requirements.txt`<br>
Get A Key `python genkey.py`<br>
Register Key At `python auther.py`<br>
Check auth token with `python checker.py`

## Ideology
Both server and client gets the same public and private key, server does it's own auth token generation and checks with the client's auth token if matches.

## Expirations
Auth tokens expire after 10 seconds after generation <br>
Registration Of Public & Private Keys Expire After 10 Minutes