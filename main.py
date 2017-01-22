import csv
import os

import constants


race = constants.RACES_ZERG

def load_units_csv():
	import pdb
	pdb.set_trace()
	path = os.path.join(constants.PATH_DATA, constants.PATH_UNITS_CSV)
	with open(path, 'r') as units_file:
	    reader = csv.DictReader(units_file)
	    for row in reader:
	    	print(row)
	return reader


def main():
	print('Generating \'{}\' build order'.format(constants.RACES[race ]))

	units = load_units_csv()
	print(units)


if __name__ == '__main__':
	main()
