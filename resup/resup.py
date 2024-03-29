# -*- coding: utf-8 -*-
import ckanapi
import ckanapi.cli.progressbar as progressbar
import requests
import argparse
import hashlib
import tarfile
import time
import gzip
import shutil
import uuid
import re
import sys
import os
import io
import stat
import time
import urllib3
import pickle as pickle

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST = 'http://eaw-ckan-prod1.eawag.wroot.emp-eaw.ch'
MAXFILESIZE = 5 * 2**30 # max filesize: 5Gb
CHUNKSIZE = 4 * 2**10   # for tuning

class Connection(object):
    def __init__(self, args):
        try:
            apikey = args.get('k') or [os.environ['CKAN_APIKEY']]
        except KeyError:
            print('ERROR: No API key found. Either provide it with with the \'-k\' ' +\
                'option or set the environment variable \'CKAN_APIKEY\', e.g. ' +\
                'in bash:\n\'export CKAN_APIKEY=xxxxxxxxxxxxxxxxxxxxx\'')
            sys.exit(1)
        else:
            apikey = apikey[0]
        server = args.get('s') or [HOST]
        server = server[0]
        self.conn = ckanapi.RemoteCKAN(server, apikey=apikey)

    def get_connection(self):
        return self.conn
    
class Parser(object):
    def __init__(self):
        self.pa = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=
"""
Batch upload of resources to data package in CKAN.
Batch download and deletion from data package in CKAN.

{} handles compression, creation of a tar-archive,
checksumming, splitting of large files for upload, and
re-assemblage of thusly splitted files upon download.

Resources to be downloaded or deleted can be specified
by providing a regular expression to select resource names.
""".format(os.path.basename(sys.argv[0])),
            epilog=
"""
{} {{put | get | list | del}} -h for specific help on subcommands.

The package has to exist already. If it doesn't,
create one using the web-interface. You can\'t create
a package without resources through the web-interface.
You might want to create a resource with name "dummy"
(and enter anything after clicking on "Link"). This
resource will be deleted once the real resources have
been uploaded.
 
""".format(os.path.basename(sys.argv[0]))
            )
        # parent parser (common arguments for all subcommands)
        papa = argparse.ArgumentParser(add_help=False)
        papa.add_argument('-s', type=str, metavar='SERVER', nargs=1,
                          help='CKAN server (default is '+HOST+')')
                          
        papa.add_argument('-k', nargs=1, metavar='API_KEY',
                          help='Your API-key. If omitted, the environment variable \'CKAN_APIKEY\' will be used.')

      
        subparsers = self.pa.add_subparsers(help='subcommands', dest='subcmd')
        
        # put subcommand
        pa_put = subparsers.add_parser('put', help='upload resources',
                                       parents=[papa],
                                       description='Upload a batch of files ' +
                                       'as resources to CKAN.')

        pa_put.add_argument('pkg_name', metavar='PACKAGENAME', type=str,
                            help='Name of the data package')
  
        pa_put.add_argument('directory', metavar='DIRECTORY', type=str, nargs='?',
                            default=os.curdir,
                            help='The directory containing the resources '+
                            'to be uploaded. Default is the current working ' +
                            'directory. Subdirectories are ignored. Files in this ' +
                            'directory and auto-generated subdirectories (' +
                            '"_tar", "_gz", "_parts", "_checksums") must not ' +
                            'be modified after it has been ' +
                            'used as a source directory for resup for the '+
                            'first time.')

        pa_put.add_argument('resources', metavar='RESOURCES', type=str, nargs='?',
                            default='.*',
                            help='A regular expression that matches the resources ' +
                            'to be uploaded, e.g. \".*\" (the default)')

        pa_put.add_argument('--tar', action='store_true', help='create a tar archive')

        pa_put.add_argument('--gz', action='store_true', help='gzip the file(s) before upload')

        pa_put.add_argument('--maxfilesize', type=float, metavar='MAXFILESIZE',
                            help='Maximum filesize (in bytes) for upload. Larger files ' +
                            'will be split into parts <= MAXFILESIZE. ' +
                            'The default is {} Mb.'.format(MAXFILESIZE / 2**20),
                            default=MAXFILESIZE)

        pa_put.add_argument('--nochksum', action='store_true',
                             help='Do not calculate a cryptographic checksum')

        pa_put.add_argument('--keepdummy', action='store_true',
                            help='do not delete the resource \'dummy\', if present, '+
                            'from package. The default is to delete it.')

        pa_put.add_argument('--noclean', action='store_true', help='Keep the ' +
                            'various temporary directories and files ' +
                            'potentially created (e.g. "_tar", "_gz"). ' +
                            'Default is to delete them.')

        pa_put.add_argument('--resourcetype', type=str, metavar='RESOURCETYPE',
                            help='The Resource Type attached to the upload. '
                            'Choose one that applies to all uploaded files. '
                            'Available are "Dataset", "Collection", "Text", '
                            '"Image", "Audiovisual", "Software", "Sound", '
                            '"GeospatialData", "Model", "Event", '
                            '"InteractiveResource", "PhysicalObject", '
                            '"Service", "Workflow", "Other". '
                            'The default is "Collection", which is suited to '
                            'describe heterogeneous sets of files.')

        pa_put.add_argument('--upload_empty', action='store_true',
                            help='upload empty files instead f the real resources.')

        pa_put.add_argument('--tmpdir', metavar='TMPDIR', type=str,
                            default=os.curdir,
                            help='The directory for temporary files, such as ' +
                            'checksums and parts of files. Default is the ' +
                            'current working directory. Using this ' +
                            'option, you are responsible to keep track of ' +
                            'which tmp-dir belongs to which upload-directory.')

        # get subcommand
        pa_get = subparsers.add_parser('get', help='download resources',
                                       parents=[papa],
                                       description='Bulk download '+
                                       'resources of a package in CKAN.')
        pa_get.add_argument('pkg_name', metavar='PACKAGENAME', type=str,
                            help='Name of the data package')
        pa_get.add_argument('--quiet','-q', action='store_true',
                            help='Omit asking for confirmation if a dowloaded ' +
                            'resource\'s checksum doesn\'t match (useful if ' +
                            'files on the server don\'t have a checksum) and ' +
                            'also if local files will be overwritten')
  
        pa_get.add_argument('directory', metavar='DIRECTORY', type=str, nargs='?',
                        default=os.curdir,
                        help='Directory into which resources are downloaded. ' +
                        'Default is the current working directory.')
        
        pa_get.add_argument('resources', metavar='RESOURCES', type=str, nargs='?',
                        default='.*',
                        help='The name of the resource to be downloaded or ' +
                        'a regular expression that matches the resources ' +
                        'to be downloaded, e.g. \".*\" (the default!)')
   

        # list subcommand
        pa_list = subparsers.add_parser('list', help='list your packages',
                                        parents=[papa],
                                        description='List the packages that '+
                                        'you can modify.')

        # delete subcommand
        pa_del = subparsers.add_parser('del', help='delete resources',
                                       parents=[papa],
                                       description='Batch delete resoures of '+
                                       'a package in CKAN.')
        
        pa_del.add_argument('pkg_name', metavar='PACKAGENAME', type=str,
                            help='Name of the data package')
        
        pa_del.add_argument('resources', metavar='RESOURCES', type=str, nargs='?',
                            default='.*',
                            help='The name of the resource to be deleted or ' +
                            'a regular expression that matches the resources ' +
                            'to be deleted, e.g. \".*\" (the default!)')
        
    def parse(self, arglist):
        arguments = vars(self.pa.parse_args(args=arglist))
        return arguments

# ### END of Parser() ##########################################

class Put(object):
    
    def __init__(self, args):
        self.pkg_name = args['pkg_name']
        self.directory = os.path.normpath(args['directory'])
        failmsg = 'Upload directory "{}" doesn\'t exist. Aborting.'.format(self.directory)
        self._checkdir(self.directory, failmsg)
        self.resources = args['resources']
        self.connection = args['connection']
        self.gz = args['gz']
        self.tar = args['tar']
        self.maxsize = args['maxfilesize']
        self.keepdummy = args['keepdummy']
        self.nochksum = args['nochksum']
        self.hashtype = 'sha256'
        self.noclean = args['noclean']
        self.resource_type = args['resourcetype']
        self.upload_empty = args['upload_empty']
        self.tmpdir = args['tmpdir']
        failmsg = 'Temp-directory "{}" doesn\'t exist. Aborting.'.format(self.tmpdir)
        self._checkdir(self.tmpdir, failmsg)
        self.checksumsdir = False
        
        allfiles = [os.path.normpath(os.path.join(self.directory, f))
                    for f in os.listdir(self.directory)
                    if os.path.isfile(os.path.normpath(
                            os.path.join(self.directory, f)))]
        self.resourcefiles = [f for f in allfiles
                              if not re.match('.*\.(yaml|yml)', f)]
        self.resourcefiles = [f for f in self.resourcefiles if
                              re.match(self.resources, os.path.basename(f))]
        self.metafiles = [f for f in allfiles
                              if re.match('.*\.(yaml|yml)', f)]
        self.metadata = {f: self._mk_meta_default(f) for f in self.resourcefiles}
        self.partfiles = {}
        self.id_to_filename = {}


    def _checkdir(self, directory, failmsg):
        if os.path.exists(directory):
                return()
        print(failmsg)
        sys.exit(1)

    def _mk_meta_default(self, fn):
        default_meta = {
            'package_id': self.pkg_name,
            'citation': '',
            'name': '',
            'resource_type': self.resource_type or 'Dataset',
            'url': 'dummy',
            'restricted_level': 'public'
        }
        metadict = dict(default_meta)
        metadict.update({'name': os.path.basename(fn)})
        if not self.nochksum:
            metadict.update({'hashtype': self.hashtype})
        return metadict

    
    def _split_files(self):

        def newpartsfile(oldfile, count):
            if oldfile:
                oldfile.close()
            else:
                self.partfiles[filename] = []
            partsname = os.path.join(partsdir,
                                     os.path.basename(filename) +
                                     '.{:0=4}'.format(count))
            fpart = open(partsname, 'wb')
            print("    writing new parts-file: {}".format(partsname))
            self.partfiles[filename].append(partsname)
            return(fpart)

        def update_part_metadata(filename):
            for fpart in self.partfiles[filename]:
                self.metadata[fpart] = dict(self.metadata[filename])
                self.metadata[fpart]['name'] = os.path.basename(fpart)
            del self.metadata[filename]

        chunksize = CHUNKSIZE
        partsdir = os.path.join(self.tmpdir, '_parts')
        if not os.path.exists(partsdir):
            os.mkdir(partsdir)
        
        for filename in [f for f in list(self.metadata.keys())
                         if os.stat(f).st_size > self.maxsize]:
            print("splitting {}".format(filename))
            count = 1
            cur_partsfile = newpartsfile(None, count)
            cur_size = 0
            with open(filename, 'rb') as f:
                for chunk in iter(lambda: f.read(chunksize), b''):
                    cur_size += chunksize
                    if cur_size > self.maxsize:
                        count += 1
                        cur_partsfile = newpartsfile(cur_partsfile, count)
                        cur_size = chunksize
                    cur_partsfile.write(chunk)
                cur_partsfile.close()
            update_part_metadata(filename)

    def _chksum(self):
        checksumsdir = os.path.join(self.tmpdir, '_checksums')
        allmetafile = os.path.join(checksumsdir, "allchecksums.pkl")
        if os.path.exists(allmetafile):
            print("loading existing checksums")
            oldmeta = pickle.load(open(allmetafile, "rb"))
        for filename in list(self.metadata.keys()):
            try:
                self.metadata[filename]['hash'] = oldmeta[filename]['hash']
            except NameError:
                hash_sha = hashlib.sha256()
                print("Calculating checksum for {} ...".format(filename))
                t0 = time.time()
                with open(filename, 'rb') as f:
                    for chunk in iter(lambda: f.read(8192), b''):
                        hash_sha.update(chunk)
                digest = hash_sha.hexdigest()
                deltat = time.time() - t0
                print("    time: {} seconds".format(deltat))
                print('    {}: {}'.format('sha256', digest))
                self.metadata[filename]['hash'] = digest
            else:
                print("Found pre-calculated checksum for {}.".format(filename))

        if not os.path.exists(checksumsdir):
            os.mkdir(checksumsdir)
        with open(allmetafile, "wb") as f:
            pickle.dump(self.metadata, f)

    def _gnuzip(self):
        gzdir = os.path.join(self.tmpdir, '_gz')
        if not os.path.exists(gzdir):
            os.mkdir(gzdir)
        for f in list(self.metadata.keys()):
            fn_out = os.path.join(gzdir, os.path.basename(f) + '.gz')
            print('compressing {} ...'.format(f))
            with open(f, 'rb') as fin, gzip.open(fn_out, 'wb') as fout:
                shutil.copyfileobj(fin, fout)
            self.metadata[fn_out] = self.metadata[f]
            self.metadata[fn_out].update({'name': os.path.basename(fn_out)})
            del self.metadata[f]

    def _tar(self):
        tardir = os.path.join(self.tmpdir, '_tar')
        if not os.path.exists(tardir):
            os.mkdir(tardir)
        fn_out = os.path.join(tardir,
                              os.path.basename(self.directory) +'.tar')
        print('Creating tar-archive: {}'.format(fn_out))
        with tarfile.open(fn_out, 'w') as tf:
            for f_in in list(self.metadata.keys()):
                print('    adding file {}'.format(f_in))
                tf.add(f_in)
        self.metadata = {fn_out: self._mk_meta_default(fn_out)}

    def _upload(self):
        for res in sorted(self.metadata.keys()):
            self.metadata[res]['size'] = os.stat(res).st_size
            print("uploading {} ({})".format(res, self.metadata[res]['size']))
            print(self.metadata[res])
            time0 = time.time()
            if self.upload_empty:
                files = {'upload': io.StringIO('DUMMY')}
            else:
                files={'upload': open(res, 'rb')}
            upload_result = self.connection.call_action(
                'resource_create', self.metadata[res],
                files=files,
                progress=progressbar.mkprogress, requests_kwargs={'verify': False})
            print(('total time: {} s'.format(time.time()-time0)))
            # record resource id / filename mapping
            if self.upload_empty: 
                self.id_to_filename.update({res: upload_result['id']})

    def _clean(self):
        if self.noclean:
            return()
        for d in [os.path.join(self.tmpdir, tmp)
                  for tmp in ['_gz', '_parts', '_tar']]:
            if os.path.exists(d):
                shutil.rmtree(d)

    def upload(self):
        if self.gz:
            self._gnuzip()    
        if self.tar:
            self._tar()
        self._split_files()
        if not self.nochksum:
            self._chksum()
        self._upload()
        if not self.keepdummy:
            del_resources({'pkg_name': self.pkg_name,
                           'connection': self.connection,
                           'resources': 'dummy'})
        if self.upload_empty:
            print((self.id_to_filename))
        self._clean()

# ### END of Put() ##########################################
                 
class Get(object):
    def __init__(self, args):
        self.conn = args['connection']
        self.pkg_name = args['pkg_name']
        self.directory = os.path.normpath(args['directory'])
        self.resources = args['resources']
        self.yes = args['quiet']
        self.partpatt = re.compile('^(?P<basename>.+)\.(?P<idx>\d+)$')
        self.downloaddict = {}
        check_package(args)
        self._checkdir()
        try:
            self.resources = re.compile(self.resources)
        except:
            print(('It seems "{}" is not a valid regular expression.'
                  .format(self.resources)))
            print('Aborting!')
            sys.exit(1)


    def _checkdir(self):
        testfile =  os.path.join(self.directory,
                                 'testwriteable_64747354612458526831012')
        try:
            with open(testfile, 'wb') as test:
            #add bytes identifier for py3 compatibility
                test.write(b'0')
        except Exception as e:
            print(e)
            sys.exit('Can\'t write in {}. Aborting.'.format(self.directory))
        else:
            os.remove(testfile)

    def _getresources(self):
        res = self.conn.call_action('package_show', {'id': self.pkg_name}, requests_kwargs={'verify': False})
        res = res.get('resources')
        if not res:
            print('No resources in package {}. Aborting.'.format(self.pkg_name))
            sys.exit(1)
        return(res)

    def _filterresources(self, res):
        res1 = [r for r in res if re.match(self.resources, r['name'])]
        return(res1)
        

    def _downloaddict(self, res):

        for r in res:
            resnew = {'url': r.get('url'), 'id': r.get('id'),
                      'hash': r.get('hash'), 'idx': 0}
            match = re.match(self.partpatt, r['name'])
            if match:
                basnam, idx = match.group(1, 2)
                idx = int(idx)
                resnew.update({'idx': idx})
                if basnam in self.downloaddict:
                    self.downloaddict[basnam].append(resnew)
                else:
                    self.downloaddict[basnam] = [resnew]
            else:
                if r['name'] in self.downloaddict:
                    r['name'] += str(uuid.uuid4())
                self.downloaddict[r['name']] = [resnew]
                
        for k in list(self.downloaddict.keys()):
            v = sorted(self.downloaddict[k], key=lambda x: x['idx'])
            self.downloaddict[k] = v

    def _download(self):

        def existingfile(path, name):
            if os.path.exists(path):
                if not self.yes:
                    answer = input('File {} exists. Overwrite? [Y/N] '
                                       .format(path))
                else:
                    answer = 'yes'
                if answer not in ['y', 'Y', 'yes', 'Yes', 'YES']:
                    print('Skipping download of {}'.format(name))
                    return True
                else:
                    os.remove(path)
                    return False
            

        def dl_part(fout, part):
            r = requests.get(part['url'],
                             headers={'X-CKAN-API-Key': self.conn.apikey})
            instream = io.BytesIO(r.content)
            chunk = True
            sha = hashlib.sha256()
            while chunk:
                chunk = instream.read1(CHUNKSIZE)
                sha.update(chunk)
                fout.write(chunk)
            return(sha.hexdigest())

        def validate_part(digest, part, partbase):
            if digest != part['hash']:
                print('Checksum validation failed for {}.'.format(partbase))
                print(digest)
                print(part['hash'])
                if not self.yes:
                    ans = input('Retry download? [Y/N] ')
                else:
                    return False
                if ans in ['y', 'Y', 'yes', 'Yes', 'YES']:
                    return True
                else:
                    print('Ignoring failed download of {}!'.format(partbase))
                    return False
            else:
                print('Checksum validation for {} passed.'.format(partbase))
                return False
        
        for f_out_base in list(self.downloaddict.keys()):
            f_out = os.path.join(self.directory, f_out_base)
            if existingfile(f_out, f_out_base):
                continue

            with io.open(f_out, mode='ab') as fout:
                idx = 0
                while idx < len(self.downloaddict[f_out_base]):
                    part = self.downloaddict[f_out_base][idx]
                    partbase = os.path.basename(part['url'])
                    print('Downloading {} ...'.format(partbase))
                    digest = dl_part(fout, part)
                    if validate_part(digest, part, partbase) :
                        continue
                    else:
                        idx += 1
      
    def get(self):
        #print vars(self)
        res = self._getresources()
        res = self._filterresources(res)
        print("Pattern: {}".format(self.resources.pattern))
        self._downloaddict(res)
        self._download()
        
# ### END of Get() ##########################################

def del_resources(args):
    pkg_name = args['pkg_name']
    conn = args['connection']
    resources = args['resources']
    try:
        resources = re.compile(resources)
    except:
        print(('It seems "{}" is not a valid regular expression.'
              .format(resources)))
        print('Aborting!')
        sys.exit(1)
    check_package(args)
    pkg = conn.call_action('package_show', {'id': pkg_name}, requests_kwargs={'verify': False})
    allres = [(res['name'], res['id']) for res in pkg['resources']]
    delres = [(r[0], r[1]) for r in allres if re.match(resources, r[0])]
    for r in delres:
        print("DELETING Resources: {}".format(r[0]))
        conn.call_action('resource_delete', {'id': r[1]}, requests_kwargs={'verify': False})

def check_package(args):
    if args['pkg_name'] in list_packages(args):
        return()
    else:
        sys.exit('No modifyable package "{}" found. Aborting.'
                 .format(args['pkg_name']))

def list_packages(args):
    conn = args['connection']
    orgas = conn.call_action('organization_list_for_user',
                             {'permission': 'update_dataset'}, requests_kwargs={'verify': False})
    oids = [o['id'] for o in orgas]
    searchquery = '('+' OR '.join(['owner_org:{}'.format(oid) for oid in oids]) + ')'
    res = conn.call_action('package_search',
                           {'q': searchquery,
                            'include_drafts': True,
                            'rows': 1000,
                            'include_private': True},
                           requests_kwargs={'verify': False})['results']
    pkgs = [p['name'] for p in res]
    return(pkgs)

def main():
    pa = Parser()
    args = pa.parse(sys.argv[1:])
    c = Connection(args).get_connection()
    args.update({'connection': c})

    if args['subcmd'] == 'put':
        put = Put(args)
        put.upload()
    if args['subcmd'] == 'get':
        get = Get(args)
        get.get()
    if args['subcmd'] == 'del':
        del_resources(args)
    if args['subcmd'] == 'list':
        pkgnames = list_packages(args)
        for p in pkgnames:
            print(p)

if __name__ == '__main__':
    main()
