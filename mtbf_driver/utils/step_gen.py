#!/usr/bin/python
import os
import random
import json
import shutil


class StepGen(object):
    def __init__(self, level=1, root=None, runlist=None, workspace=None):
        self.max_level = 5
        self.dummy = ('test_dummy_case.py', 'tests/test_dummy_case.py')
        self.setLevel(level)
        self.setRunlist(runlist)
        self.setWorkspace(workspace)
        self.enqueue = []
        if(root):
            self.setRoot(root)
            self.loadFiles(root)

    def setLevel(self, level):
        '''
        level 0: No test but dummy
        level 1: One test and then dummy
        level 2: Two tests paired with one dummy
        level 3: Three tests
        level 4: Four tests
        level 5: No dummy cases
        '''
        if level >= 0 and level <= self.max_level:
            self.level = level

    def setRoot(self, root):
        self.root = root

    def setWorkspace(self, workspace):
        self.workspace = workspace
        if not os.path.exists(workspace):
            os.mkdir(workspace)

    def setRunlist(self, runlist):
        with open(runlist) as fh:
            self.runlist = json.load(fh)['runlist']

    def loadFiles(self, root):
        to_run = set(self.runlist)
        uniq = set()
        for dir_path, dir_name, file_path in os.walk(root):
            for fp in file_path:
                full_path = os.path.join(dir_path, fp)
                if 'pyc' not in fp and fp in to_run and fp not in uniq:
                    uniq.add(fp)
                    shutil.copy2(full_path, self.workspace)
                    self.enqueue.append((fp, full_path))
                else:
                    print("possibly duplicated? : " + full_path)
            if len(self.enqueue) == 0:
                raise ValueError("0 file in runlist is matched, root dir: ", root)

    def generate(self):
        '''
        from run list, randomly pick up test cases
        and return a list, write to file at the same time
        '''
        li = []
        for i in range(0, self.level):
            li.append(self.enqueue[random.randint(0, len(self.enqueue) - 1)])
        if self.level != self.max_level:
            pos = random.randint(0, self.level)
            li.insert(pos, self.dummy)
        return li


def main():
    run_file = 'tests/test_run.txt'
    sg = StepGen(level=3, root='/tmp/run_test', workspace='/tmp/replay', runlist=run_file)
    print('enqueue : ', sg.enqueue)
    import time
    while(True):
        time.sleep(1)
        print(sg.generate())

if __name__ == '__main__':
    main()
