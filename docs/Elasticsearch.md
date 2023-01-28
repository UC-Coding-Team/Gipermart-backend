# Elasticsearch Architecture

For the design of the Elasticsearch architecture for the data storage of the Gota: A Services for Recipes project, the following has been considered:

- Index lifecycle management (ILM)
- Template Index (Mapping, Settings)

## ILM

[ILM](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html) is the automation of data cycle management according to performance, resiliency or retention requirements by defining management policies.
In this way, new indexes can be created automatically depending on the number of data or their size, or according to their age, or reduce the number for better management of the shards in the cluster.

Is defined in the following settings [Rollover](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-rollover.html) after 50 gb of index and the [Lifecycle Index](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-index-lifecycle.html) .

    {
        "policy": {
            "phases": {
            "hot": {
                "min_age": "0ms",
                "actions": {
                "rollover": {
                    "max_size": "50gb"
                },
                "set_priority": {
                    "priority": 100
                }
                }
            },
            "warm": {
                "min_age": "365d",
                "actions": {
                "forcemerge": {
                    "max_num_segments": 1
                },
                "set_priority": {
                    "priority": 50
                }
                }
            },
            "cold": {
                "min_age": "365d",
                "actions": {
                "set_priority": {
                    "priority": 0
                }
                }
            }
            }
        }
    }


## Template
An index template is a way to tell Elasticsearch how to configure an index when it is created.
For this project It defined the next: 

- Mapping: Is the process of defining how a document, and the fields it contains, are stored and indexed.
- Settings: The lifecyle, number of shards and replicas, pipeline and other functional characteristics of the index are defined in the configuration.
- Pipelines: Define a pipeline for preprocessing documents before indexing.
For this project has defined add-current-time(date of document ingestion to elasticsearch)

        {
        "recipe-000001" : {
            "aliases" : {
            "r_recipe" : {
                "is_write_index" : true
            }
            },
            "mappings" : {
            "dynamic_templates" : [ ],
            "properties" : {
                "ingredients" : {
                "type" : "nested",
                "dynamic" : "true",
                "properties" : {
                    "ingredient" : {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                        }
                    }
                    },
                    "name" : {
                    "type" : "text"
                    },
                    "quantity" : {
                    "type" : "keyword"
                    }
                }
                },
                "labels" : {
                "type" : "keyword"
                },
                "name" : {
                "type" : "text"
                },
                "steps" : {
                "type" : "nested",
                "dynamic" : "true",
                "properties" : {
                    "description" : {
                    "type" : "text"
                    },
                    "step" : {
                    "type" : "integer"
                    }
                }
                },
                "timestamp" : {
                "type" : "date"
                }
            }
            },
            "settings" : {
            "index" : {
                "lifecycle" : {
                "name" : "recipes_policy",
                "rollover_alias" : "r_recipe"
                },
                "routing" : {
                "allocation" : {
                    "include" : {
                    "_tier_preference" : "data_content"
                    }
                }
                },
                "mapping" : {
                "nested_objects" : {
                    "limit" : "10000"
                },
                "total_fields" : {
                    "limit" : "10000"
                }
                },
                "number_of_shards" : "3",
                "provided_name" : "recipe-000001",
                "max_inner_result_window" : "10000",
                "default_pipeline" : "add-current-time",
                "creation_date" : "1663256531724",
                "priority" : "100",
                "number_of_replicas" : "1",
                "uuid" : "8K7_LLWqReuWn1HO1zlwRA",
                "version" : {
                "created" : "7110299"
                }
            }
            }
        }
        }   












