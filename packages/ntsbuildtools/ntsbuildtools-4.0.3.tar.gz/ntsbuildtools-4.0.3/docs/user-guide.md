BuildTools is a collection of scripts that support the University of Oregon's Network and Telecom Services team (NTS) 
continuous integration and deployment solutions. E.g. this solution is used in Jenkinsfile pipelines.

[![PyPI version](https://badge.fury.io/py/ntsbuildtools.svg)](https://badge.fury.io/py/ntsbuildtools)

# Install BuildTools

BuildTools is packaged as `ntsbuildtools` and provided in the Python Package Index (PyPI).
So, simply use pip to install BuildTools.

    pip install ntsbuildtools

# BuildTools Usage

With BuildTools installed, the `buildtools` CLI utility should now be available in your shell.

    $ buildtools --version
    BuildTools Version: 1.3.5

Below is an example of posting a comment onto an existing BitBucket Pull Request.

    $ buildtools post bitbucket pr-comment \
        --bitbucket-url https://git.uoregon.edu \
        --user rleonar7 \ 
        --password SuperSecretPassword \ 
        --project ISN \
        --repo buildtools \
        --pull-request-id 2 \ 
        --message "Hello, world! I am BuildTools!"

![Screenshot of the created pull request comment.](https://uoregon-my.sharepoint.com/:i:/r/personal/rleonar7_uoregon_edu/Documents/share/post-bb-pr-comment.png)

## BuildTools Capabilities

BuildTools has many capabilities. These capabilities are provided as subcommands. 
To discover the subcommands available in your version of BuildTools, use the `--help` argument anywhere in the CLI. 

> BuildTools capabilities can discovered much more easily when using tab completion -- **how to enable tab completion via `argcomplete` is discussed below.**

In the example below, we see how the `--help` flag informs us that the `buildtools post bitbucket pr-comment` command is available and how to run it!

    $ buildtools --help
    usage: buildtools [-h] [--version] [--bitbucket-url BITBUCKET_URL] {post,parse} ...
     
    positional arguments:
      {post,parse}
        post                Make an HTTP POST to a target.
        parse               Parse some input (typically from a file).

    $ buildtools post --help
    usage: buildtools post [-h] {bitbucket,teams,github} ...
    
    positional arguments:
      {bitbucket,teams,github}
        bitbucket           Target Bitbucket.
        teams               Target Microsoft Teams.
        github              Target GitHub.

    $ buildtools post bitbucket --help
    usage: buildtools post bitbucket [-h] {build-status,pr-comment} ...
    
    positional arguments:
      {build-status,pr-comment}
        build-status        Set the "Build Status" in Bitbucket for a particular git commit.
        pr-comment          Posts a comment to a Bitbucket pull request, with optional arguments for 'Jenkins build 
                            annotations', indicating build status, encasing content in 'diff markdown', and more!

    $ buildtools post bitbucket pr-comment --help
    usage: buildtools post bitbucket pr-comment [-h] [--version] [--bitbucket-url BITBUCKET_URL]
                                                (--message COMMENT_MESSAGE | --file COMMENT_FILE | --json JSON_OUTPUT | --json-file JSON_FILE)
                                                --user USER --password PASSWORD --project PROJECT
                                                --repo REPO --pull-request-id PULL_REQUEST_ID
                                                [--diff-markdown]
                                                [--code-markdown]
                                                [--max-comment-size MAX_COMMENT_SIZE] [--tail TAIL]
                                                [--build-annotation]
                                                [--playbook-limit PLAYBOOK_LIMIT]
                                                [--build-id BUILD_ID] [--build-url BUILD_URL]
                                                [--build-status {SUCCESS,UNSTABLE,FAILURE,NOT_BUILD,ABORTED}]
    
    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --bitbucket-url BITBUCKET_URL
                            URL for Bitbucket. [env var: BITBUCKET_URL]
      --message COMMENT_MESSAGE, -m COMMENT_MESSAGE
                            Provide the comment as a message on the command line.
      --file COMMENT_FILE, -f COMMENT_FILE
                            Provide the comment in a file.
      --json JSON_OUTPUT, -j JSON_OUTPUT
                            Provide ansible JSON output as a message on the command line (which will
                            be parsed to extract build-status info). NOTE: Additional 'formatting'
                            arguments, such as '--code-markdown', are ignored when using json input.
      --json-file JSON_FILE
                            Provide ansible JSON output as a file (which will be parsed to extract
                            build-status info). NOTE: Additional 'formatting' arguments, such as '--
                            code-markdown', are ignored when using json input.
      --user USER           Bitbucket user that will be used to authenticate to Bitbucket. [env var:
                            BITBUCKET_USER]
      --password PASSWORD   Bitbucket password (or Personal Access Token) for the Bitbucket user.
                            [env var: BITBUCKET_PASSWORD]
      --project PROJECT     The Bitbucket project key for the project where the pull request exists.
                            [env var: BITBUCKET_PROJECT]
      --repo REPO           The Bitbucket repository slug for the repository where the pull request
                            exists. [env var: BITBUCKET_REPO]
      --pull-request-id PULL_REQUEST_ID
                            The ID of the Bitbucket pull request to be commented on. [env var: PR_ID]
    
    formatting:
      --diff-markdown       Wrap the provided comment in diff markdown. E.g. ```diff \{comment\}) ```
      --code-markdown       Wrap the provided comment in code markdown. E.g. ``` \{comment\}) ```
      --max-comment-size MAX_COMMENT_SIZE
                            Fragment the comment into based on the maximum comment size.
      --trim TRIM           Only print the last `TRIM` lines of the provided message/file.

### Tab Completion? Yes, please!

BuildTools works as a CLI by default, and can support tab completion via the [`argcomplete` module](https://kislyuk.github.io/argcomplete/).

    $ buildtools (double press 'tab' to see possible commands) 
    --bitbucket-url  --help           --version        -h               parse            post             
    $ buildtools post (double press 'tab')
    --help     -h         bitbucket  github     teams      
    $ buildtools post bitbucket (double press 'tab')
    --help        -h            build-status  pr-comment    
    $ buildtools post bitbucket pr-comment

Unfortunately, this does not work 'out of the box' without doing some 'bash configuration.'
So, run the following commands to enable argcomplete in your bash session:
        
    pip install argcomplete
    eval "$(register-python-argcomplete buildtools)"

#### Tab Completion for *all* bash sessions

If you want `buildtools` tab completion to work for *all* your bash sessions, we just need to install argcomplete for your user and add a line to your `bashrc` file.

Install argcomplete to your Python user site-package:

    deactivate # (if currently in a Python venv)
    pip3 install --user argcomplete

Add the following to your `~/.bashrc`:

    if [ -x "register-python-argcomplete" ] ; then
        eval "$(register-python-argcomplete buildtools)"
    fi
