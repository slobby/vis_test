import os
import pathlib
from app.classes.client import send_and_recieve
from app.classes.test_task.TestTask import TestTask
from constants import SOURCE_DESC_DIR
from app.classes.station.Station import Station


class StationTest:
    station: Station
    tasks_path: list[str]
    tasks: list[TestTask]

    def __init__(self, name, root_dir=None) -> None:
        self.name = name
        self.station = Station(name)
        self.root_dir = pathlib.Path.joinpath(pathlib.Path.cwd(),
                                              SOURCE_DESC_DIR,
                                              root_dir or name)
        self.tasks_path = self.create_tests_paths()
        self.test_tasks = self.create_tasks()

    def create_tests_paths(self) -> None:
        raw_list = [list(zip([root]*len(files), files))
                    for root, _, files in os.walk(self.root_dir)]
        flatten_raw_list = sum(raw_list, [])
        return [os.path.join(folder, file)
                for folder, file in flatten_raw_list
                if file.startswith('test')]

    def create_tasks(self) -> None:
        return [TestTask(task_path, self.station)
                for task_path in self.tasks_path]

    def run(self) -> None:
        for test_task in self.test_tasks:
            test_task.run(send_and_recieve)
