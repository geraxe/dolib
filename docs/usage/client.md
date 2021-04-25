DOLib provides sync and async clients.

For sync application - sync client
```py
from dolib.client import Client

client = Client(token="you_digital_ocean_token")

for size in client.droplets.sizes()[:5]:
    print(size.slug)
#> s-1vcpu-1gb
#> s-1vcpu-1gb-amd
#> s-1vcpu-1gb-intel
#> s-1vcpu-2gb
#> s-1vcpu-2gb-amd
```

Async client for async application
```py
from dolib.client import AsyncClient

async_client = AsyncClient(token="you_digital_ocean_token")

droplet = (await async_client.droplets.all())[0]
print(droplet)
#> Droplet(id=243139176,
#   name='dolib-test',
#   region=Region(fra1),
#   size=Size(s-1vcpu-1gb),
#   image=Image(ubuntu-20-04-x64),
# ...

```
