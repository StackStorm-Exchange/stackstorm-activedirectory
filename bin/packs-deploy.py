#!/bin/python
#
import os
import argparse
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from scp import SCPClient

STACKSTORM_PACKS_DIR="/opt/stackstorm/packs"

class Cli:
    def parse(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
        # connection args
        parser.add_argument('-H', '--hostname', help='Hostname of StackStorm box')
        parser.add_argument('-U', '--username', help='Username for StackStorm box')
        parser.add_argument('-P', '--password', help='Password for StackStorm box')

        # Subparsers
        subparsers = parser.add_subparsers(dest="command")

        ## deploy
        deploy_parser = subparsers.add_parser('deploy',
                                              help="Deploy packs to a host",
                                              formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        packs_default_dir = os.path.join(os.path.dirname(__file__), '..', 'packs')
        deploy_parser.add_argument('-d', '--directory', default=packs_default_dir,
                                   help="Directory where packs are located")
        deploy_parser.add_argument('-p', '--packs', nargs='*',
                                   help=("List of packs to deploy, if empty"
                                         "then all will be deployed"))

        deploy_parser = subparsers.add_parser('examples',
                                              help="Prints examples of how to use this script to stdout"
        )
        
        args = parser.parse_args()
        if args.command == "examples":
            self.examples()
            exit(0)
        return args

    def examples(self):
        print "examples:\n"\
            "  # deploy all packs in packs/\n"\
            "  ./bin/packs-deploy.py -H host.domain.tld -P xxx -U root deploy\n"\
            "\n"\
            "  # deploy all packs in xxx/\n"\
            "  ./bin/packs-deploy.py -H host.domain.tld -P xxx -U root -d xxx/ deploy\n"\
            "\n"\
            "  # deploy a specific pack in packs/\n"\
            "  ./bin/packs-deploy.py -H host.domain.tld -P xxx -U root -p stackstorm-activedirectory deploy\n"\
            "\n"\
            "  # deploy a specific pack in xxx/\n"\
            "  ./bin/packs-deploy.py -H host.domain.tld -P xxx -U root -d xxx/ -p stackstorm-activedirectory deploy"



        
class Deploy(object):
    def __init__(self, args):
        self.args = args
        self.is_local = False
        if (self.args.hostname is None or
            self.args.hostname == "localhost" or
            self.args.hostname == "127.0.0.1"):
            self.is_local = True
            

    def run(self):
        if self.is_local:
            self.run_localhost()
        else:
            self.run_remote()

    def run_cmd(self, cmd):
        if self.is_local:
            Deploy.run_cmd_local(cmd)
        else:
            Deploy.run_cmd_ssh(self.ssh, cmd)
            
    @staticmethod
    def run_cmd_local(cmd):
        import subprocess
        cmd_args = cmd.split(' ')
        proc = subprocess.Popen(cmd_args)
        proc.wait()

    @staticmethod
    def run_cmd_ssh(ssh, cmd):
        timeout = None
        chan = ssh.get_transport().open_session(timeout=timeout)
        try:
            chan.get_pty()
            chan.settimeout(timeout)
            Deploy.run_cmd_ssh_chan(chan, cmd)
        finally:
            chan.close()

    @staticmethod
    def run_cmd_ssh_chan(chan, cmd):
        import select
        import socket
        import sys
        import termios
        import tty
        
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
        
            chan.exec_command(cmd)
        
            while True:
                r, w, e = select.select([chan, sys.stdin], [], [])
                if chan in r:
                    try:
                        x = chan.recv(1)
                        if len(x) == 0:
                            break
                        sys.stdout.write(x)
                        sys.stdout.flush()
                    except socket.timeout:
                        pass
                    
                if sys.stdin in r:
                    x = sys.stdin.read(1)
                    if len(x) == 0:
                        break
                    chan.send(x)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


    def copy_dir(self, src, dst, direction='put'):
        """
        :param src: path to source directory
        :param dst: path to destination directory
        :param direction: direction to copy the files:
            - 'put' means put the files onto a remote server
            - 'get' means get the files from a remote server
        """
        if self.is_local:
            Deploy.copy_dir_local(src, dst)
        else:
            Deploy.copy_dir_scp(self.scp, src, dst, direction)

    @staticmethod
    def copy_dir_local(src, dst):
        import shutil
        shutil.copytree(src, dst)

    @staticmethod
    def copy_dir_scp(scp, src, dst, direction):
        if direction == 'put':
            scp.put(src, remote_path=dst, recursive=True)
        elif direction == 'get':
            scp.get(src, local_path=dst, recursive=True)
        else:
            raise ValueError("Invalid direction '{}', valid=put,get")
            

    def connect_ssh(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(self.args.hostname,
                         username=self.args.username,
                         password=self.args.password)
        self.scp = SCPClient(self.ssh.get_transport())
            
    def run_remote(self):
        if self.args.hostname is None:
            raise ValueError("Missing -H/--hostname on commandline")
        if self.args.username is None:
            raise ValueError("Missing -U/--username on commandline")
        if self.args.password is None:
            raise ValueError("Missing -P/--password on commandline")
            
        self.connect_ssh()
        try:
            self.run_common()
        finally:
            self.scp.close()
            self.ssh.close()

    def run_localhost(self):
        self.run_common()

    def run_common(self):
        """ Performs the actual "deploy" work, this is generic calling
        only functions that also check if it's local/remote and behaving
        correctly
        """
        if self.args.directory is None:
            raise ValueError("Missing -d/--directory on commandline")
        if not os.path.exists(self.args.directory):
            raise ValueError("Directory given on commandline doesn't exist: {}".
                             format(self.args.directory))
        
        directory = self.args.directory
        packs = self.args.packs if self.args.packs is not None else []
        if len(packs) == 0:
            # add all directories in the "packs" directory
            for f in os.listdir(directory):
                if os.path.isdir(os.path.join(directory, f)):
                    packs.append(f)
                    
        packs_dst = []
        for pack in packs:
            pack_src  = os.path.join(directory, pack)
            pack_name = pack.replace('stackstorm-', '')
            pack_dst  = os.path.join(STACKSTORM_PACKS_DIR, pack_name)
            packs_dst.append({'name': pack_name, 'dst': pack_dst})
            
            print "Removing old pack in {}".format(pack_dst)
            self.run_cmd('sudo rm -rf {}'.format(pack_dst))
            print "Copying pack {} to {}".format(pack_src, pack_dst)
            self.copy_dir(pack_src, pack_dst, direction='put')
            print "Copying done!"

        # Set proper ownership of deployed packs, so StackStorm can access them
        self.run_cmd('sudo chgrp -R st2packs {}'.format(STACKSTORM_PACKS_DIR))
            
        # Register each pack with StackStorm
        for pack in packs_dst:
            pack_name = pack['name']
            pack_dst = pack['name']
            print "Registering pack: {}".format(pack_dst)
            self.run_cmd('sudo st2 pack register {}'.format(pack_dst))
            print "Registering done!"
            
            print "Setting up virtualenv for pack: {}".format(pack_name)
            self.run_cmd('sudo st2 run packs.setup_virtualenv update=true packs={}'.format(pack_name))
            print "Setup virtualenv done!"
            
if __name__ == '__main__':
    cli = Cli()
    args = cli.parse()
    print "cmdline args = {}".format(args)
    deploy = Deploy(args)
    deploy.run()
    

