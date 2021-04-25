from dolib.client import Client

client = Client(token="60c13d47***ed98dd9")

droplet = client.droplets.all()[0]

print(droplet)
# > Droplet(id=120794777, name='dolib-test', region=Region(fra1),
# >   size=Size(s-2vcpu-4gb), image=Image('18.04 x64'), ....)

volume = client.volumes.get("53cf7120-9d5b-11ea-aed1-0a58ac14d008")

client.volumes.attach(volume, droplet_id=droplet.id)
