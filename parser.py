from dateutil import parser as date_parser

class Parser:

	def parse_data(self, change):
		"""parsing data dari replica
		
		Args:
		    change (TYPE): Description
		
		Returns:
		    TYPE: Description
		"""
		keys = change['columnnames']
		values = change['columnvalues']
		tipes = change['columntypes']

		hasil = {}

		for c in range(0, len(keys)):

			tipe = tipes[c]
			value = values[c]
			# print(tipe)
			if tipe.find('timestamp') != -1:
				if value:
					value = date_parser.parse(value)
			elif tipe[-2:] == '[]':
				value = value[1:-1]
				if value:
					value = value.split(',')

			hasil[keys[c]] = value

		return hasil

	def parse_delete(self, change):
		oldkeys = change['oldkeys']
		keys = oldkeys['keynames']
		values = oldkeys['keyvalues']

		hasil = {}

		for c in range(0, len(keys)):
			hasil[keys[c]] = values[c]

		return hasil