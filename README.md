# resup.py

+ Batch upload of resources to data package in CKAN.
+ Batch download and deletion from data package in CKAN.

**resup.py** handles compression, creation of a tar-archive,
checksumming, splitting of large files for upload, and
re-assemblage of thusly splitted files upon download.

Resources to be downloaded or deleted can be specified
by providing a regular expression to select resource names.

##Usage:

    resup.py [-h] {put,get,list,del} ...

    positional arguments:
	  {put,get,list,del}  subcommands
		  put               upload ressources
		  get               download ressources
		  list              list your packages
		  del               delete resources

    optional arguments:
    -h, --help          show this help message and exit

    resup.py {put | get | list | del} -h for specific help on subcommands.
[resup.py del](#user-content-del)
-------
    resup.py put [-h] [-s SERVER] [-k API_KEY] [--tar] [--gz]
                    [--maxfilesize MAXFILESIZE] [--keepdummy] [--noclean]
                    PACKAGENAME [DIRECTORY]

    Upload a batch of files as resources to CKAN.

	positional arguments:
	  PACKAGENAME           Name of the data package
	  DIRECTORY             The directory containing the ressources to be
							uploaded. Default is the current working directory.
							Subdirectories are ignored.

	optional arguments:
	  -h, --help            show this help message and exit
	  -s SERVER          CKAN server
                                (default is https://eaw-ckan-dev1.eawag.wroot.emp-eaw.ch)
	  -k API_KEY            Your API-key. If omitted, the environment variable
							'CKAN_APIKEY' will be used.
	  --tar                 create a tar archive
	  --gz                  gzip the file(s) before upload
	  --maxfilesize MAXFILESIZE
							Maximum filesize (in bytes) for upload. Larger files
							will be split into parts <= MAXFILESIZE. The default
							is 4096 Mb.
	  --keepdummy           do not delete the ressource 'dummy', if present, from
							package. The default is to delete it.
	  --noclean             Keep the various temporary directories and files
							potentially created (e.g. "_tar", "_gz"). Default is
							to delete them.
------
    resup.py get [-h] [-s SERVER] [-k API_KEY] PACKAGENAME [DIRECTORY] [RESOURCES]

	Bulk download resources of a package in CKAN.

	positional arguments:
	  PACKAGENAME  Name of the data package
	  DIRECTORY    Directory into which ressources are downloaded. Default is the
				   current working directory.
	  RESOURCES    The name of the resource to be downloaded or a regular
				   expression that matches the resources to be downloaded, e.g.
				   ".*" (the default!)

	optional arguments:
	  -h, --help   show this help message and exit
	  -s SERVER    CKAN server
				   (default is https://eaw-ckan-dev1.eawag.wroot.emp-eaw.ch)
	  -k API_KEY   Your API-key. If omitted, the environment variable
				   'CKAN_APIKEY' will be used.
------
    resup.py list [-h] [-s SERVER] [-k API_KEY]

    List the packages that you can modify.

    optional arguments:
      -h, --help  show this help message and exit
      -s SERVER   CKAN server
                  (default is https://eaw-ckan-dev1.eawag.wroot.emp-eaw.ch)
      -k API_KEY  Your API-key. If omitted, the environment variable 'CKAN_APIKEY'
                  will be used.

------
<a id="del"></a>

	resup.py del [-h] [-s SERVER] [-k API_KEY] PACKAGENAME [RESOURCES]

	Batch delete resoures of a package in CKAN.

	positional arguments:
	  PACKAGENAME  Name of the data package
	  RESOURCES    The name of the resource to be deleted or a regular expression
				   that matches the resources to be deleted, e.g. ".*" (the
				   default!)

	optional arguments:
	  -h, --help   show this help message and exit
	  -s SERVER    CKAN server (default is https://eaw-ckan-dev1.eawag.wroot.emp-
				   eaw.ch)
	  -k API_KEY   Your API-key. If omitted, the environment variable
				   'CKAN_APIKEY' will be used.
	    

