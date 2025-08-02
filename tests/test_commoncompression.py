"""
    __author__ = 'Satoshi Imai'
    __credits__ = ['Satoshi Imai']
    __version__ = '0.9.0'
"""

import logging
import shutil
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from src.pycodehelper.compression import CommonCompression

thisEncoding = 'utf-8'
newLine = '\n'


@pytest.fixture(scope='module')
def logger() -> logging.Logger:
    log = logging.getLogger(__name__)

    yield log
    # end def


@pytest.fixture(scope='module')
def tempdir() -> Path:

    tempdir = Path(tempfile.mkdtemp())
    yield tempdir
    if tempdir.exists():
        shutil.rmtree(tempdir)
        # end if
    # end def


@pytest.fixture(scope='module')
def test_df() -> pd.DataFrame:
    return pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                        columns=['columnA', 'columnB', 'columnC'])
    # end def


def test_xz(test_df: pd.DataFrame, tempdir: Path, logger: logging.Logger):
    compressor = CommonCompression()

    compression = 'xz'

    raw_source = tempdir.joinpath('compression_test.csv')
    comp_source = tempdir.joinpath('compression_test.csv.xz')
    rev_source = tempdir.joinpath('compression_rev.csv')
    test_df.to_csv(raw_source, index=False, header=True)

    logger.info('test compress')
    with pytest.raises(NameError):
        compressor.compress(compression, raw_source, comp_source)
        # end with

    logger.info('test extract')

    test_df.to_csv(
        comp_source,
        compression=compression,
        index=False,
        header=True)
    with pytest.raises(NameError):
        compressor.extract(compression, comp_source, rev_source)
        # end with
    # end def


def test_bzip2(test_df: pd.DataFrame, tempdir: Path, logger: logging.Logger):
    compressor = CommonCompression()

    compression = 'bz2'

    raw_source = tempdir.joinpath('compression_test.csv')
    comp_source = tempdir.joinpath('compression_test.csv.bz2')
    rev_source = tempdir.joinpath('compression_rev.csv')
    test_df.to_csv(raw_source, index=False, header=True)

    logger.info('test compress')
    compressor.compress(compression, raw_source, comp_source)
    comp_df = pd.read_csv(comp_source, compression=compression)
    assert len(test_df.compare(comp_df)) == 0

    logger.info('test extract')
    compressor.extract(compression, comp_source, rev_source)
    rev_df = pd.read_csv(rev_source)
    assert len(test_df.compare(rev_df)) == 0
    # end def


def test_gzip(test_df: pd.DataFrame, tempdir: Path, logger: logging.Logger):
    compressor = CommonCompression()

    compression = 'gzip'

    raw_source = tempdir.joinpath('compression_test.csv')
    comp_source = tempdir.joinpath('compression_test.csv.gz')
    rev_source = tempdir.joinpath('compression_rev.csv')
    test_df.to_csv(raw_source, index=False, header=True)

    logger.info('test compress')
    compressor.compress(compression, raw_source, comp_source)
    comp_df = pd.read_csv(comp_source, compression=compression)
    assert len(test_df.compare(comp_df)) == 0

    logger.info('test extract')
    compressor.extract(compression, comp_source, rev_source)
    rev_df = pd.read_csv(rev_source)
    assert len(test_df.compare(rev_df)) == 0
    # end def


def test_zip(test_df: pd.DataFrame, tempdir: Path, logger: logging.Logger):
    compressor = CommonCompression()

    compression = 'zip'

    raw_source = tempdir.joinpath('compression_test.csv')
    comp_source = tempdir.joinpath('compression_test.csv.zip')
    rev_source = tempdir.joinpath('compression_rev.csv')
    test_df.to_csv(raw_source, index=False, header=True)

    logger.info('test compress')
    compressor.compress(compression, raw_source, comp_source)
    comp_df = pd.read_csv(comp_source, compression=compression)
    assert len(test_df.compare(comp_df)) == 0

    logger.info('test extract')
    compressor.extract(compression, comp_source, rev_source)
    rev_df = pd.read_csv(rev_source)
    assert len(test_df.compare(rev_df)) == 0
    # end def


def test_zip_all(test_df: pd.DataFrame, tempdir: Path, logger: logging.Logger):
    compressor = CommonCompression()

    raw_path = tempdir.joinpath('test')
    raw_path.mkdir()
    raw_source1 = raw_path.joinpath('compression_test1.csv')
    raw_source2 = raw_path.joinpath('compression_test2.csv')
    raw_source3 = raw_path.joinpath('compression_test3.csv')
    comp_source = tempdir.joinpath('compression_test.zip')
    rev_source = tempdir.joinpath('rev')
    test_df.to_csv(raw_source1, index=False, header=True)
    test_df.to_csv(raw_source2, index=False, header=True)
    test_df.to_csv(raw_source3, index=False, header=True)

    logger.info('test compress')
    compressor.zip_compress_all(raw_path, comp_source)

    logger.info('test extract')
    compressor.zip_extract_all(comp_source, rev_source)
    rev1_df = pd.read_csv(rev_source.joinpath(raw_source1.name))
    rev2_df = pd.read_csv(rev_source.joinpath(raw_source2.name))
    rev3_df = pd.read_csv(rev_source.joinpath(raw_source3.name))
    assert len(test_df.compare(rev1_df)) == 0
    assert len(test_df.compare(rev2_df)) == 0
    assert len(test_df.compare(rev3_df)) == 0
    # end def
