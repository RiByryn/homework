import json

import pandas as pd
import requests as requests


class StandingsItem:
    def __init__(self, team):
        self.team = team
        self.matches = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.points = 0
        self.sums = 0

    def __str__(self):
        return f'{self.team}: {self.matches} matches, {self.wins}-{self.draws}-{self.losses}, {self.sums} game pts, {self.points} pts'


class Match:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.score1 = 0
        self.score2 = 0

    def calculate_score(
            self,
            raw_results_1: dict,
            raw_results_2: dict,
            standings_item1: StandingsItem,
            standings_item2: StandingsItem,
    ):
        standings_item1.matches += 1
        standings_item2.matches += 1
        if len(raw_results_1) != 8 and len(raw_results_2) != 8:
            standings_item1.losses += 1
            standings_item2.losses += 1
            return
        if len(raw_results_1) != 8 and len(raw_results_2) == 8:
            self.score2 = 7
            standings_item1.losses += 1
            standings_item2.wins += 1
            standings_item2.points += 2
            standings_item2.sums += raw_results_2['Очки']
            return
        if len(raw_results_1) == 8 and len(raw_results_2) != 8:
            self.score1 = 7
            standings_item1.wins += 1
            standings_item1.points += 2
            standings_item1.sums += raw_results_1['Очки']
            standings_item2.losses += 1
            return

        round_names = list(filter(lambda x: x != 'Очки', raw_results_1.keys()))
        for round_name in round_names:
            if raw_results_1[round_name] > raw_results_2[round_name]:
                self.score1 += 1
            elif raw_results_1[round_name] < raw_results_2[round_name]:
                self.score2 += 1

        standings_item1.sums += raw_results_1['Очки']
        standings_item2.sums += raw_results_2['Очки']

        if self.score1 == self.score2:
            standings_item1.draws += 1
            standings_item2.draws += 1
            standings_item1.points += 1
            standings_item2.points += 1
        elif self.score1 > self.score2:
            standings_item1.wins += 1
            standings_item2.losses += 1
            standings_item1.points += 2
        elif self.score1 < self.score2:
            standings_item1.losses += 1
            standings_item2.wins += 1
            standings_item2.points += 2


class Tournament:
    num_groups: int
    num_teams: int

    def __init__(self, num_groups, num_teams):
        self.calendar = None
        self.bracket = None
        self.teams = None
        self.standings = None
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
            self.standings = list(map(lambda group: list(map(lambda team: StandingsItem(team), group)), result))
            self.teams = result

    def read_data_from_table(self, tour):
        data = pd.read_excel('Tablitsa.xls', f'Игра №{tour}', usecols=[2, 6, 7, 8, 9, 10, 11, 12, 16], skiprows=2)
        data_dropna = data.dropna()
        print(data_dropna)
        game_result_by_team = data_dropna.set_index('КОМАНДА').to_dict(orient='index')
        return game_result_by_team

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
                    tour_list.append(
                        Match(group_teams[match[0] - 1], group_teams[match[1] - 1])
                    )
                group.append(tour_list)
            bracket.append(group)
        self.bracket = bracket

    def play_and_print(self, results):
        for group_idx, group in enumerate(self.bracket):
            print(f'Группа {chr(ord("A") + group_idx)}: \n')
            for tour_idx, tour in enumerate(group):
                print(f'Тур {tour_idx + 1}:\n')
                for match in tour:
                    standings_item1 = list(filter(lambda item: item.team == match.team1, self.standings[group_idx]))[0]
                    standings_item2 = list(filter(lambda item: item.team == match.team2, self.standings[group_idx]))[0]
                    match.calculate_score(
                        results[tour_idx + 1].get(match.team1, {}),
                        results[tour_idx + 1].get(match.team2, {}),
                        standings_item1,
                        standings_item2
                    )
                    print(f'{match.team1} VS {match.team2}: {match.score1}-{match.score2}')
        self.print_standings()

    def print_standings(self):
        for group_standings in self.standings:
            print()
            for standings_item in group_standings:
                print(standings_item)
        print()


tournament = Tournament(num_groups=2, num_teams=8)
tournament.read_teams_from_file('teams.txt')
tournament.get_calendar()
tournament.generate_bracket()
all_results = {}
for i in range(1, 11):
    result_table = tournament.read_data_from_table(i)
    all_results[i] = result_table
print(all_results)
tournament.play_and_print(all_results)
# tour_results = tournament.score_all_tours(all_results)

#Нахуевертить счета, опираясь на эксель-табличку. Взять results.csv. Замаппить результаты матчей на сетку. Результат: "команда VS команда: 5:3"
#Работа с классами, вызов методов с разными переменными. быть проще.