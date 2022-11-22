import logging
import pdb

from sss_log import setup_log
setup_log()
from enum import Enum
import os
import stat
from typing import Optional
import pickle
from sss_db import DataBase
import glob
import unittest
import wave
import os

# Some diffing algos
# https://stackoverflow.com/questions/1471153/string-similarity-metrics-in-python
import difflib

class IndexTree:
    index_tree = {}
    def add_file(self, path, data=None):
        path = os.path.normpath(path)
        splits = path.split(os.sep)

        iter = self.index_tree
        for s in splits:
            iter[s] = None
            iter = iter[s]

        if os.path.isdir(path):
            iter = {}
        elif os.path.isfile(path):
            iter = data

# FileIndexer pickled objects are used as application 'project' files
class FileIndexer:
    def __init__(self, library_path="index.db"):
        # index glob is used for diffing between the app filesystem ans os filesystem
        self.index_glob = None
        self.library = library_path

        self.db = DataBase(library_path)
        self.index_tree = IndexTree()

    # Add all the files we run into the DB and PROJ file
    def index(self, start_dir):
        logging.debug("Starting File Indexing (.wav) ...")
        self.index_glob = glob.glob("{}/**/*.wav".format(start_dir), recursive=True)

        for file in self.index_glob:
            self.db.add_file(file)
            logging.debug("Parsing {} ...".format(file))
            print(file)
            wavfile = wave.open(file, mode="rb")

            params = wavfile.getparams()
            # NEVER read in audio data in the indexer
            data = {
                "channels": params[0],
                "sample_width": params[1],
                "frames": params[3],
                "framerate": params[2],
                "audio_data": None,
            }

            self.index_tree.add_file(file, data=data)
        self.dump()

        logging.debug("Finished Indexing")

    # Similar to index() but also remove files
    def refresh(self, start_dir):
        logging.debug("Refreshing file index...")
        old_glob = self.index_glob
        new_glob = self.index_glob = glob.glob("{}/**/*.wav".format(start_dir), recursive=True)

        logging.debug("Diffing indicies...")
        new_files = new_glob - old_glob
        old_files = old_glob - new_glob

        logging.debug("Updating file index...")
        for f in new_files:
            self.db.add_file(f)

        for f in old_files:
            self.db.rem_file(f)
        logging.debug("Finished refreshing file index...")

    def dump(self):
        logging.debug("Dumping File Index...")
        pickle.dump(self, self.library)
        logging.debug("Finished Dumping File Index")

    def load(self):
        logging.debug("Loading File Index...")
        self.index_glob = pickle.load(self.library)
        logging.debug("Finished Loading File Index")

    def search_tags(self):
        self.tags = self.db.get_tags()
        pdb.set_trace()

    def search_files(self):
        pass


class IndexTest(unittest.TestCase):
    def test_index(self):
        fs = FileIndexer(library_path="test.db")
        fs.index("./tests")
        fs.refresh("./test")
        pass

    def test_dump(self):
        pass

    def test_load(self):
        pass
    def test_refresh(self):
        pass
    def test_search_tags(self):
        pass
    def test_search_files(self):
        pass

if __name__ == '__main__':
    import os
    unittest.main()
    os.remove("test.db")

