#!/usr/bin/python3
""" Fabric script to distribute an archive to web servers """

from fabric.api import *
from os.path import exists

env.hosts = ‘107.20.129.200’ , '34.226.190.215’
env.user = 'ubuntu'  # Replace with your SSH username
env.key_filename = '~/.ssh/school’'  # Replace with your SSH private key path

def do_deploy(archive_path):
    """
    Distribute an archive to web servers
    """

    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_no_extension = archive_filename.split('.')[0]
        remote_tmp = "/tmp/"
        remote_release = "/data/web_static/releases/"
        remote_current = "/data/web_static/current"

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, remote_tmp)

        # Create the release folder
        run("mkdir -p {}{}/".format(remote_release, archive_no_extension))

        # Uncompress the archive to the release folder
        run("tar -xzf {}{} -C {}{}/".format(remote_tmp, archive_filename, remote_release, archive_no_extension))

        # Remove the uploaded archive from the web server
        run("rm {}{}".format(remote_tmp, archive_filename))

        # Move the uncompressed content to the release folder
        run("mv {0}{1}/web_static/* {0}{1}/".format(remote_release, archive_no_extension))

        # Remove the old symbolic link
        run("rm -rf {}".format(remote_current))

        # Create a new symbolic link linked to the new version
        run("ln -s {0}{1}/ {2}".format(remote_release, archive_no_extension, remote_current))

        print("New version deployed!")
        return True
    except Exception:
        return False


