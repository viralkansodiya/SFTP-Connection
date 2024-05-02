import pysftp
from urllib.parse import urlparse
import os


class Sftp:
    def __init__(self, hostname, username, password, port=22, pem_file_path = None):
        """Constructor Method"""
        # Set connection object to None (initial value)
        self.connection = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.pem_file_path= pem_file_path

    def connect(self):
        """Connects to the sftp server and returns the sftp connection object"""

        try:
            # Get the sftp connection object
            self.connection = pysftp.Connection(
                host=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port,
            )
        except Exception as err:
            raise Exception(err)
        finally:
            print(f"Connected to {self.hostname} as {self.username}.")

    def listdir(self, remote_path):
        """lists all the files and directories in the specified path and returns them"""
        for obj in self.connection.listdir(remote_path):
            yield obj

    def listdir_attr(self, remote_path):
        """lists all the files and directories (with their attributes) in the specified path and returns them"""
        for attr in self.connection.listdir_attr(remote_path):
            yield attr

    def disconnect(self):
        """Closes the sftp connection"""
        self.connection.close()
        print(f"Disconnected from host {self.hostname}")

    def sftp_upload(self, hostname, port, username, pem_file, local_file, remote_path):
        hostname = self.hostname
        port = self.hostname
        pem_file
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey.from_private_key_file(pem_file)
            ssh.connect(hostname, port, username=username, pkey=private_key)

            sftp = ssh.open_sftp()

            # Create remote directory if it doesn't exist
            try:
                sftp.chdir(remote_path)
            except IOError:
                sftp.mkdir(remote_path)
                sftp.chdir(remote_path)

            # Upload the file
            sftp.put(local_file, remote_path + '/' + os.path.basename(local_file))

            sftp.close()
            ssh.close()

            print(f"File {local_file} uploaded successfully to {remote_path}")
        except Exception as e:
            print(f"Error: {e}")