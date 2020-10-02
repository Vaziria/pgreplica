from datetime import datetime

import pytest

from ..puan_replica import BasicConsumer


@pytest.fixture
def consumer():
	yield BasicConsumer()


def test_parse_update_insert(consumer):

	change = {'kind': 'insert', 'schema': 'public', 'table': 'users', 'columnnames': ['id', 'name', 'image', 'email', 'password', 'user_type', 'verified', 'juragan_id', 'active', 'receive_ord_at', 'last_login', 'created'], 'columntypes': ['integer', 'character varying(64)', 'character varying', 'character varying(64)', 'character varying(80)', 'user_type', 'boolean', 'integer', 'boolean', 'timestamp without time zone', 'timestamp without time zone', 'timestamp without time zone'], 'columnvalues': [1206, 'Banara Wastuti', None, 'nurdiyantikarsana@yahoo.com', '2e6a0fc5e51d119fc5cd8c0a89bbbc7ae5a700f944d54fc167deb8fe0a9adb24', 'juragan', None, None, None, None, '2020-10-02 07:48:17.934764', '2020-10-02 07:48:17.934764']}
	hasil = consumer.parse_data(change)

	assert isinstance(hasil['created'], datetime)