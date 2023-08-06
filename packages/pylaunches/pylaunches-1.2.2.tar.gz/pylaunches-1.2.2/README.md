# PyLaunches

_A python packages to get information form upcoming space launches._

## Install

```bash
python3 -m pip install pylaunches
```

### Example usage

```python
"""Example usage of pylaunches."""
import asyncio

from pylaunches import PyLaunches, PyLaunchesException


async def example():
    """Example usage of pylaunches."""
    async with PyLaunches() as api:
        try:
            launches = await api.upcoming_launches()
            for launch in launches:
                print(launch.name)
        except PyLaunchesException:
            print(":(")


asyncio.get_event_loop().run_until_complete(example())

```

This package is using the [Launch Library 2 API][launchlibrary] to get the information.

[launchlibrary]: https://thespacedevs.com/llapi