<h1 align="center">ProxyIP</h1>
<p align="center">
    <em>Base on asyncio、 aiohttp、 sanic</em>
</p>

### ENV

 Build web service base on [sanic](https://github.com/channelcat/sanic).

### Quick Start

#### Install Redis

Proxies will be stored in [Redis](https://redis.io/), a memory-based database that is fast.

#### Clone to local

```bash
git clone https://github.com/zmingGit/ProxyIP
```

#### Dependencies

```bash
pip install -r requirements.txt
```

#### Configuration

You can find the `config.py` file in the ProxyIP folder. You can run the service after updating the redis connection config.

#### RUn

```bash
# run spider
python client.py
# run web service
python server.py
```

### Architecture

This project can be divided into several modules.

`crawler`: fetch proxies, test proxies, stored to redis.

`store`: encapsulate the redis interface, provide connection pool.

`validtor`: verify proxies in redis, remove them if necessary.

`scheduler`: registration time, will dispatch crawler and validtor.

`webapi`: provide web service.

### Example

```python
import random

import requests

# make sure the web service is started

try:
    proxies = requests.get("http://localhost:3289/get/20").json()
    req = requests.get("https://example.com", proxies=random.choice(proxies))
except:
    raise

# or

try:
    proxy = requests.get("http://localhost:3289/pop").json()
    req = requests.get("https://example.com", proxies=proxy)
except:
    raise
```

### License

MIT [©zming](https://github.com/zMingGit/ProxyIP)
