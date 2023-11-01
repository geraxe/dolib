import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
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
    netmask: Union[str, int]
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
    completed_at: Optional[datetime] = None
    resource_id: Optional[int] = None
    resource_type: str
    region: Optional[Region] = None
    region_slug: Optional[str] = None


class Balance(BaseModel):
    month_to_date_balance: Decimal
    account_balance: Decimal
    month_to_date_usage: Decimal
    generated_at: datetime


class BillingHistory(BaseModel):
    description: str
    amount: str
    invoice_id: Optional[str] = None
    invoice_uuid: Optional[uuid.UUID] = None
    date: datetime
    type: str


class CDNEndpoint(BaseModel):
    id: Optional[uuid.UUID] = None
    origin: str
    endpoint: Optional[str] = None
    created_at: Optional[datetime] = None
    ttl: Optional[int] = None
    certificate_id: Optional[str] = None
    custom_domain: Optional[str] = None


class Certificate(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    type: str
    private_key: Optional[str] = None
    leaf_certificate: Optional[str] = None
    certificate_chain: Optional[str] = None
    not_after: Optional[datetime] = None
    sha1_fingerprint: Optional[str] = None
    created_at: Optional[datetime] = None
    dns_names: Optional[List[str]] = None
    state: Optional[str] = None


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
        role: Optional[str] = None
        password: Optional[str] = None
        mysql_settings: Optional[dict] = None

    class DB(BaseModel):
        name: str

    id: Optional[uuid.UUID] = None

    # required params
    name: str
    engine: str
    size: str
    region: str
    num_nodes: int

    # optional params
    version: Optional[str] = None
    connection: Optional[Connection] = None
    private_connection: Optional[Connection] = None
    users: Optional[List[User]] = None
    db_names: Optional[List[str]] = None
    status: Optional[str] = None
    maintenance_window: Optional[dict] = None
    created_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    private_network_uuid: Optional[uuid.UUID] = None


class DBReplica(BaseModel):
    name: str
    size: Optional[str] = None
    connection: Optional[DBCluster.Connection] = None
    private_connection: Optional[DBCluster.Connection] = None
    region: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    private_network_uuid: Optional[uuid.UUID] = None


class Invoice(BaseModel):
    class Item(BaseModel):
        product: str
        resource_uuid: Optional[uuid.UUID] = None
        resource_id: Optional[str] = None
        group_description: Optional[str] = None
        description: str
        amount: Decimal
        duration: str
        duration_unit: str
        start_time: datetime
        end_time: datetime
        project_name: Optional[str] = None

    invoice_uuid: Optional[uuid.UUID] = None
    amount: Optional[Decimal] = None
    invoice_period: Optional[str] = None
    billing_period: Optional[str] = None
    updated_at: Optional[datetime] = None
    invoice_items: Optional[List[Item]] = None


class Image(BaseModel):
    class Distribution(Enum):
        ALMALINUX = "AlmaLinux"
        ARCH_LINUX = "Arch Linux"
        CENTOS = "CentOS"
        COREOS = "CoreOS"
        DEBIAN = "Debian"
        FEDORA = "Fedora"
        FEDORA_ATOMIC = "Fedora Atomic"
        FREEBSD = "FreeBSD"
        GENTOO = "Gentoo"
        OPENSUSE = "openSUSE"
        RANCHEROS = "RancherOS"
        ROCKY_LINUX = "Rocky Linux"
        UBUNTU = "Ubuntu"
        UNKNOWN = "Unknown"

    class Type(Enum):
        APPLICATION = "application"
        BASE = "base"
        SNAPSHOT = "snapshot"
        BACKUP = "backup"
        CUSTOM = "custom"
        ADMIN = "admin"

    id: Optional[int] = None
    name: str
    region: Optional[str] = None
    url: Optional[str] = None
    type: Optional[Type] = None
    distribution: Optional[Distribution] = None
    slug: Optional[str] = None
    public: Optional[bool] = None
    regions: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    min_disk_size: Optional[int] = None
    size_gigabytes: Optional[float] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    error_message: Optional[str] = None


class Domain(BaseModel):
    class Record(BaseModel):
        id: Optional[int] = None
        type: str
        name: Optional[str] = None
        data: Optional[str] = None
        priority: Optional[int] = None
        port: Optional[int] = None
        ttl: Optional[int] = None
        weight: Optional[int] = None
        flags: Optional[int] = None
        tag: Optional[str] = None

    name: str
    ttl: Optional[int] = None
    zone_file: Optional[str] = None


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

    id: Optional[int] = None

    # required params
    name: str
    region: Union[str, Region]
    size: Union[str, Size]
    image: Union[int, str, Image]

    # optional params
    ssh_keys: Optional[List[Union[int, str]]] = None
    backups: Optional[bool] = None
    ipv6: Optional[bool] = None
    private_networking: Optional[bool] = None
    monitoring: Optional[bool] = None
    vpc_uuid: Optional[uuid.UUID] = None
    user_data: Optional[str] = None
    volumes: Optional[List[str]] = None
    tags: Optional[List[str]] = None

    memory: Optional[int] = None
    vcpus: Optional[int] = None
    disk: Optional[int] = None
    locked: Optional[bool] = None
    created_at: Optional[datetime] = None
    status: Optional[str] = None
    backup_ids: Optional[List[int]] = None
    snapshot_ids: Optional[List[int]] = None
    features: Optional[List[str]] = None
    size_slug: Optional[str] = None
    networks: Optional[Networks] = None
    kernel: Optional[Kernel] = None
    next_backup_window: Optional[BackupWindow] = None
    volume_ids: Optional[List[str]] = None


class FirewallTargets(BaseModel):
    addresses: Optional[List[str]] = None
    droplet_ids: Optional[List[int]] = None
    load_balancer_uids: Optional[List[str]] = None
    tags: Optional[List[str]] = None


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

    id: Optional[uuid.UUID] = None

    # required params
    name: str

    # optional params
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    pending_changes: Optional[List[Changes]] = None
    inbound_rules: Optional[List[InboundRule]] = None
    outbound_rules: Optional[List[OutboundRule]] = None
    droplet_ids: Optional[List[int]] = None
    tags: Optional[List[str]] = None


class FloatingIP(BaseModel):
    ip: Optional[str] = None
    region: Optional[Union[str, Region]] = None
    droplet: Optional[Droplet] = None


class K8SCluster(BaseModel):
    class Pool(BaseModel):
        class Labels(BaseModel):
            tier: str
            service: str

        class Node(BaseModel):
            class Status(BaseModel):
                state: str

            id: Optional[uuid.UUID] = None
            name: str
            status: Status
            created_at: datetime
            updated_at: datetime

        id: Optional[uuid.UUID] = None

        size: str
        name: str
        count: int

        tags: Optional[List[str]] = None
        labels: Optional[Labels] = None
        auto_scale: Optional[bool] = None
        min_nodes: Optional[int] = None
        max_nodes: Optional[int] = None
        nodes: Optional[List[Node]] = None

    id: Optional[str] = None

    # required params
    name: str
    region: str
    version: str
    node_pools: List[Pool]

    # optional params
    endpoint: Optional[str] = None
    auto_upgrade: Optional[bool] = None
    ipv4: Optional[str] = None
    cluster_subnet: Optional[str] = None
    service_subnet: Optional[str] = None
    vpc_uuid: Optional[uuid.UUID] = None
    tags: Optional[List[str]] = None
    maintenance_policy: Optional[dict] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class LoadBalancer(BaseModel):
    class ForwardingRule(BaseModel):
        # required params
        entry_protocol: str
        entry_port: int
        target_protocol: str
        target_port: int

        # optional params
        certificate_id: Optional[str] = None
        tls_passthrough: Optional[bool] = None

    class HealthCheck(BaseModel):
        # required params
        protocol: str
        port: int

        # optional params
        path: Optional[str] = None
        check_interval_seconds: Optional[int] = None
        response_timeout_seconds: Optional[int] = None
        unhealthy_threshold: Optional[int] = None
        healthy_threshold: Optional[int] = None

    class StickySessions(BaseModel):
        type: str
        cookie_name: Optional[str] = None
        cookie_ttl_seconds: Optional[int] = None

    id: Optional[str] = None

    # required params
    name: str
    region: Union[str, Region]
    forwarding_rules: List[ForwardingRule]

    # optional params
    size: Optional[str] = None
    ip: Optional[str] = None
    algorithm: Optional[str] = None
    status: Optional[str] = None
    health_check: Optional[HealthCheck] = None
    sticky_sessions: Optional[StickySessions] = None
    tag: Optional[str] = None
    droplet_ids: Optional[List[int]] = None
    redirect_http_to_https: Optional[bool] = None
    enable_proxy_protocol: Optional[bool] = None
    enable_backend_keepalive: Optional[bool] = None
    vpc_uuid: Optional[str] = None
    created_at: Optional[datetime] = None


class OneClickApp(BaseModel):
    slug: str
    type: str


class Project(BaseModel):
    class Resource(BaseModel):
        class Links(BaseModel):
            self: str

        urn: str
        assigned_at: Optional[datetime] = None
        links: Optional[Links] = None
        status: Optional[str] = None

    id: Optional[str] = None

    # required params
    name: str
    purpose: str

    # optional params
    owner_uuid: Optional[str] = None
    owner_id: Optional[int] = None
    description: Optional[str] = None
    environment: Optional[str] = None
    is_default: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Registry(BaseModel):
    class Subscription(BaseModel):
        class Tier(BaseModel):
            name: str
            slug: str
            included_repositories: int
            included_storage_bytes: int
            allow_storage_overage: bool
            included_bandwidth_bytes: int
            monthly_price_in_cents: int

        tier: Tier
        created_at: Optional[datetime] = None
        updated_at: Optional[datetime] = None

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
    subscription_tier_slug: Optional[str] = None
    created_at: Optional[datetime] = None


class Snapshot(BaseModel):
    id: Optional[Union[str, int]] = None
    name: str
    created_at: Optional[datetime] = None
    regions: Optional[List[str]] = None
    resource_id: Optional[str] = None
    resource_type: Optional[str] = None
    min_disk_size: Optional[int] = None
    size_gigabytes: Optional[float] = None
    tags: Optional[List[str]] = None


class SSHKey(BaseModel):
    id: Optional[int] = None
    fingerprint: Optional[str] = None
    public_key: str
    name: str


class Tag(BaseModel):
    class Resource(BaseModel):
        resource_id: str
        resource_type: str

    class TagStat(BaseModel):
        class Count(BaseModel):
            count: int
            last_tagged_uri: Optional[str] = None

        count: int
        last_tagged_uri: Optional[str] = None
        droplets: Count
        images: Count
        volumes: Count
        volume_snapshots: Count
        databases: Count

    name: str
    resources: Optional[TagStat] = None


class Volume(BaseModel):
    id: Optional[str] = None

    # required params
    name: str
    region: Union[str, Region]
    size_gigabytes: int

    # optional params
    droplet_ids: Optional[List[int]] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    filesystem_type: Optional[str] = None
    filesystem_label: Optional[str] = None
    tags: Optional[List[str]] = None


class VPC(BaseModel):
    class Member(BaseModel):
        name: str
        urn: str
        created_at: datetime

    id: Optional[str] = None

    # required params
    name: str
    region: str

    # optional params
    urn: Optional[str] = None
    ip_range: Optional[str] = None
    description: Optional[str] = None
    default: Optional[bool] = None
    created_at: Optional[datetime] = None
