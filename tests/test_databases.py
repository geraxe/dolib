import pytest
from httpx import HTTPStatusError

from dolib.client import AsyncClient, Client
from dolib.models import DBCluster, DBReplica


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_databases(client: Client) -> None:
    database = DBCluster(
        name="dolib-test-database",
        engine="pg",
        region="fra1",
        size="db-s-2vcpu-4gb",
        num_nodes=1,
        tags=["test"],
    )

    # create database
    created_database = client.databases.create(database)
    assert isinstance(created_database, DBCluster)
    assert created_database.id is not None

    # list databases
    databases = client.databases.all()
    assert len(databases) > 0

    # filter databases
    databases = client.databases.filter()
    filtered_databases = client.databases.filter(tag_name="test")
    assert len(filtered_databases) <= len(databases)

    # read database
    read_database = client.databases.get(str(created_database.id))
    assert read_database.id == created_database.id
    assert isinstance(read_database, DBCluster)

    # add replica
    repl = DBReplica(
        name="test-repl",
        region="ams3",
        size="db-s-2vcpu-4gb",
    )
    replica = client.databases.add_replica(str(created_database.id), repl)
    assert isinstance(replica, DBReplica)

    # get replica
    read_replica = client.databases.get_replica(str(created_database.id), replica.name)
    assert isinstance(read_replica, DBReplica)

    # list replicas
    replicas = client.databases.replicas(str(created_database.id))
    assert len(replicas) > 0

    # delete replica
    client.databases.delete_replica(str(created_database.id), replica)

    user = DBCluster.User(name="test")

    # add user
    created_user = client.databases.add_user(str(created_database.id), user)
    assert user.name == created_user.name
    assert isinstance(created_user, DBCluster.User)

    # get user
    read_user = client.databases.get_user(str(created_database.id), user.name)
    assert user.name == read_user.name
    assert isinstance(read_user, DBCluster.User)

    # list users
    users = client.databases.users(str(created_database.id))
    assert len(users) > 0
    assert isinstance(users[0], DBCluster.User)

    # delete user
    client.databases.delete_user(str(created_database.id), read_user)

    db = DBCluster.DB(name="test-db")

    # add database
    created_db = client.databases.add_db(str(created_database.id), db)
    assert isinstance(created_db, DBCluster.DB)

    # read db
    read_db = client.databases.get_db(str(created_database.id), created_db.name)
    assert isinstance(read_db, DBCluster.DB)

    # list dbs
    dbs = client.databases.dbs(str(created_database.id))
    assert len(dbs) > 0
    assert isinstance(dbs[0], DBCluster.DB)

    # delete db
    client.databases.delete_db(str(created_database.id), created_db)

    # resize cluster
    with pytest.raises(HTTPStatusError):
        client.databases.resize(
            str(created_database.id), size="db-s-2vcpu-4gb", num_nodes=1
        )

    # migrate cluster
    client.databases.migrate(str(created_database.id), region="ams3")

    # delete database
    client.databases.delete(database=created_database)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_databases(async_client: AsyncClient) -> None:
    database = DBCluster(
        name="dolib-test-database",
        engine="pg",
        region="fra1",
        size="db-s-2vcpu-4gb",
        num_nodes=1,
        tags=["test"],
    )

    # create database
    created_database = await async_client.databases.create(database)
    assert isinstance(created_database, DBCluster)
    assert created_database.id is not None

    # list databases
    databases = await async_client.databases.all()
    assert len(databases) > 0

    # filter databases
    databases = await async_client.databases.filter()
    filtered_databases = await async_client.databases.filter(tag_name="test")
    assert len(filtered_databases) <= len(databases)

    # read database
    read_database = await async_client.databases.get(str(created_database.id))
    assert read_database.id == created_database.id
    assert isinstance(read_database, DBCluster)

    # add replica
    repl = DBReplica(
        name="test-repl",
        region="ams3",
        size="db-s-2vcpu-4gb",
    )
    replica = await async_client.databases.add_replica(str(created_database.id), repl)
    assert isinstance(replica, DBReplica)

    # get replica
    read_replica = await async_client.databases.get_replica(
        str(created_database.id), replica.name
    )
    assert isinstance(read_replica, DBReplica)

    # list replicas
    replicas = await async_client.databases.replicas(str(created_database.id))
    assert len(replicas) > 0

    # delete replica
    await async_client.databases.delete_replica(str(created_database.id), replica)

    user = DBCluster.User(name="test")

    # add user
    created_user = await async_client.databases.add_user(str(created_database.id), user)
    assert user.name == created_user.name
    assert isinstance(created_user, DBCluster.User)

    # get user
    read_user = await async_client.databases.get_user(
        str(created_database.id), user.name
    )
    assert user.name == read_user.name
    assert isinstance(read_user, DBCluster.User)

    # list users
    users = await async_client.databases.users(str(created_database.id))
    assert len(users) > 0
    assert isinstance(users[0], DBCluster.User)

    # delete user
    await async_client.databases.delete_user(str(created_database.id), read_user)

    db = DBCluster.DB(name="test-db")

    # add database
    created_db = await async_client.databases.add_db(str(created_database.id), db)
    assert isinstance(created_db, DBCluster.DB)

    # read db
    read_db = await async_client.databases.get_db(
        str(created_database.id), created_db.name
    )
    assert isinstance(read_db, DBCluster.DB)

    # list dbs
    dbs = await async_client.databases.dbs(str(created_database.id))
    assert len(dbs) > 0
    assert isinstance(dbs[0], DBCluster.DB)

    # delete db
    await async_client.databases.delete_db(str(created_database.id), created_db)

    # resize cluster
    with pytest.raises(HTTPStatusError):
        await async_client.databases.resize(
            str(created_database.id), size="db-s-2vcpu-4gb", num_nodes=1
        )

    # migrate cluster
    await async_client.databases.migrate(str(created_database.id), region="ams3")

    # delete database
    await async_client.databases.delete(database=created_database)
