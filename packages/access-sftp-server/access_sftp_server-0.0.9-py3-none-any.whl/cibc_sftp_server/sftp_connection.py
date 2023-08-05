import paramiko


def establishConnection(host: str, port: int, username: str, password: str):
    server = paramiko.Transport((host, port))

    # open connection to transport server
    server.connect(username=username, password=password)
    print(f'Connecting to {host}:{port}...')

    return server


def sftpConnection(server):
    sftp = paramiko.SFTPClient.from_transport(server)
    print('Connected!')
    return sftp
