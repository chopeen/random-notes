# Multiple SSH keys on a single machine

## Problem

The GitHub account `github.com/chopeen` is configured to use the key `github_chopeen`
and `github.com/grzenkom` uses `id_rsa`.

Pushing to `github.com/chopeen` fails with error:

> ERROR: Permission to chopeen/learning-transformers.git denied to grzenkom.  
> fatal: Could not read from remote repository.

Running push in verbose mode (`GIT_SSH_COMMAND="ssh -v" git push`) shows:

    debug1: Offering RSA public key: /home/users/grzenkom/.ssh/id_rsa
    debug1: Server accepts key: pkalg ssh-rsa blen 279
    debug1: Authentication succeeded (publickey).
    Authenticated to github.com ([140.82.118.4]:22).
    debug1: channel 0: new [client-session]
    debug1: Entering interactive session.
    debug1: pledge: network
    debug1: Sending environment.
    debug1: Sending env LC_CTYPE = en_US.UTF-8
    debug1: Sending env LANG = en_US.UTF-8
    debug1: Sending command: git-receive-pack 'chopeen/learning-transformers.git'
    ERROR: Permission to chopeen/learning-transformers.git denied to grzenkom.
    debug1: client_input_channel_req: channel 0 rtype exit-status reply 0

Git finds file `id_rsa`, offers it to GitHub and is recognized as `grzenkom`.
Since it was successful, it does not try to use `github_chopeen` at all.

## Solution

Select the key file to be used manually:

    # remove all cached keys
    eval `ssh-agent -s`
    ssh-add -D
    
    # verify they were removed
    ssh-add -l
    
    # add a key
    ssh-add ~/.ssh/github_chopeen

It is also possible to define a permanent configuration in `.ssh/config`, but later you
need to replace `github.com` with alternative domain names specified in SSH configuration.

