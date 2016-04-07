# Mercurial commit hook testing setup

This is an integration setup for mercurial commit hook that integrates
with Trac issue tracker.

It creates some tickets with different components, milestones and states,
then creates some commits that reference those tickets,
then pushes the commits to a repository that has pretxnchangegroup hook enabled.

## Configuration

Copy `hook-test.ini.example` to `hook-test.ini` and fill in the URL
of your Trac instance, the list of components, the milestone
to use for new tickets and the parameters of the pre-push hook.

## Usage

Run the test with:

    $ python go.py
