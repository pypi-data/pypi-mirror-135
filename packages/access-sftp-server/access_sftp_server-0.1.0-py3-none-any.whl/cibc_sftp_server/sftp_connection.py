import paramiko


def establish_connection(host: str, port: int, username: str, password: str):
    server = paramiko.Transport((host, port))

    # open connection to transport server
    server.connect(username=username, password=password)
    print(f'Connecting to {host}:{port}...')

    return server


def sftp_connection(server):
    sftp = paramiko.SFTPClient.from_transport(server)
    print('Connected!')
    return sftp
