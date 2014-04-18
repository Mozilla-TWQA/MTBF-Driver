#!/usr/bin/python


class StressLevel(object):
    def __init__(self):
        pass

    def setLevel(self, level):
        if level >=0 and level <=5:
            self.level = level

    def importTests(self, manifest):
        pass

    def generate(self):
        # TODO: produce a manifest and return file path
        manifest = '/tmp/manifest.ini'
        return manifest

    def randomizer(self):
        pass
