# Mercurial commit hook testing setup

This is a test setup for mercurial commit hook that integrates
with Trac issue tracker.

I runs the following scenario:
* Create some tickets with different components, milestones and states,
* Create some commits that reference those tickets,
* Push the commits to a repository that has target hook installed for pretxnchangegroup.

## Configuration

Copy `hook-test.ini.example` to `hook-test.ini` and fill in the URL
of your Trac instance, the list of components, the milestone
to use for new tickets and the parameters of the hook.

## Usage

Run the test with:

    $ python go.py
