#!/usr/bin/env python3
"""
A python module that calculates top students
"""


def top_students(mongo_collection):
    """
    Python function that returns all students
    sorted by average score
    """
    return list(mongo_collection.aggregate([
        {
            "$project": {
                '_id': 1,
                "name": "$name",
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]))
