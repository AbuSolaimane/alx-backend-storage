#!/usr/bin/env python3
""" this sis a module """


def schools_by_topic(mongo_collection, topic):
    """ this is a method """
    documents = mongo_collection.find({"topics": topic})
    return list(documents)
