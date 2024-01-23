#!/usr/bin/env python3
""" this is a module """


def list_all(mongo_collection):
    """ this is a method """
    documents = mongo_collection.find()

    if documents.count() == 0:
        return []

    return documents
