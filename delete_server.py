import errno
import os
import openstack


def create_connection(auth_url, region, project_name, username, password):

    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
        region_name=region,
        app_name='examples',
        app_version='1.0',
    )


"""
Delete resources with the Compute service.

For a full guide see
https://docs.openstack.org/openstacksdk/latest/user/guides/compute.html
"""


def delete_keypair(conn):
    print("Delete Key Pair:")

    keypair = conn.compute.find_keypair("NOMEZINHO")

    try:
        os.remove("PRIVATE_KEYPAIR_FILE")
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e

    print(keypair)

    conn.compute.delete_keypair(keypair)


def delete_server(conn):
    print("Delete Server:")

    server = conn.compute.find_server("ESSE")

    print(server)

    conn.compute.delete_server(server)



conn =  create_connection("http://192.168.0.22:5000/v3","RegionOne","admin","admin","Joh5zou4Chahchai")
delete_server(conn)
delete_keypair(conn)
