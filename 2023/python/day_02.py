#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path

def parse_draft(cube_pairs):
    draft = defaultdict(int)
    for cnt, color in map(str.split, cube_pairs.split(',')):
        draft[color] = int(cnt)

    return draft


def parse_input(data):
    games = {}
    for line in data.rstrip().split('\n'):
        (game_id, drafts) = line.split(':')
        games[int(game_id[5:])] = [parse_draft(d) for d in drafts.split(';')]

    return games


def draft_is_possible(draft):
    return draft['red'] <= 12 and draft['green'] <= 13 and draft['blue'] <= 14


def power(game):
    min_r = min_g = min_b = 0
    for draft in game:
        min_r = max(min_r, draft['red'])
        min_g = max(min_g, draft['green'])
        min_b = max(min_b, draft['blue'])
    return min_r * min_g * min_b


def part_1(games):
    game_is_possible = lambda gid: all(draft_is_possible(d) for d in games[gid])

    return sum(filter(game_is_possible, games.keys()))


def part_2(games):
    return sum(power(game) for game in games.values())


if __name__ == '__main__':
    test_data = parse_input(Path('../input/day_02_test.txt').read_text())
    game_data = parse_input(Path('../input/day_02.txt').read_text())
    print(part_1(test_data))
    print(part_1(game_data))
    print(part_2(test_data))
    print(part_2(game_data))
