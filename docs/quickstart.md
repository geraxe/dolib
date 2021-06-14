# QuickStart

First, start by importing DOLib Client:

```pycon
>>> from dolib import Client
```

And create client object with you Digial Ocean API token.

```pycon
>>> client = Client(token="60c13d47***ed98dd9")
>>> client
<dolib.client.Client at 0x7fdee03c0be0>
```

Get you account information:

```pycon
>>> client.account.get()
Account(floating_ip_limit=3, droplet_limit=25, volume_limit=100, email='yuri@balandin.ru', uuid='4775b5*****************a930', email_verified=True, status='active', status_message='')
```

List available sizes (with limit)

```pycon
>>> client.droplets.sizes()[:5]
[Size(slug='s-1vcpu-1gb', available=True, transfer=1.0, price_monthly=5.0, price_hourly=0.00744, memory=1024, vcpus=1, disk=25, regions=['ams2', 'ams3', 'blr1', 'fra1', 'lon1', 'nyc1', 'nyc2', 'nyc3', 'sfo1', 'sfo3', 'sgp1', 'tor1']),
 Size(slug='s-1vcpu-1gb-amd', available=True, transfer=1.0, price_monthly=6.0, price_hourly=0.00893, memory=1024, vcpus=1, disk=25, regions=['ams3', 'blr1', 'fra1', 'lon1', 'nyc1', 'nyc3', 'sfo3', 'sgp1', 'tor1']),
 Size(slug='s-1vcpu-1gb-intel', available=True, transfer=1.0, price_monthly=6.0, price_hourly=0.00893, memory=1024, vcpus=1, disk=25, regions=['ams3', 'blr1', 'fra1', 'lon1', 'nyc1', 'nyc3', 'sfo3', 'sgp1', 'tor1']),
 Size(slug='s-1vcpu-2gb', available=True, transfer=2.0, price_monthly=10.0, price_hourly=0.01488, memory=2048, vcpus=1, disk=50, regions=['ams2', 'ams3', 'blr1', 'fra1', 'lon1', 'nyc1', 'nyc2', 'nyc3', 'sfo1', 'sfo3', 'sgp1', 'tor1']),
 Size(slug='s-1vcpu-2gb-amd', available=True, transfer=2.0, price_monthly=12.0, price_hourly=0.01786, memory=2048, vcpus=1, disk=50, regions=['ams3', 'blr1', 'fra1', 'lon1', 'nyc1', 'nyc3', 'sfo3', 'sgp1', 'tor1'])]
```

and we can create new droplet for example

for it you need import Droplet model

```pycon
>>> from dolib.models import Droplet
```

then create new Droplet object

```pycon
>>> test_droplet = Droplet(
...   name="test-droplet",
...   region="ams3",
...   size="s-1vcpu-1gb",
...   image="ubuntu-18-04-x64",
... )
>>> test_droplet
Droplet(id=None, name='test-droplet', region='ams3', size='s-1vcpu-1gb', image='ubuntu-18-04-x64', ssh_keys=None, backups=None, ipv6=None, private_networking=None, monitoring=None, vpc_uuid=None, user_data=None, volumes=None, tags=None, memory=None, vcpus=None, disk=None, locked=None, created_at=None, status=None, backup_ids=None, snapshot_ids=None, features=None, size_slug=None, networks=None, kernel=None, next_backup_window=None, volume_ids=None)
```

then create this droplet on Digital Ocean

```pycon
>>> new_droplet = client.droplets.create(test_droplet)
>>> new_droplet
Droplet(id=250429617, name='test-droplet', region=Region(ams3), size=Size(slug='s-1vcpu-1gb', available=True, transfer=1.0, price_monthly=5.0, price_hourly=0.00744, memory=1024, vcpus=1, disk=25, regions=['ams2', 'ams3', 'blr1', 'fra1', 'lon1', 'nyc1', 'nyc2', 'nyc3', 'sfo1', 'sfo3', 'sgp1', 'tor1']), image=Image(id=85779928, name='18.04 (LTS) x64', region=None, url=None, type='base', distribution='Ubuntu', slug='ubuntu-18-04-x64', public=True, regions=['nyc3', 'nyc1', 'sfo1', 'nyc2', 'ams2', 'sgp1', 'lon1', 'ams3', 'fra1', 'tor1', 'sfo2', 'blr1', 'sfo3'], created_at=datetime.datetime(2021, 6, 11, 16, 8, 28, tzinfo=datetime.timezone.utc), min_disk_size=15, size_gigabytes=0.4, description='Ubuntu 18.04 x86 image', tags=[], status='available', error_message=None), ssh_keys=None, backups=None, ipv6=None, private_networking=None, monitoring=None, vpc_uuid=None, user_data=None, volumes=None, tags=[], memory=1024, vcpus=1, disk=25, locked=False, created_at=datetime.datetime(2021, 6, 14, 9, 37, 56, tzinfo=datetime.timezone.utc), status='new', backup_ids=[], snapshot_ids=[], features=[], size_slug='s-1vcpu-1gb', networks=Networks(v4=[], v6=[]), kernel=None, next_backup_window=None, volume_ids=[])
```

you can shutdown this droplet

```pycon
>>> action = client.droplets.shutdown(new_droplet.id)
>>> action
Action(id=1229070666, status='in-progress', type='shutdown', started_at=datetime.datetime(2021, 6, 14, 10, 57, 54, tzinfo=datetime.timezone.utc), completed_at=None, resource_id=250429617, resource_type='droplet', region=Region(ams3), region_slug='ams3')
>>> action.status
'in-progress'
```

check for shutdown complete


```pycon
>>> client.actions.get(action.id)
Action(id=1229070666, status='completed', type='shutdown', started_at=datetime.datetime(2021, 6, 14, 10, 57, 54, tzinfo=datetime.timezone.utc), completed_at=datetime.datetime(2021, 6, 14, 10, 57, 58, tzinfo=datetime.timezone.utc), resource_id=250429617, resource_type='droplet', region=Region(ams3), region_slug='ams3')
```

and finally we can delete this droplet

```pycon
>>> client.droplets.delete(new_droplet)
```


How you can see using DOLib its easy. You have fully featured Digital Ocean console in python context.
