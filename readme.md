# replikasi Custom postgres dengan python

##examples

quick setup POC replication dengan docker

- `docker-compose -f examples/docker-compose-test.yml up`

##setup pglogical di postgres
- setup extension
`
create extension pglogical;
`

- adding node

`
SELECT pglogical.create_node(
node_name := 'pythonreplica',
dsn := 'host=postgresdb port=5432 dbname=postgres'
);
`

- adding replication set
`
SELECT pglogical.replication_set_add_all_tables('default', ARRAY['public']);
`

