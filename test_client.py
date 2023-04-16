from client import Client


def test_client_create():
    client1 = Client.from_name("John")
    assert(isinstance(client1, Client))
    assert(client1.name == "John")