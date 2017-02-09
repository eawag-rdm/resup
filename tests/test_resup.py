# _*_ coding: utf-8 _*_

# Just started unit-testing very late ...

import os
import sys
import glob
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from resup import resup

class TestResup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datadir = os.path.join(os.path.dirname(__file__), 'data')

    @classmethod
    def mkdummyput(cls, arglist):
        pa = resup.Parser()
        args = pa.parse(arglist)
        args.update({'connection': 'dummy'})
        return resup.Put(args)

    def test_put_regex(self):
        arglist = ['put', 'pkgname', self.datadir]
        put = self.mkdummyput(arglist)
        #print(glob.glob(os.path.join(self.datadir, '*')))
        self.assertItemsEqual(
            put.metadata.keys(),
            glob.glob(os.path.join(self.datadir, '*')))
        
        arglist = ['put', 'pkgname', self.datadir,
                   '.*taa.*|.*\.ico|.*git.*']
        put = self.mkdummyput(arglist)
        self.assertItemsEqual(
            put.metadata.keys(),
            (glob.glob(os.path.join(self.datadir, '*taa*'))
             + glob.glob(os.path.join(self.datadir, '*.ico')))
        )
    def test_chksum(self):
        testfile = os.path.join(self.datadir, 'chksumtest.txt')
        arglist = ['put', '--chksum', 'False', 'pkgname',
                   self.datadir, 'chksumtest.txt']
        put = self.mkdummyput(arglist)
        if put.chksum.lower() != 'false':
            put._chksum(put.chksum)
        self.assertNotIn('hash', put.metadata[testfile])
        arglist = ['put', '--chksum', 'sha1', 'pkgname',
                   self.datadir, 'chksumtest.txt']
        put = self.mkdummyput(arglist)
        if put.chksum.lower() != 'false':
            put._chksum(put.chksum)
        self.assertEqual('3d7b54f1882fa975c8fc839c8d0374f692992136',
                         put.metadata[testfile]['hash'])
        arglist = ['put', '--chksum', 'sha256', 'pkgname',
                   self.datadir, 'chksumtest.txt']
        put = self.mkdummyput(arglist)
        if put.chksum.lower() != 'false':
            put._chksum(put.chksum)
        self.assertEqual('160b74c51fd702609cbaa6bd7bbcc8ff51e5f4e426eccba5f45051ad33e0ad15',
                         put.metadata[testfile]['hash'])
        arglist = ['put', 'pkgname',
                   self.datadir, 'chksumtest.txt']
        put = self.mkdummyput(arglist)
        if put.chksum.lower() != 'false':
            put._chksum(put.chksum)
        self.assertEqual('3d7b54f1882fa975c8fc839c8d0374f692992136',
                         put.metadata[testfile]['hash'])
   
        



