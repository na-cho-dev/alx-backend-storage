#!/usr/bin/env python3
"""
List all documents in Python
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    Args:
        mongo_collection: pymongo collection object
    Returns:
        All documents in a collection or an empty list if no document
        in the collection
    """
    return [doc for doc in mongo_collection.find()]
