#!/usr/bin/env python


"""\
usage: tomcat_users.py TOMCAT_USERS_XML USER PASSWORD
"""


import os
import shutil
import sys
import xml.etree.ElementTree as ET


def make_backup(input_file):
    backup_file = input_file + '.bk'
    if os.path.exists(backup_file):
        os.remove(backup_file)
    shutil.copy2(input_file, backup_file)


def add_role(node, rolename='tomcat'):
    ET.SubElement(node, 'role', {'rolename': 'tomcat'}).tail = '\n  '


def add_user(node, username, passwd, rolename='tomcat'):
    ET.SubElement(
        node,
        'user',
        {'username': username, 'password': passwd, 'roles': 'tomcat'}
        ).tail = '\n'


def main():
    if len(sys.argv) < 4:
        print __doc__
        raise SystemExit
    input_file = sys.argv[1]
    if input_file in ('--help', '-h', 'help'):
        print __doc__
        raise SystemExit
    username = sys.argv[2]
    passwd = sys.argv[3]

    make_backup(input_file)

    with open(input_file) as f:
        tree = ET.parse(f)

    root = tree.getroot()
    add_role(root)
    add_user(root, username, passwd)

    tree.write(input_file)


if __name__ == '__main__':
    main()
