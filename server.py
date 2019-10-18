import openstack,os
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
    
def list_flavors(conn):
    print("List Flavors:")

    for flavor in conn.compute.flavors():
        print(flavor)


def list_images(conn):
    print("List Images:")

    for image in conn.compute.images():
        print(image)


def list_networks(conn):
    print("List Networks:")

    for network in conn.network.networks():
        print(network)


def list_servers(conn):
    print("List Servers:")

    for server in conn.compute.servers():
        print(server)

def create_keypair(conn):
    keypair = conn.compute.find_keypair("NOMEZINHO")

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name="NOMEZINHO")

        print(keypair)

        try:
            os.mkdir(SSH_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open("PRIVATE_KEYPAIR_FILE", 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod("PRIVATE_KEYPAIR_FILE", 0o400)

    return keypair


def create_server(conn):
    print("Create Server:")

    image = conn.compute.find_image("xenial")
    flavor = conn.compute.find_flavor("m1.tiny")
    network = conn.network.find_network("ext_net")
    keypair = create_keypair(conn)

    server = conn.compute.create_server(
        name="ESSE",
        image_id=image.id,
        flavor_id=flavor.id,
        networks=[{"uuid": network.id}],
        key_name=keypair.name,
    )

    server = conn.compute.wait_for_server(server)

    print(
        "ssh -i {key} root@{ip}".format(key="PRIVATE_KEYPAIR_FILE", ip=server.access_ipv4)
    )


conn =  create_connection("http://192.168.0.22:5000/v3","RegionOne","admin","admin","Joh5zou4Chahchai")

create_server(conn)
