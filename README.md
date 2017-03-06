# Ansible Role for Solr Cloud

This is an ansible role to install Solr Cloud. Configuration is maintained in Zookeeper. Each EC2 instance running Solr also runs an instance of Zookeeper.

## Tags

- zk: Intall, configue and run Zookeeper
- solr: Install, configure and run Solr Cloud
- copy_collection_config: Copy collection config files and custom jars to Zookeeper instances
- collection: Create a new collection
- change_replica: Replaces a Solr server

## Usage

Most of the variables can be found in defaults/main.yml.
Variables to create collections are as follows:

```yml
solr_collections:
  - name: collection1
    upload_to_zookeeper: True
    config_local_folder: solr_configs/collection1
    copy_remote_folder: /home/ubuntu
    config_remote_folder: /home/ubuntu/collection1
    zookeeper_configset_name: collection1
    create_collection: True
    collection_name: collection1
    number_shards: 3
    replication_factor: 2
    max_shards_per_node: 1
  - name: collection2
    upload_to_zookeeper: True
    config_local_folder: solr_configs/collection2
    copy_remote_folder: /home/ubuntu
    config_remote_folder: /home/ubuntu/collection2
    zookeeper_configset_name: collection2
    create_collection: True
    collection_name: collection2
    number_shards: 3
    replication_factor: 2
    max_shards_per_node: 1
```

Steps to setup new Solr Cloud servers
- To install Zookeeper use "zk" tag.
- To install SolrCloud use "solr" tag.
- Copy the collections to all the servers using "copy_collection_config" tag.
- Create collections by using tag "collection"

To replace a server which is down with a new server
- Run the role for all the servers excluding the server which is down and including the new server with tag 'zk'
- Run the role with 'solr' and 'copy_collection_config' tags on the new server
- Run 'change_replica' for all the servers


## Future Enhancements

Separate Zookeeper instances will be taken up in future.
