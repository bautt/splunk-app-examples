#!/usr/bin/env python
#
# Copyright 2011-2015 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A command line utility for interacting with Splunk KV Store Collections."""

import json
import sys

from splunklib.client import connect

from utils import parse


def main():
    opts = parse(sys.argv[1:], {}, ".env")
    opts.kwargs["owner"] = "nobody"
    opts.kwargs["app"] = "search"
    service = connect(**opts.kwargs)

    print("KV Store Collections:")
    for collection in service.kvstore:
        print("  %s" % collection.name)

    # Let's delete a collection if it already exists, and then create it
    collection_name = "example_collection"
    if collection_name in service.kvstore:
        service.kvstore.delete(collection_name)

    # Let's create it and then make sure it exists    
    service.kvstore.create(collection_name)
    collection = service.kvstore[collection_name]

    # Let's make sure it doesn't have any data
    print("Should be empty: %s" % json.dumps(collection.data.query()))

    # Let's add some json data
    collection.data.insert(json.dumps({"_key": "item1", "somekey": 1, "otherkey": "foo"}))
    # Let's add data as a dictionary object
    collection.data.insert({"_key": "item2", "somekey": 2, "otherkey": "foo"})
    collection.data.insert(json.dumps({"somekey": 3, "otherkey": "bar"}))

    # Let's make sure it has the data we just entered
    print("Should have our data: %s" % json.dumps(collection.data.query(), indent=1))

    # Let's run some queries
    print("Should return item1: %s" % json.dumps(collection.data.query_by_id("item1"), indent=1))

    # Let's update some data
    data = collection.data.query_by_id("item2")
    data['otherkey'] = "bar"
    # Passing data using 'json.dumps'
    collection.data.update("item2", json.dumps(data))
    print("Should return item2 with updated data: %s" % json.dumps(collection.data.query_by_id("item2"), indent=1))
    data['otherkey'] = "foo"
    # Passing data as a dictionary instance
    collection.data.update("item2", data)
    print("Should return item2 with updated data: %s" % json.dumps(collection.data.query_by_id("item2"), indent=1))

    query = json.dumps({"otherkey": "foo"})
    print("Should return item1 and item2: %s" % json.dumps(collection.data.query(query=query), indent=1))

    query = json.dumps({"otherkey": "bar"})
    print("Should return third item with auto-generated _key: %s" % json.dumps(collection.data.query(query=query),
                                                                               indent=1))

    # passing query data as dict
    query = {"somekey": {"$gt": 1}}
    print("Should return item2 and item3: %s" % json.dumps(collection.data.query(query=query), indent=1))

    # Let's delete the collection
    collection.delete()


if __name__ == "__main__":
    main()
