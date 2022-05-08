<div align='center'>

  ```
  ██████  ███████ ███    ██ ██████  ███████ ███████ ██    ██  ██████  ██    ██ ███████ 
  ██   ██ ██      ████   ██ ██   ██ ██         ███  ██    ██ ██    ██ ██    ██ ██      
  ██████  █████   ██ ██  ██ ██   ██ █████     ███   ██    ██ ██    ██ ██    ██ ███████ 
  ██   ██ ██      ██  ██ ██ ██   ██ ██       ███     ██  ██  ██    ██ ██    ██      ██ 
  ██   ██ ███████ ██   ████ ██████  ███████ ███████   ████    ██████   ██████  ███████ 

  ```
</div>

## Overview :sparkles:
- A Python-based Discord bot which utilizes the Pycord library and the Ticketmaster API to allow users to find and filter events with ease. 
- To provide the fastest response times for the users of our bot, a cache system is used to reduce latency by saving API results. This works by associating an API URL with its result and a UNIX timestamp. Once the cached result because sufficiently old, the appropriate API is invoked and the cache is updated with the result. This also has the effect of reducing the number of API calls, which is important because the number of Ticketmaster API calls is limited.
- Invite the bot to your server <a href="" target="_blank">here</a> :pushpin:

## Development :computer:
### Requirements
- Python 3.10

### Setup
Install virtual environment
```sh
$ pip install pipenv
```

Run virtual environment
```sh
$ pipenv shell
```

Install dependencies
```sh
$ pipenv install -r requirements.txt
```

Provide environment variables ~ Create .env file
```sh
TICKETMASTER_TOKEN=your_key_here
BOT_TOKEN=your_key_here
```

### Usage
```sh
$ python main.py
```

