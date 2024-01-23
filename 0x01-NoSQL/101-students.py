#!/usr/bin/env python3
""" this is a module """


def top_students(mongo_collection):
    # sourcery skip: inline-immediately-returned-variable
    """ this si a method """
    top_student = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_student
