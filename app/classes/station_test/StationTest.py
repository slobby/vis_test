import os
import pathlib
from constants import SOURCE_DESC_DIR
from station.Station import Station


class StationTest:
    station: Station
    task: list[str]

    def __init__(self, name, root_dir=None):
        self.name = name
        self.root_dir = pathlib.Path.joinpath(pathlib.Path.cwd(),
                                              SOURCE_DESC_DIR,
                                              root_dir or name)

    def get_tests_paths(self):
        subdirs_gen = [zip([root]*len(files), files)
                       for root, _, files in os.walk(self.root_dir)]
        t = [list(map(lambda x: os.path.join(*x), item)) for item in d]


# %%
d = [zip([root]*len(files), files) for (root, _, files)
     in os.walk('d:\\Projects\\Python\\vis_test\\stations\\test')]
t = [list(map(lambda x: os.path.join(*x), item)) for item in d]

# print(t)


sum(t, [])


# %%
