from queue import Queue
from threading import Lock, Thread
from os import listdir, makedirs , walk
from os.path import abspath, exists, join
from shutil import copy
from argparse import ArgumentParser
from tqdm import tqdm
from typing import List


class FastCopy:
    file_queue = Queue()
    totalFiles, copy_count = 0, 0
    lock = Lock()
    progress_bar = None

    def __init__(self,
                 src_dir: str,
                 dest_dir: str):

        self.src_dir = abspath(src_dir)
        if not exists(self.src_dir):
            raise ValueError('Error: source directory {} does not exist.'.format(self.src_dir))

        self.dest_dir = abspath(dest_dir)
        if not exists(self.dest_dir):
            print('Destination folder {} does not exist - creating now...'.format(self.dest_dir))
            makedirs(self.dest_dir)

        file_list = [join(root, file) for root, _, files in walk(abspath(self.src_dir)) for file in files]
        self.total_files = len(file_list)
        print("{} files to copy from {} to {}".format(self.total_files,
                                                      self.src_dir,
                                                      self.dest_dir))
        self.dispatch_workers(file_list)

    def single_copy(self):
        while True:
            file = self.file_queue.get()
            copy(file, self.dest_dir)
            self.file_queue.task_done()
            with self.lock:
                self.progress_bar.update(1)

    def dispatch_workers(self,
                         file_list: List[str]):
        n_threads = 14
        for i in range(n_threads):
            t = Thread(target=self.single_copy)
            t.daemon = True
            t.start()
        print('14 copy deamons started.')
        self.progress_bar = tqdm(total=self.total_files)
        for file_name in file_list:
            self.file_queue.put(file_name)
        self.file_queue.join()
        self.progress_bar.close()
        print('{}/{} files copied successfully.'.format(len(listdir(self.dest_dir)),
                                                        self.total_files))


if __name__ == '__main__':
    parser = ArgumentParser(description='Fast multi-threaded copy.')
    parser.add_argument('src_dir',
                        help='Path of the source directory (location to be copy from).')
    parser.add_argument('dest_dir',
                        help='Path of the destination directory (location to copy to).')
    args = parser.parse_args()
    FastCopy(src_dir=args.src_dir,
             dest_dir=args.dest_dir)
