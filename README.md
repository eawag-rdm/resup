# resup.py

+ Batch upload of resources to data package in CKAN.
+ Batch download and deletion from data package in CKAN.

**resup.py** handles compression, creation of a tar-archive,
checksumming, splitting of large files for upload, and
re-assemblage of thusly splitted files upon download.

Resources to be downloaded or deleted can be specified
by providing a regular expression to select resource names.

**usage:** `resup.py [-h] {put,get,list,del} ...`

```bash
positional arguments:
  {put,get,list,del}  subcommands
    put               upload ressources
    get               download ressources
    list              list your packages
    del               delete resources

optional arguments:
  -h, --help          show this help message and exit

resup.py {put | get | list | del} -h for specific help on subcommands.

