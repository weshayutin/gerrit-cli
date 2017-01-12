# gerrit-cli
A simple set of Gerrit Command Line Tools.

     usage: gerrit [-h] [--host HOST] [--port PORT] [--dry-run]
                   [--config-file CONFIG_FILE] [-v]
                   {ls,show,update,abandon,restore,recheck} ...

     A simple gerrit command line interface

     positional arguments:
       {ls,show,update,abandon,restore,recheck}
         ls                  list reviews
         show                show review(s)
         update              update review(s)
         abandon             abandon review(s)
         restore             restore review(s)
         recheck             abandon review(s)

     optional arguments:
       -h, --help            show this help message and exit
       --host HOST           The gerrit host. Default: review.openstack.org
       --port PORT           The gerrit port. Default: 29418
       --dry-run             Whether or not to actually execute commands that
                             modify a review.
       --config-file CONFIG_FILE
                             The path to the gerrit-cli configuration file to use
                             for this session. (Default: ~/.gerrit-cli/gerrit-
                             cli.json
       -v, --verbose         Provide additional (verbose) debug output.
