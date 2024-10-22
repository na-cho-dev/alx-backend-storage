#!/usr/bin/env python3
"""
Insert a document in Python
"""


def insert_school(mongo_collection, **kwargs):
    """
    Python function that inserts a new document
    in a collection based on kwargs

    Args:
        mongo_collection -> pymongo collection object
        kwargs           -> Variable number of key vaue args
    """
    result = mongo_collection.insert_one(kwargs).inserted_id

    return result
