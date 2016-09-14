# resup.py

Batch upload of resources to data package in CKAN.
Batch download and deletion from data package in CKAN.

**resup.py** handles compression, creation of a tar-archive,
checksumming, splitting of large files for upload, and
re-assemblage of thusly splitted files upon download.

Resources to be downloaded or deleted can be specified
by providing a regular expression to select resource names.
