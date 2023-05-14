import json
from dataclasses import dataclass

import requests as requests
import pandas as pd


class Tournament:
    num_groups: int
    num_teams: int

    def __init__(self, num_groups, num_teams):
        self.calendar = None
        self.teams = None
        self.num_groups = num_groups
        self.num_teams = num_teams

    def read_teams_from_file(self, filename: str):
        with open(filename, mode='r', encoding="utf-8") as f:
            teams = [line.strip("\n") for line in f.readlines()]
            result = []
            for step_id in range(self.num_teams):
                min_team_id = step_id * self.num_groups
                max_team_id = (step_id + 1) * self.num_groups
                step = teams[min_team_id:max_team_id]
                if step_id % 2 == 1:
                    step.reverse()
                result.append(step)
            result = [list(i) for i in zip(*result)]
            self.teams = result

    def read_data_from_table(self, tour):
        data = pd.read_excel('Tablitsa.xls', f'Игра №{tour}', usecols=[2, 6, 7, 8, 9, 10, 11, 12, 16], skiprows=2)
        data_dropna = data.dropna()
        print(data_dropna)
        dict_of_dicts = data_dropna.set_index('КОМАНДА').to_dict(orient='index')
        return dict_of_dicts

    def get_calendar(self):
        url = f'https://functions.yandexcloud.net/d4e33p918nvbcrhoadtg?tours={self.num_teams}'
        resp = requests.get(url)
        if resp.status_code != 200:
            error_text = json.loads(resp.text)['error']
            raise Exception(f'Fail to get data from server, code = {resp.status_code}, error = {error_text}')
        data = json.loads(resp.text)
        if 'tours' in data:
            calendar = data['tours']
        else:
            raise KeyError('Tours not found in response')
        self.calendar = calendar

    def generate_bracket(self):
        if self.calendar is None or self.teams is None:
            raise Exception('Groups data is not initialized')
        bracket = []
        for group_teams in self.teams:
            group = []
            for tour in self.calendar:
                tour_list = []
                for match in tour:
                    tour_list.append((group_teams[match[0] - 1], group_teams[match[1] - 1]))
                group.append(tour_list)
            bracket.append(group)
        return bracket

    def score_all_tours(self, bracket_tour, all_results):
        bracket = []
        for group_teams in self.teams:
            group = []
            for tour in self.calendar:
                tour_list = []
                for match in tour:
                    team_1 = group_teams[match[0] - 1]
                    team_2 = group_teams[match[1] - 1]
                    tour_list.append(
                        team_1,
                        team_2,
                        self.score_match_result(
                            team_1,
                            team_2,
                            self.calendar.index(tour),
                            all_results[tour][team_1],
                            all_results[tour][team_2],
                        )
                    )
                    group.append(tour_list)
            bracket.append(group)
        return bracket

    def score_match_result(self, result_team_1, result_team_2):


tournament = Tournament(num_groups=2, num_teams=8)
tournament.read_teams_from_file('teams.txt')
tournament.get_calendar()
bracket_tour = tournament.generate_bracket()
print(bracket_tour)
all_results = {}
for i in range(1, 11):
    result_table = tournament.read_data_from_table(i)
    all_results.update({i: result_table})
print(all_results)
for idx, group in enumerate(bracket_tour):
    print(f'Группа {chr(ord("A") + idx)}: \n')
    for tour_idx, tour in enumerate(group):
        print(f'Тур {tour_idx + 1}:\n')
        for match in tour:
            print(f'{match[0]} VS {match[1]}')
        print()
tour_results = tournament.score_all_tours(bracket_tour, all_results)
for idx, group in enumerate(tour_results):
    print(f'Группа {chr(ord("A") + idx)}: \n')
    for tour_idx, tour in enumerate(group):
        print(f'Тур {tour_idx + 1}:\n')
        for match in tour:
            print(f'{match[0]} {match[2]} {match[1]}')
        print()
#Нахуевертить счета, опираясь на эксель-табличку. Взять results.csv. Замаппить результаты матчей на сетку. Результат: "команда VS команда: 5:3"
#Работа с классами, вызов методов с разными переменными. быть проще.