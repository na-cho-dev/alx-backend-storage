#!/usr/bin/env python3
"""
Module: Where can I learn Python?
"""


def schools_by_topic(mongo_collection, topic):
    """Python function that returns a list of school
    having a specific topic

    Args:
        mongo_collection: pymongo collection object
        topic (string): Topic searched
    """
    return [doc for doc in mongo_collection.find({"topics": topic})]
