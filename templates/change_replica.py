import requests, json

solr_instance = 'http://ec2-54-82-164-100.compute-1.amazonaws.com:8983'

r = requests.get(solr_instance + '/solr/admin/collections?action=CLUSTERSTATUS&wt=json')
resp = json.loads(r.text)
live_nodes = resp['cluster']['live_nodes']
down_nodes = []
collection_node_map = {}

for collection, collection_details in resp['cluster']['collections'].iteritems():
    for shard_name, shard_details in collection_details['shards'].iteritems():
        for node_name, node_details in shard_details['replicas'].iteritems():
            if not collection_node_map.get(collection, None):
                collection_node_map[collection] = list()
            print node_details['node_name']
            collection_node_map[collection].append(node_details['node_name'])
            collection_node_map[collection] = list(set(collection_node_map[collection]))
            if (node_details['state'] == "down") and (node_details['node_name'] not in live_nodes):
                down_nodes.append({'collection': collection, 'shard': shard_name, 'replica': node_name, 'node': node_details['node_name']})

replacement_map = {}

for down_node in down_nodes:
    if down_node['node'] not in live_nodes:
        new_nodes = list(set(live_nodes) - set(collection_node_map[down_node['collection']]))
        for new_node in new_nodes:
            if not replacement_map.get(new_node, None):
                replacement_map[new_node] = down_node['node']
                replacement_map[down_node['node']] = new_node

for down_node in down_nodes:
    if down_node['node'] not in live_nodes:
        new_node = replacement_map[down_node['node']]
        print solr_instance + '/solr/admin/collections?action=deletereplica&collection=' + down_node['collection'] + '&shard=' + down_node['shard'] + '&replica=' + down_node['replica'] + '&wt=json'
        # r = requests.get(solr_instance + '/solr/admin/collections?action=deletereplica&collection=' + down_node['collection'] + '&shard=' + down_node['shard'] + '&replica=' + down_node['replica'] + '&wt=json')

for down_node in down_nodes:
    if down_node['node'] not in live_nodes:
        new_node = replacement_map[down_node['node']]
        print solr_instance + '/solr/admin/collections?action=addreplica&collection=' + down_node['collection'] + '&shard=' + down_node['shard'] + '&replica=' + new_node + '&wt=json'
        # r = requests.get(solr_instance + '/solr/admin/collections?action=addreplica&collection=' + down_node['collection'] + '&shard=' + down_node['shard'] + '&replica=' + new_node + '&wt=json')



