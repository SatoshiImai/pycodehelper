# coding:utf-8
# ---------------------------------------------------------------------------
# __author__ = 'Satoshi Imai'
# __credits__ = ['Satoshi Imai']
# __version__ = '0.9.0'
# ---------------------------------------------------------------------------

import bz2
import filecmp
import gzip
import os
import shutil
import tempfile
import zipfile
from pathlib import Path


class Bzip2CompareException(Exception):
    pass


class GzipCompareException(Exception):
    pass


class ZipCompareException(Exception):
    pass


class CommonCompression(object):
    def compress(self, compression: str, source_filepath: str,
                 dest_filepath: str):
        if compression == 'bz2':
            self.bz2_compress(source_filepath, dest_filepath)
        elif compression == 'gzip':
            self.gzip_compress(source_filepath, dest_filepath)
        elif compression == 'zip':
            self.zip_compress(source_filepath, dest_filepath)
        else:
            raise NameError(
                f'CommonCompression doesn\'t support compression:{compression}'
            )
            # end if
        # end def

    def extract(self,
                compression: str,
                source_filepath: str,
                dest_filepath: str,
                block_size: int = 65536):
        if compression == 'bz2':
            self.bz2_extract(source_filepath, dest_filepath, block_size)
        elif compression == 'gzip':
            self.gzip_extract(source_filepath, dest_filepath, block_size)
        elif compression == 'zip':
            self.zip_extract(source_filepath, dest_filepath)
        else:
            raise NameError(
                f'CommonCompression doesn\'t support compression:{compression}'
            )
            # end def
        # end def

    def bz2_extract(self,
                    source_filepath: str,
                    dest_filepath: str,
                    block_size: int = 65536):

        if not isinstance(source_filepath, str):
            source_filepath = str(source_filepath)
            # end if
        if not isinstance(dest_filepath, str):
            dest_filepath = str(dest_filepath)
            # end if

        with bz2.open(source_filepath, 'rb') as s_file, \
                open(dest_filepath, 'wb') as d_file:
            while True:
                block = s_file.read(block_size)
                if not block:
                    break
                else:
                    d_file.write(block)
                    # end if
                # end while
            d_file.write(block)
            # end with
        # end def

    def bz2_compress(self, source_filepath: str, dest_filepath: str):

        if not isinstance(source_filepath, str):
            source_filepath = str(source_filepath)
            # end if
        if not isinstance(dest_filepath, str):
            dest_filepath = str(dest_filepath)
            # end if

        with open(source_filepath, 'rb') as f_in:
            with bz2.open(dest_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                # end with
            # end with

        test_path = source_filepath.replace('.', '_test.')
        self.bz2_extract(dest_filepath, test_path)
        if filecmp.cmp(source_filepath, test_path):
            os.remove(test_path)
        else:
            raise Bzip2CompareException(f'compress error:{source_filepath}')
            # end if
        # end def

    def gzip_extract(self,
                     source_filepath: str,
                     dest_filepath: str,
                     block_size: int = 65536):

        if not isinstance(source_filepath, str):
            source_filepath = str(source_filepath)
            # end if
        if not isinstance(dest_filepath, str):
            dest_filepath = str(dest_filepath)
            # end if

        with gzip.open(source_filepath, 'rb') as s_file, \
                open(dest_filepath, 'wb') as d_file:
            while True:
                block = s_file.read(block_size)
                if not block:
                    break
                else:
                    d_file.write(block)
                    # end if
                # end while
            d_file.write(block)
            # end with
        # end def

    def gzip_compress(self, source_filepath: str, dest_filepath: str):

        if not isinstance(source_filepath, str):
            source_filepath = str(source_filepath)
            # end if
        if not isinstance(dest_filepath, str):
            dest_filepath = str(dest_filepath)
            # end if

        with open(source_filepath, 'rb') as f_in:
            with gzip.open(dest_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                # end with
            # end with

        test_path = source_filepath.replace('.', '_test.')
        self.gzip_extract(dest_filepath, test_path)
        if filecmp.cmp(source_filepath, test_path):
            os.remove(test_path)
        else:
            raise Bzip2CompareException(f'compress error:{source_filepath}')
            # end if
        # end def

    def zip_extract(self, source_filepath: str, dest_filepath: str):

        if not isinstance(source_filepath, str):
            source_filepath = str(source_filepath)
            # end if
        if not isinstance(dest_filepath, str):
            dest_filepath = str(dest_filepath)
            # end if

        tempDir = Path(tempfile.mkdtemp())

        with zipfile.ZipFile(source_filepath, 'r') as zf:
            extractKey = zf.namelist()[0]
            zf.extract(extractKey, str(tempDir))
            # end with

        shutil.move(tempDir.joinpath(extractKey), dest_filepath)
        # end def

    def zip_extract_all(self, source_filepath: str, extractTo: str):

        if not isinstance(source_filepath, str):
            source_filepath = str(source_filepath)
            # end if
        if not isinstance(extractTo, str):
            extractTo = str(extractTo)
            # end if

        with zipfile.ZipFile(source_filepath, 'r') as zf:
            zf.extractall(extractTo)
            # end with
        # end def

    def zip_compress(self, source_filepath: str, dest_filepath: str):

        if not isinstance(source_filepath, str):
            source_filepath = str(source_filepath)
            # end if
        if not isinstance(dest_filepath, str):
            dest_filepath = str(dest_filepath)
            # end if

        fileName = Path(source_filepath).name
        with zipfile.ZipFile(dest_filepath, 'w') as zf:
            zf.write(source_filepath, arcname=fileName)
            # end with

        test_path = Path(source_filepath.replace('.', '_test.'))
        self.zip_extract(dest_filepath, test_path)
        if filecmp.cmp(source_filepath, test_path):
            os.remove(test_path)
        else:
            raise ZipCompareException(f'compress error:{source_filepath}')
            # end if
        # end def

    def zip_compress_all(self, source_dir: str, dest_filepath: str):

        if not isinstance(source_dir, str):
            source_dir = str(source_dir)
            # end if
        if not isinstance(dest_filepath, str):
            dest_filepath = str(dest_filepath)
            # end if

        with zipfile.ZipFile(dest_filepath, 'w') as zf:
            for root, dirs, files in os.walk(source_dir):
                root = Path(root)
                for file in files:
                    zf.write(root.joinpath(file), arcname=file)
                    # end for
                # end for
            # end with
        # end def

    # end class
