DOLib models it is a Pydantic models for all Digital Ocean API objects. Its simple to use this models in python context.

```py
from dolib.models import Droplet

droplet = Droplet(name="dolib-test", region="fra1", size="s-1vcpu-1gb", image="ubuntu-20-04-x64")

new_droplet = client.droplets.create(droplet)
print(new_droplet)
#> Droplet(id=243139176,
#   name='dolib-test',
#   region=Region(fra1),
#   size=Size(s-1vcpu-1gb),
#   image=Image(ubuntu-20-04-x64),
# ...
#   vcpus=1,
#   created_at=datetime.datetime(2021, 4, 25, 9, 52, 58, tzinfo=datetime.timezone.utc),
# ...

print(new_droplet.region.name)
#> Frankfurt 1

print(new_droplet.created_at.date())
#> 2021-04-25

```
