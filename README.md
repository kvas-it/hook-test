# Mercurial commit hook testing repo

Create some tickets in the issue tracker then create some commits
that reference those tickets, then push them to a repository that
has pretxnchangegroup hook enabled. This will cause the hook to
do its special magic on the tickets.

## Configuration

Copy `hook-test.ini.example` to `hook-test.ini` and fill in the URL
of your Trac instance, the list of components and the milestone
to use for new tickets, and the parameters of the pre-push hook.

## Usage

    $ python go.py
