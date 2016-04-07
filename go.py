#!/usr/bin/env python

import collections
import ConfigParser
import os
from os import path
import subprocess
import shutil
import time
import xmlrpclib


# Initialise.
config = ConfigParser.SafeConfigParser()
config.read('hook-test.ini')

trac_url = config.get('trac', 'url')
trac_components = config.get('trac', 'components').split()
trac_milestone = config.get('trac', 'milestone')
hook_root = config.get('hook', 'root')
hook_script = config.get('hook', 'script')
hook_func = config.get('hook', 'func')
hook = 'python:{}/{}:{}'.format(hook_root, hook_script, hook_func)

hook_env = dict(os.environ)
hook_env['PYTHONPATH'] = hook_root


def poke_trac(message):
    subprocess.call(['curl', '{}?message={}'.format(trac_url, message)])


trac = xmlrpclib.ServerProxy(trac_url)
timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())


# Prepare the repository for commits.
repo_root = path.join(os.getcwd(), 'tmp')
repo_one = path.join(repo_root, 'one')
repo_two = path.join(repo_root, 'two')


def hg(*args):
    """Call hg."""
    subprocess.check_call(('hg',) + args, env=hook_env)


shutil.rmtree(repo_root, ignore_errors=True)
os.makedirs(repo_one)
os.chdir(repo_one)
hg('init')
with open(path.join('.hg', 'hgrc'), 'w') as fp:
    fp.write('[hooks]\npretxnchangegroup = {}\n'.format(hook))
with open('README.txt', 'w') as fp:
    fp.write('nothing')
hg('add', 'README.txt')
hg('commit', '-m', 'Initial commit')
hg('clone', repo_one, repo_two)


# Create some new tickets for each component.
component_tickets = collections.defaultdict(list)
for component in trac_components:
    for i in range(5):
        milestone = trac_milestone if i in [2, 4] else ''
        ticket_id = trac.ticket.create(
            'Test ticket {} from {}'.format(i, timestamp),
            'All your base are belong to us!',
            {'component': component, 'milestone': milestone})
        ticket = trac.ticket.get(ticket_id)

        if i in [3, 4]:
            attrs = ticket[3]
            ticket = trac.ticket.update(
                ticket_id, 'Closed by test setup',
                {'_ts': attrs['_ts'], 'action': 'resolve'})

        component_tickets[component].append(ticket_id)
        print ('Created ticket #{0}: summary="{3[summary]}", '
               'status={3[status]}, component="{3[component]}", '
               'milestone={3[milestone]}'
               .format(*ticket))


# Create some commits.
os.chdir(repo_two)


def commit(msg):
    """Create a commit."""
    with open('README.txt', 'w') as fp:
        fp.write(msg)
    hg('commit', '-m', msg)

# Touch issue 0 and close 1-4.
for component in trac_components:
    tickets = component_tickets[component]
    commit('Issue {0}, Fixes {1}, Issue {2}, Fixes {4} - One'.format(*tickets))
    commit('Fixes {2}, Fixes {3} - Two'.format(*tickets))
    commit('Noissue - Three')

# Some invalid commit messages.
commit('Issue 6666 - No such ticket')
commit('Wrong format of commit message')

# Now push the commits to invoke the hook.
poke_trac('before-hook')
hg('push')
poke_trac('after-hook')
