### ReFire: Basic firewall and reverse proxy

ReFire is a basic firewall to block http requests from AWS, Azure and GCP ip addresses. This focuses on blocking requests.

Features planned:
- Block requets on specific ports and protocols
- Block ip address ranges of countries
- Block requests from US states or cities
- Block files based on MIME types

Might be reimplemented in GO or Rust

### Running the program

```python

### if you want to intercept requests arriving on port 80. 
### it will socket to port 80

python main.py -p 80
```
