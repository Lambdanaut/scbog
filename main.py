import csv
import os

import constants


chosen_race = constants.RACES_ZERG


class Genetic(object):
    def __init__(self, unit_types):
        self.unit_types = unit_types

        self.population = []

    def run(self):
        pass

    def generation(self):
        pass

    def mutate(self):
        pass

    def mate(self):
        pass

    def heuristic(self):
        pass

    def get_buildables(self, units, check_supply=False):
        buildables = []
        for unit_type in self.unit_types.values():
            required = [u for u in [unit_type['requires'], unit_type['devours']] if u]
            if (# Required units check
                all([u in units for u in required]) and 
                # Supply check
                (not check_supply or self.remaining_supply(units) >= unit_type['supply'])):

                buildables.append(unit_type['name'])

        return buildables

    def remaining_supply(self, units):
        return self.sum_of_field(units, 'supply_given') - self.sum_of_field(units, 'supply')

    def sum_of_field(self, units, field):
        return sum([self.unit_types[u][field] for u in units])


def load_unit_types_csv():
    path = os.path.join(constants.PATH_DATA, constants.PATH_UNITS_TYPES_CSV)
    with open(path, 'r') as unit_types_file:
        reader = csv.DictReader(unit_types_file)
        unit_types = {u['name']: u for u in reader if u.get('race') == constants.RACES[chosen_race]}

        # Typify columns
        for u_name, u in unit_types.items():
            unit_types[u_name]['life'] = int(u['life'])
            unit_types[u_name]['mineral_cost'] = int(u['mineral_cost'])
            unit_types[u_name]['vespene_cost'] = int(u['vespene_cost'])
            unit_types[u_name]['supply'] = int(u['supply'])
            unit_types[u_name]['supply_given'] = int(u['supply_given'])

    return unit_types


def main():
    print('Generating \'{}\' build order'.format(constants.RACES[chosen_race]))

    test_units_1 = ['hatchery', 'drone', 'overlord']
    test_units_2 = ['hatchery', 'overlord'] + ['drone' for d in range(10)]

    unit_types = load_unit_types_csv()

    genetic = Genetic(unit_types)

    # Testing Assertions
    assert (genetic.sum_of_field(test_units_1, 'supply_given') == 10)
    assert (genetic.remaining_supply(test_units_2) == 0)

    # Buildables Assertions
    assert (set(genetic.get_buildables(test_units_1)) == {
        'hatchery', 'drone', 'overlord', 'spawning pool',
        'extractor', 'evolution chamber'} )

    assert (set(genetic.get_buildables(test_units_2, check_supply=True)) == {
        'hatchery', 'overlord', 'spawning pool', 'extractor',
        'evolution chamber'} )


if __name__ == '__main__':
    main()
