from csv import reader, DictWriter

player_csv = 'players.csv'
goalies_csv = 'goalies.csv'

players_points = {
    'G': 3,
    'A': 2,
    '+/-': 1,
    'PIM': 0.5,
    'S': 0.4,
    'HIT': 0.5
}

goalies_points = {
    'W': 1,
    'GA': -1,
    'SV': 0.4,
    'SO': 3
}


def get_player_stats():
    players = []
    with open(player_csv, 'r') as csvfile:
        player_reader = reader(csvfile, delimiter=',')
        last = '0'
        for row in player_reader:
            if row[0] == 'Rk':
                continue
            if not last == row[0]:
                players.append(
                    {
                        'Player': row[1].split('\\')[0],
                        'Age': row[2],
                        'Pos': row[3],
                        'Tm': row[4],
                        'GP': int(row[5]),
                        'G': int(row[6]),
                        'A': int(row[7]),
                        '+/-': int(row[9]),
                        'PIM': int(row[10]),
                        'PPP': int(row[12]) + int(row[16]),
                        'S': int(row[18]),
                        'ATOI': row[21],
                        'HIT': int(row[23]),
                    }
                )
            else:
                players[-1]['GP'] += int(row[5])
                players[-1]['G'] += int(row[6])
                players[-1]['A'] += int(row[7])
                players[-1]['+/-'] += int(row[9])
                players[-1]['PIM'] += int(row[10])
                players[-1]['PPP'] += int(row[12]) + int(row[16])
                players[-1]['S'] += int(row[18])
                players[-1]['ATOI'] += int(row[21])
                players[-1]['HIT'] += int(row[23])
            last = row[0]

    for row in players:
        row['FP'] = (
            row['G'] * players_points['G'] +
            row['A'] * players_points['A'] +
            row['+/-'] * players_points['+/-'] +
            row['PIM'] * players_points['PIM'] +
            row['S'] * players_points['S'] +
            row['HIT'] * players_points['HIT']
        )
        row['FP'] = round(row['FP'], 2)

    return sorted(players, key=lambda k: k['FP'], reverse=True)


def get_goalie_stats():
    goalies = []
    with open(goalies_csv, 'r') as csvfile:
        goalies_reader = reader(csvfile, delimiter=',')
        last = '0'
        for row in goalies_reader:
            if row[0] == 'Rk':
                continue
            if not last == row[0]:
                goalies.append(
                    {
                        'Player': row[1].split('\\')[0],
                        'Age': row[2],
                        'Pos': 'G',
                        'Tm': row[3],
                        'GP': int(row[4]),
                        'W': int(row[6]),
                        'GA': int(row[9]),
                        'SV': int(row[11]),
                        'SO': int(row[14]),
                        'MIN': int(row[16])
                    }
                )
            else:
                goalies[-1]['GP'] += int(row[4])
                goalies[-1]['W'] += int(row[6])
                goalies[-1]['GA'] += int(row[9])
                goalies[-1]['SV'] += int(row[11])
                goalies[-1]['SO'] += int(row[14])
                goalies[-1]['MIN'] += int(row[16])
            last = row[0]

    for row in goalies:
        row['FP'] = (
                row['W'] * goalies_points['W'] +
                row['GA'] * goalies_points['GA'] +
                row['SV'] * goalies_points['SV'] +
                row['SO'] * goalies_points['SO']
        )
        row['FP'] = round(row['FP'], 2)

    return sorted(goalies, key=lambda k: k['FP'], reverse=True)


def create_csvs():
    goalies = get_goalie_stats()
    with open('output\\goalies.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Age', 'Pos', 'Tm', 'GP', 'W', 'GA', 'SV', 'SO', 'MIN', 'FP']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for goalie in goalies:
            writer.writerow(goalie)

    players = get_player_stats()
    with open('output\\right_wing.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Age', 'Pos', 'Tm', 'GP', 'G', 'A', '+/-', 'PIM', 'PPP', 'S', 'ATOI', 'HIT', 'FP']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player in players:
            if not player['Pos'] == 'RW':
                continue
            writer.writerow(player)

    players = get_player_stats()
    with open('output\\left_wing.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Age', 'Pos', 'Tm', 'GP', 'G', 'A', '+/-', 'PIM', 'PPP', 'S', 'ATOI', 'HIT', 'FP']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player in players:
            if not player['Pos'] == 'LW':
                continue
            writer.writerow(player)

    players = get_player_stats()
    with open('output\\center.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Age', 'Pos', 'Tm', 'GP', 'G', 'A', '+/-', 'PIM', 'PPP', 'S', 'ATOI', 'HIT', 'FP']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player in players:
            if not player['Pos'] == 'C':
                continue
            writer.writerow(player)

    players = get_player_stats()
    with open('output\\defense.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Age', 'Pos', 'Tm', 'GP', 'G', 'A', '+/-', 'PIM', 'PPP', 'S', 'ATOI', 'HIT', 'FP']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player in players:
            if not player['Pos'] == 'D':
                continue
            writer.writerow(player)

    master_list = []
    for player in get_player_stats():
        master_list.append(
            {
                'Player': player['Player'],
                'Age': player['Age'],
                'Pos': player['Pos'],
                'FP': player['FP']
            }
        )

    for goalie in get_goalie_stats():
        master_list.append(
            {
                'Player': goalie['Player'],
                'Age': goalie['Age'],
                'Pos': goalie['Pos'],
                'FP': goalie['FP']
            }
        )

    master_list = sorted(master_list, key=lambda k: k['FP'], reverse=True)
    with open('output\\master.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Age', 'Pos', 'FP']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player in master_list:
            writer.writerow(player)

