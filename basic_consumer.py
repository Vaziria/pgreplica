from vazutils.logger import Logger

from .parser import Parser

logger = Logger(__name__)


class BasicConsumer(Parser):

	table = 'basic_consumer'

	def __call__(self, kind, table, change):
		
		if kind in ['insert', 'update']:
			change = self.parse_data(change)

		elif kind == 'delete':
			change = self.parse_delete(change)	

		func = getattr(self, kind, self.default_callback)
		# print(self.table)
		return func(kind, change)

	def default_callback(self, kind, change):
		logger.info('{}_{} not handled'.format(kind, self.table))

		return True