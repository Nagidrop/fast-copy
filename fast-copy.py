from queue import Queue
from threading import Lock, Thread
from os import listdir, makedirs , walk
from os.path import abspath, exists, join
from shutil import copy
from argparse import ArgumentParser
from tqdm import tqdm
from typing import List


class FastCopy:
    file_queue, totalFiles, copy_count, lock, progress_bar = Queue(), 0, 0, Lock(), None

    def __init__(self,
                 src_dir: str,
                 dest_dir: str):

        self.src_dir = abspath(src_dir)
        if not exists(self.src_dir):
            raise ValueError(f'Error: source directory {self.src_dir} does not exist.')

        self.dest_dir = abspath(dest_dir)
        if not exists(self.dest_dir):
            print(f'Destination folder {self.dest_dir} does not exist - creating now...')
            makedirs(self.dest_dir)

        file_list = [join(root, file) for root, _, files in walk(abspath(self.src_dir)) for file in files]
        self.total_files = len(file_list)
        print(f'{self.total_files} files to copy from {self.src_dir} to {self.dest_dir}')
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
        n_threads = 15
        for i in range(n_threads):
            t = Thread(target=self.single_copy)
            t.daemon = True
            t.start()
        print(f'{n_threads} copy deamons started.')
        self.progress_bar = tqdm(total=self.total_files)
        [self.file_queue.put(file_name) for file_name in file_list]
        self.file_queue.join()
        self.progress_bar.close()
        copied_files = sum([len(files) for root, dirs, files in walk(self.dest_dir)])
        print(f'{copied_files}/{self.total_files} files copied successfully.')


if __name__ == '__main__':
    parser = ArgumentParser(description='Fast multi-threaded copy.')
    parser.add_argument('src_dir',
                        help='Path of the source directory (location to be copy from).')
    parser.add_argument('dest_dir',
                        help='Path of the destination directory (location to copy to).')
    args = parser.parse_args()
    FastCopy(src_dir=args.src_dir,
             dest_dir=args.dest_dir)
