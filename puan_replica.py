import sys
import os
import json

os.environ['logfile'] = 'puan_replica.log'

import psycopg2
from psycopg2.extras import LogicalReplicationConnection, REPLICATION_LOGICAL

from vazutils.logger import Logger


from .parser import Parser

logger = Logger(__name__)

def create_connection(**kargs):
	# host = '192.168.1.2',
	# password = 'heri7777',
	# port = '5432',
	# user = 'postgres',
	conn = psycopg2.connect(connection_factory=LogicalReplicationConnection, **kargs)

	return conn

def delete_replication(conn):
	cur = conn.cursor()

	cur.drop_replication_slot("python_puan")

def run_replication(conn, consumer):

	cur = conn.cursor()

	# cur.drop_replication_slot("python_puan")
	# exit()
	try:
		cur.start_replication(slot_name='python_puan', decode=True)

	except psycopg2.ProgrammingError as e:

		cur.create_replication_slot('python_puan', output_plugin='wal2json')
		cur.start_replication( slot_name='python_puan', decode=True)



	print("Starting streaming, press Control-C to end...", file=sys.stderr)

	try:
		cur.consume_stream(consumer)
	except KeyboardInterrupt:
		cur.close()
		conn.close()
		print("The slot 'pytest' still exists. Drop it with SELECT pg_drop_replication_slot('pytest'); if no longer needed.", file=sys.stderr)
		print("WARNING: Transaction logs will accumulate in pg_xlog until the slot is dropped.", file=sys.stderr)



class BasicReplica(Parser):

	transactions = None

	consumers = {

	}

	def __init__(self):
		self.transactions = []

	def add_consumer(self, obj = None, table = None):

		if not table and obj:
			table = obj.table
		
		elif not table or not obj:
			return False

		self.consumers[table] = obj 

		return True

	def ack(self, msg):
		msg.cursor.send_feedback(flush_lsn=msg.data_start)
		self.transactions = []

	def __call__(self, msg):
		
		data = json.loads(msg.payload)
		logger.debug(msg.payload)
		changes = data['change']
		# print('------------')

		# self.transactions = changes

		for change in changes:
			# print(change)
			# print('\n')
			table = change.get('table')
			kind = change.get('kind')

			func = self.consumers.get(table, self.default_callback)
			# print(func.__class__.__name__)
			payload = func(kind, table, change)
			if isinstance(payload, list):
				self.transactions.extend(payload)

		self.save_transaction()
		self.ack(msg)


	def save_transaction(self):
		trans = self.transactions


	def default_callback(self, kind, table, change):
		logger.info('{}_{} not handled'.format(kind, table))

		return True


# class TestConsumer(BasicConsumer):

# 	def insert_buyer(self, kind, table, change):
# 		hasil = self.parse_data(change)
# 		print(hasil)

# 	def update_buyer(self, kind, table, change):
# 		hasil = self.parse_data(change)
# 		print(hasil)


	



# if __name__ == '__main__':
# 	conn = create_connection(
# 			host = '192.168.1.2',
# 			password = 'heri7777',
# 			port = '5432',
# 			user = 'postgres'
# 		)

# 	consumer = TestConsumer()
# 	run_replication(conn, consumer)


	