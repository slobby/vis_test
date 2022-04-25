import datetime
import os
import shutil
from app.classes.TCPClient import Clients
from app.classes.TestRowHandler import AbstractTestRowHandler
from app.classes.TestTask import TestTask
from constants import OUTPUT_DIR, SOURCE_DESC_DIR
from colorama import Fore, Style


class StationTest:
    station_name: str
    clients: Clients
    row_handler: AbstractTestRowHandler
    root_dir: str
    tasks_paths: list[str]
    success_paths: list[str]
    fixture_paths: list[str]
    test_tasks: list[TestTask]
    success_tasks: list[TestTask]
    fixture_tasks: list[TestTask]

    def __init__(self,
                 station_name: str,
                 clients: Clients,
                 row_handler: AbstractTestRowHandler,
                 tests_paths=None,
                 success_paths=None,
                 fixture_paths=None) -> None:
        self.station_name = station_name
        self.clients = clients
        self.row_handler = row_handler
        self.root_dir = os.path.join(os.getcwd(),
                                     SOURCE_DESC_DIR,
                                     self.station_name)
        self.tasks_path = self.create_tests_paths(tests_paths)
        self.success_paths = self.create_paths(success_paths)
        self.fixture_paths = self.create_paths(fixture_paths)
        self.test_tasks = self.create_tasks(self.tasks_path)
        self.success_tasks = self.create_tasks(self.success_paths)
        self.fixture_tasks = self.create_tasks(self.fixture_paths)

    def create_tests_paths(self, tests_paths=None) -> list[str]:
        if not tests_paths:
            tests_paths = ['']

        tepm_dir_tests_paths = []
        tepm_tests_paths = []

        for elem_path in tests_paths:
            candidate_path = os.path.join(self.root_dir, elem_path)
            if os.path.isdir(candidate_path):
                tepm_dir_tests_paths.\
                    extend(list(zip([root]*len(files), files))
                           for root, _, files in os.walk(candidate_path))
            else:
                candidate_path += '.csv'
                if os.path.exists(candidate_path):
                    tepm_tests_paths.append(candidate_path)
        if tepm_dir_tests_paths:
            flatten_raw_list = sum(tepm_dir_tests_paths, [])
            tepm_tests_paths.extend(os.path.join(folder, file)
                                    for folder, file in flatten_raw_list
                                    if file.startswith('test'))
        return sorted(tepm_tests_paths)

    def create_paths(self, paths_list=None) -> list[str]:
        if paths_list:
            return list(filter(os.path.exists, [
                os.path.join(self.root_dir, path_list + '.csv')
                for path_list in paths_list]))
        else:
            return list()

    def create_tasks(self, paths_list: list[str]) -> list[TestTask]:
        return [TestTask(t_path, self.station_name, self.row_handler, self.clients)
                for t_path in paths_list]

    def run(self) -> bool:
        self.clear_output_dir()
        success = 0
        result = True
        fixture_result = True
        success_result = True
        print('\n===================== test session stats =====================')
        print(f'station {Fore.CYAN}{Style.BRIGHT}{self.station_name}')
        print(f'{Style.BRIGHT}collected {len(self.test_tasks)} items\n')

        start_time = datetime.datetime.now()
        for test_task in self.test_tasks:
            if not test_task.run():
                result = False
                for fixture_task in self.fixture_tasks:
                    if not fixture_task.run():
                        fixture_result = False
                        break
            else:
                success += 1
                for success_task in self.success_tasks:
                    if not success_task.run():
                        success_result = False
                        break
            if not fixture_result or not success_result:
                break
        elapsed_time = datetime.datetime.now() - start_time
        print(
            f'\n===================== REPORT in {elapsed_time.total_seconds():.2f} sec =====================')
        if success:
            print(f'{Fore.GREEN}PASSED:{success}')
        if (len(self.test_tasks)-success > 0):
            print(f'{Fore.RED}FAILED:{len(self.test_tasks)-success}')
        return result

    def clear_output_dir(self) -> None:
        output_dir = os.path.join(os.getcwd(),
                                  OUTPUT_DIR,
                                  self.station_name)
        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)
