# resup

[![Build Status](https://travis-ci.org/eawag-rdm/resup.svg?branch=master)](https://travis-ci.org/eawag-rdm/resup) Python 2.7, PyPy

-------



+ Batch upload of resources to data package in CKAN.
+ Batch download and deletion from data package in CKAN.

**resup** handles compression, creation of a tar-archive,
checksumming, splitting of large files for upload, and
re-assemblage of thusly splitted files upon download.

Resources to be uploaded, downloaded or deleted can be specified
by providing a regular expression to select resource names.

See [Usage](#usage)


## Installation:

[From Source](#srcinstall) | [Windows](#package-for-windows) | [Linux](#linstall)

<a id="srcinstall">

### Installation from source

**Required:** Python 2.7 or PyPy   
**Recommendation:** Install into a *virtual environment*

```
virtualenv venv
source venv/bin/activate
pip install --process-dependency-links git+https://github.com/eawag-rdm/resup.git

```

### Package for Windows

We provide an installer for Windows (tested with Win7). Installation does **not** require administrator privileges.

1. Download https://github.com/eawag-rdm/resup/raw/master/WindowsInstaller/resup_setup.exe.
2. Run it.
3. Follow instructions and allow the installer to reboot your computer.

You can access the program as `resup` via `cmd.exe` or `powershell.exe` from any location.

<a id="linstall">

### Package for Linux

We provide packaged versions of resup that do not require a Python installation.

One version was built on a x86_64 machine running a default install of
CentOS 6.8. This build uses pretty antique system libraries, should
therefore run on most Linuxes, but throws "InsecurePlatformWarning"s.

The other version was built on a fairly modern Debian 4.6.

1. Download https://github.com/eawag-rdm/resup/raw/master/resup/dist/resup_x86_64_CentOS_6.8   
    **or** https://github.com/eawag-rdm/resup/raw/master/resup/dist/resup_x86_64_Debian_4.6.4.
2. Copy to an appropriate location, e.g. `cp resup_x86_64_CentOS_6.8 $HOME/resup`
3. Make it excecuteable: `chmod u+x  $HOME/resup`


## Usage:

    resup [-h] {put,get,list,del} ...

    positional arguments:
	  {put,get,list,del}  subcommands
		  put               upload ressources
		  get               download ressources
		  list              list your packages
		  del               delete resources

    optional arguments:
    -h, --help          show this help message and exit

resup {[put](#user-content-put) | [get](#user-content-put) | [list](#user-content-list) | [del](#user-content-del)} -h for specific help on subcommands.

-------
<a id="put"></a>

	   usage: resup put [-h] [-s SERVER] [-k API_KEY] [--tar] [--gz]
	                    [--maxfilesize MAXFILESIZE] [--chksum HASHDIGEST]
	                    [--keepdummy] [--noclean]
	                    PACKAGENAME [DIRECTORY] [RESOURCES]

	   Upload a batch of files as resources to CKAN.

	   positional arguments:
	     PACKAGENAME           Name of the data package
	     DIRECTORY             The directory containing the ressources to be
	                           uploaded. Default is the current working directory.
	                           Subdirectories are ignored.
	     RESOURCES             A regular expression that matches the resources to be
	                           uploaded, e.g. ".*" (the default)

	   optional arguments:
	     -h, --help            show this help message and exit
	     -s SERVER             CKAN server (default is https://eaw-ckan-
	                           dev1.eawag.wroot.emp-eaw.ch)
	     -k API_KEY            Your API-key. If omitted, the environment variable
	                           'CKAN_APIKEY' will be used.
	     --tar                 create a tar archive
	     --gz                  gzip the file(s) before upload
	     --maxfilesize MAXFILESIZE
	                           Maximum filesize (in bytes) for upload. Larger files
	                           will be split into parts <= MAXFILESIZE. The default
	                           is 4096 Mb.
	     --chksum HASHDIGEST   The type of cryptographic hash used to calculate a
	                           checksum. Possible values are "sha1" (the default),
	                           "sha256" and "false" (for skipping checksum
	                           calculation).
	     --keepdummy           do not delete the ressource 'dummy', if present, from
	                           package. The default is to delete it.
	     --noclean             Keep the various temporary directories and files
	                           potentially created (e.g. "_tar", "_gz"). Default is
	                           to delete them.

------
<a id="list"></a>

    resup get [-h] [-s SERVER] [-k API_KEY] PACKAGENAME [DIRECTORY] [RESOURCES]

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
 <a id="list"></a>
 
    resup list [-h] [-s SERVER] [-k API_KEY]

    List the packages that you can modify.

    optional arguments:
      -h, --help  show this help message and exit
      -s SERVER   CKAN server
                  (default is https://eaw-ckan-dev1.eawag.wroot.emp-eaw.ch)
      -k API_KEY  Your API-key. If omitted, the environment variable 'CKAN_APIKEY'
                  will be used.

------
<a id="del"></a>

	resup del [-h] [-s SERVER] [-k API_KEY] PACKAGENAME [RESOURCES]

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
	    

