#!/usr/bin/env python3
""" this is a module """


def update_topics(mongo_collection, name, topics):
    """ this is a method """
    query = {"name": name}
    new_values = {"$set": {"topics": topics}}

    mongo_collection.update_many(query, new_values)
