<div align="center">

![banner](https://cdn.technofab.de/images/aiokubemq-banner.png)

# AIOKubeMQ
[![ci](https://img.shields.io/gitlab/pipeline/technofab/aiokubemq/main?label=Pipeline&logo=gitlab)](https://gitlab.com/TECHNOFAB/aiokubemq/-/commits/main)
[![python versions](https://img.shields.io/pypi/pyversions/aiokubemq?label=Versions&logo=python&logoColor=white)](https://pypi.org/project/aiokubemq/)
[![project version](https://img.shields.io/pypi/v/aiokubemq?label=PyPi&logo=pypi&color=%23FFD43B&logoColor=white)](https://pypi.org/project/aiokubemq/)
[![made with python](https://img.shields.io/badge/Made%20with-Python-007ec6.svg?logo=python&logoColor=white)](https://www.python.org/)
[![license](https://img.shields.io/pypi/l/aiokubemq?label=License&logo=internet-archive&logoColor=white)](https://choosealicense.com/licenses/gpl-3.0/)
[![black](https://img.shields.io/badge/Code%20Style-black-000.svg)](https://github.com/psf/black)

</div>

## About
Asynchronous Python KubeMQ Client. \
Basically an optimized reimplementation of https://github.com/kubemq-io/kubemq-Python 
with asyncio and typed methods.

## Note
> This repository is mirrored from [Gitlab][gitlab-repo] to [Github][github-repo].
> Most features like Issues, MRs/PRs etc. are disabled on [Github][github-repo], please use the
> [Gitlab repository][gitlab-repo] for these

## Features
- Modern Pythonic API using asyncio
- Typed
- Pretty lowlevel, wrappers can be built as seen fit

## How to use

```python
import aiokubemq

async def main():
    async with aiokubemq.KubeMQClient("client-id", "host:50000") as client:
        result = await client.ping()
        print(f"We're connected to host '{result.Host}'")
```
> see [the examples folder](examples) for more

[gitlab-repo]: https://gitlab.com/TECHNOFAB/aiokubemq
[github-repo]: https://github.com/TECHNOFAB11/aiokubemq
