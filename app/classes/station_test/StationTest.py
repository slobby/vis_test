import os
from app.classes.TCPClient import TCPClient
from app.classes.test_task.VisTestTask import TestTask, VisTestTask
from constants import SOURCE_DESC_DIR
from app.classes.station.Station import Station
from colorama import Fore, Style


class StationTest:
    station: Station
    tasks_path: list[str]
    test_tasks: list[TestTask]
    fixtures_tasks: list[TestTask]

    def __init__(self,
                 station: Station,
                 client: TCPClient,
                 tests_paths=None,
                 fixtures_paths=None) -> None:
        self.station = station
        self.client = client
        self.name = station.name
        self.root_dir = os.path.join(os.getcwd(),
                                     SOURCE_DESC_DIR,
                                     self.name)
        self.tasks_path = self.create_tests_paths(tests_paths)
        self.fixtures_paths = self.create_fixtures_paths(fixtures_paths)
        self.test_tasks = self.create_tasks()
        self.fixtures_tasks = self.create_fixtures()

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
        # else:
        #     raw_list = [list(zip([root]*len(files), files))
        #                 for root, _, files in os.walk(self.root_dir)]
        #     flatten_raw_list = sum(raw_list, [])
        #     return sorted([os.path.join(folder, file)
        #                    for folder, file in flatten_raw_list
        #                    if file.startswith('test')])

    def create_fixtures_paths(self, fixtures_paths=None) -> list[str]:
        if fixtures_paths:
            return list(filter(os.path.exists, [
                os.path.join(self.root_dir, test_path + '.csv')
                for test_path in fixtures_paths]))
        else:
            return list()

    def create_tasks(self) -> list[TestTask]:
        return [VisTestTask(task_path, self.station, self.client)
                for task_path in self.tasks_path]

    def create_fixtures(self) -> list[TestTask]:
        return [VisTestTask(task_path, self.station, self.client)
                for task_path in self.fixtures_paths]

    def run(self) -> bool:
        success = 0
        result = True
        fixture_result = True
        print('\n============== test session stats ==============')
        print(f'station {Fore.CYAN}{Style.BRIGHT}{self.name}')
        print(f'{Style.BRIGHT}collected {len(self.test_tasks)} items\n')

        for test_task in self.test_tasks:
            if not test_task.run():
                result = False
                for fixture_task in self.fixtures_tasks:
                    if not fixture_task.run():
                        fixture_result = False
                        break
            else:
                success += 1
            if not fixture_result:
                break
        print('\n===================== REPORT ===================')
        if success:
            print(f'{Fore.GREEN}PASSED:{success}')
        if (len(self.test_tasks)-success > 0):
            print(f'{Fore.RED}FAILED:{len(self.test_tasks)-success}')
        return result
