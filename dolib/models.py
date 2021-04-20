import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr


class Region(BaseModel):
    name: str
    slug: str
    sizes: List[str]
    available: bool
    features: List[str]

    def __repr__(self) -> str:
        return "Region({slug})".format(slug=self.slug)


class Network(BaseModel):
    ip_address: str
    netmask: str
    gateway: str
    type: str

    def __repr__(self) -> str:
        return "Network({ip}/{netmask} [{type}])".format(
            ip=self.ip_address,
            netmask=self.netmask,
            type=self.type,
        )


class Account(BaseModel):
    floating_ip_limit: int
    droplet_limit: int
    volume_limit: int
    email: EmailStr
    uuid: str
    email_verified: bool
    status: str
    status_message: str


class Action(BaseModel):
    id: int
    status: str
    type: str
    started_at: datetime
    completed_at: Optional[datetime]
    resource_id: Optional[int]
    resource_type: str
    region: Optional[Region]
    region_slug: Optional[str]


class Balance(BaseModel):
    month_to_date_balance: Decimal
    account_balance: Decimal
    month_to_date_usage: Decimal
    generated_at: datetime


class BillingHistory(BaseModel):
    description: str
    amount: str
    invoice_id: Optional[str]
    invoice_uuid: Optional[uuid.UUID]
    date: datetime
    type: str


class CDNEndpoint(BaseModel):
    id: Optional[uuid.UUID]
    origin: str
    endpoint: Optional[str]
    created_at: Optional[datetime]
    ttl: Optional[int]
    certificate_id: Optional[str]
    custom_domain: Optional[str]


class Certificate(BaseModel):
    id: Optional[uuid.UUID]
    name: str
    private_key: Optional[str]
    leaf_certificate: Optional[str]
    certificate_chain: Optional[str]
    not_after: Optional[datetime]
    sha1_fingerprint: Optional[str]
    created_at: Optional[datetime]
    dns_names: List[str]
    state: Optional[str]
    type: Optional[str]


class DBCluster(BaseModel):
    class Connection(BaseModel):
        uri: str
        database: str
        host: str
        port: int
        user: str
        password: str
        ssl: bool

    class User(BaseModel):
        name: str
        role: Optional[str]
        password: Optional[str]
        mysql_settings: Optional[dict]

    class DB(BaseModel):
        name: str

    id: Optional[uuid.UUID]

    # required params
    name: str
    engine: str
    size: str
    region: str
    num_nodes: int

    # optional params
    version: Optional[str]
    connection: Optional[Connection]
    private_connection: Optional[Connection]
    users: Optional[List[User]]
    db_names: Optional[List[str]]
    status: Optional[str]
    maintenance_window: Optional[dict]
    created_at: Optional[datetime]
    tags: Optional[List[str]]
    private_network_uuid: Optional[uuid.UUID]


class DBReplica(BaseModel):
    name: str
    size: Optional[str]
    connection: Optional[DBCluster.Connection]
    private_connection: Optional[DBCluster.Connection]
    region: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    tags: Optional[List[str]]
    private_network_uuid: Optional[uuid.UUID]


class Invoice(BaseModel):
    class Item(BaseModel):
        product: str
        resource_uuid: Optional[uuid.UUID]
        resource_id: Optional[str]
        group_description: Optional[str]
        description: str
        amount: Decimal
        duration: str
        duration_unit: str
        start_time: datetime
        end_time: datetime
        project_name: Optional[str]

    invoice_uuid: Optional[uuid.UUID]
    amount: Optional[Decimal]
    invoice_period: Optional[str]
    billing_period: Optional[str]
    updated_at: Optional[datetime]
    invoice_items: Optional[List[Item]]


class Image(BaseModel):
    id: Optional[int]
    name: str
    region: Optional[str]
    url: Optional[str]
    type: Optional[str]
    distribution: Optional[str]
    slug: Optional[str]
    public: Optional[bool]
    regions: Optional[List[str]]
    created_at: Optional[datetime]
    min_disk_size: Optional[int]
    size_gigabytes: Optional[float]
    description: Optional[str]
    tags: Optional[List[str]]
    status: Optional[str]
    error_message: Optional[str]


class Domain(BaseModel):
    class Record(BaseModel):
        id: Optional[int]
        type: str
        name: Optional[str]
        data: Optional[str]
        priority: Optional[int]
        port: Optional[int]
        ttl: Optional[int]
        weight: Optional[int]
        flags: Optional[int]
        tag: Optional[str]

    name: str
    ttl: Optional[int]
    zone_file: Optional[str]


class Droplet(BaseModel):
    class Size(BaseModel):
        slug: str
        available: bool
        transfer: float
        price_monthly: float
        price_hourly: float
        memory: int
        vcpus: int
        disk: int
        regions: List[str]

    class Kernel(BaseModel):
        id: int
        name: str
        version: str

    class Networks(BaseModel):
        v4: List[Network]
        v6: List[Network]

    class BackupWindow(BaseModel):
        start: datetime
        end: datetime

    id: Optional[int]

    # required params
    name: str
    region: Union[str, Region]
    size: Union[str, Size]
    image: Union[int, str, Image]

    # optional params
    ssh_keys: Optional[List[Union[int, str]]]
    backups: Optional[bool]
    ipv6: Optional[bool]
    private_networking: Optional[bool]
    monitoring: Optional[bool]
    vpc_uuid: Optional[uuid.UUID]
    user_data: Optional[str]
    volumes: Optional[List[str]]
    tags: Optional[List[str]]

    memory: Optional[int]
    vcpus: Optional[int]
    disk: Optional[int]
    locked: Optional[bool]
    created_at: Optional[datetime]
    status: Optional[str]
    backup_ids: Optional[List[int]]
    snapshot_ids: Optional[List[int]]
    features: Optional[List[str]]
    size_slug: Optional[str]
    networks: Optional[Networks]
    kernel: Optional[Kernel]
    next_backup_window: Optional[BackupWindow]
    volume_ids: Optional[List[str]]


class FirewallTargets(BaseModel):
    addresses: Optional[List[str]]
    droplet_ids: Optional[List[int]]
    load_balancer_uids: Optional[List[str]]
    tags: Optional[List[str]]


class Firewall(BaseModel):
    class InboundRule(BaseModel):
        protocol: str
        ports: str
        sources: FirewallTargets

    class OutboundRule(BaseModel):
        protocol: str
        ports: str
        destinations: FirewallTargets

    class Changes(BaseModel):
        droplet_id: int
        removing: str
        status: str

    id: Optional[uuid.UUID]
    status: Optional[str]
    created_at: Optional[datetime]
    pending_changes: Optional[List[Changes]]
    name: str
    inbound_rules: Optional[List[InboundRule]]
    outbound_rules: Optional[List[OutboundRule]]
    droplet_ids: Optional[List[int]]
    tags: Optional[List[str]]


class FloatingIP(BaseModel):
    ip: Optional[str]
    region: Optional[Union[str, Region]]
    droplet: Optional[Droplet]


class K8SCluster(BaseModel):
    class Pool(BaseModel):
        class Labels(BaseModel):
            tier: str
            service: str

        class Node(BaseModel):
            class Status(BaseModel):
                state: str

            id: Optional[uuid.UUID]
            name: str
            status: Status
            created_at: datetime
            updated_at: datetime

        id: Optional[uuid.UUID]

        size: str
        name: str
        count: int

        tags: Optional[List[str]]
        labels: Optional[Labels]
        auto_scale: Optional[bool]
        min_nodes: Optional[int]
        max_nodes: Optional[int]
        nodes: Optional[List[Node]]

    id: Optional[str]

    # required params
    name: str
    region: str
    version: str
    node_pools: List[Pool]

    # optional params
    endpoint: Optional[str]
    auto_upgrade: Optional[bool]
    ipv4: Optional[str]
    cluster_subnet: Optional[str]
    service_subnet: Optional[str]
    vpc_uuid: Optional[uuid.UUID]
    tags: Optional[List[str]]
    maintenance_policy: Optional[dict]
    created_at: Optional[str]
    updated_at: Optional[str]


class LoadBalancer(BaseModel):
    class ForwardingRule(BaseModel):
        # required params
        entry_protocol: str
        entry_port: int
        target_protocol: str
        target_port: int

        # optional params
        certificate_id: Optional[str]
        tls_passthrough: Optional[bool]

    class HealthCheck(BaseModel):
        # required params
        protocol: str
        port: int

        # optional params
        path: Optional[str]
        check_interval_seconds: Optional[int]
        response_timeout_seconds: Optional[int]
        unhealthy_threshold: Optional[int]
        healthy_threshold: Optional[int]

    class StickySessions(BaseModel):
        type: str
        cookie_name: Optional[str]
        cookie_ttl_seconds: Optional[int]

    id: Optional[str]

    # required params
    name: str
    region: Union[str, Region]
    forwarding_rules: List[ForwardingRule]

    # optional params
    size: Optional[str]
    ip: Optional[str]
    algorithm: Optional[str]
    status: Optional[str]
    health_check: Optional[HealthCheck]
    sticky_sessions: Optional[StickySessions]
    tag: Optional[str]
    droplet_ids: Optional[List[int]]
    redirect_http_to_https: Optional[bool]
    enable_proxy_protocol: Optional[bool]
    enable_backend_keepalive: Optional[bool]
    vpc_uuid: Optional[str]
    created_at: Optional[datetime]


class Project(BaseModel):
    class Resource(BaseModel):
        class Links(BaseModel):
            self: str

        urn: str
        assigned_at: Optional[datetime]
        links: Optional[Links]
        status: Optional[str]

    id: Optional[str]

    # required params
    name: str
    purpose: str

    # optional params
    owner_uuid: Optional[str]
    owner_id: Optional[int]
    description: Optional[str]
    environment: Optional[str]
    is_default: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Registry(BaseModel):
    class Repository(BaseModel):
        class Tag(BaseModel):
            registry_name: str
            repository: str
            tag: str
            manifest_digest: str
            compressed_size_bytes: int
            size_bytes: int
            updated_at: datetime

        registry_name: str
        name: str
        latest_tag: Tag
        tag_count: int

    class GarbageCollection(BaseModel):
        uuid: str
        registry_name: str
        blobs_deleted: int
        status: str
        freed_bytes: int
        created_at: datetime
        updated_at: datetime

    name: str
    created_at: Optional[datetime]


class Snapshot(BaseModel):
    id: Optional[str]
    name: str
    created_at: Optional[datetime]
    regions: Optional[List[str]]
    resource_id: Optional[str]
    resource_type: Optional[str]
    min_disk_size: Optional[int]
    size_gigabytes: Optional[float]
    tags: Optional[List[str]]


class SSHKey(BaseModel):
    id: Optional[int]
    fingerprint: Optional[str]
    public_key: str
    name: str


class Tag(BaseModel):
    class Resource(BaseModel):
        resource_id: str
        resource_type: str

    class TagStat(BaseModel):
        class Count(BaseModel):
            count: int
            last_tagged_uri: Optional[str]

        count: int
        last_tagged_uri: Optional[str]
        droplets: Count
        images: Count
        volumes: Count
        volume_snapshots: Count
        databases: Count

    name: str
    resources: Optional[TagStat]


class Volume(BaseModel):
    id: Optional[str]
    region: Union[str, Region]
    droplet_ids: Optional[List[int]]
    name: str
    description: Optional[str]
    size_gigabytes: int
    created_at: Optional[datetime]
    filesystem_type: Optional[str]
    filesystem_label: Optional[str]
    tags: Optional[List[str]]


class VPC(BaseModel):
    class Member(BaseModel):
        name: str
        urn: str
        created_at: datetime

    id: Optional[str]
    urn: Optional[str]
    name: str
    region: str
    ip_range: Optional[str]
    description: Optional[str]
    default: Optional[bool]
    created_at: Optional[datetime]
