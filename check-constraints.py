#!/usr/bin/env python
# USAGE: Download output from http://ip-address/service/marathon/v2/apps 
# E.G 'wget -0 output http://ip-address/service/marathon/v2/apps'
# and then run 'python check-constraints.py output'


import json
import re
import sys


UNIQUE_OP   = "UNIQUE"
CLUSTER_OP  = "CLUSTER"
GROUP_BY_OP = "GROUP_BY"
LIKE_OP     = "LIKE"
UNLIKE_OP   = "UNLIKE"


def group_by_value_valid(value):
    try:
        int(value)
        return True
    except:
        return False


def un_like_value_valid(value):
    try:
        re.compile(value)
        return True
    except:
        return False


def report_invalid_constraint(app_id, constraint):
    print("Invalid constraint in {} app: {}".format(app_id, json.dumps(constraint)))


def main(path):
    with open(path, "r") as f:
        content_json = json.load(f)
    apps = content_json["apps"]
    for app in apps:
        for constraint in app.get("constraints", []):
            field, operator = constraint[0], constraint[1]
            value = None
            if len(constraint) > 2:
                value = constraint[2]

            if ((operator == UNIQUE_OP   and value is not None) or
                (operator == CLUSTER_OP  and value is None) or
                (operator == CLUSTER_OP  and value is not None and value == "") or
                (operator == GROUP_BY_OP and not group_by_value_valid(value)) or
                (operator == LIKE_OP     and value is None) or
                (operator == LIKE_OP     and not un_like_value_valid(value)) or
                (operator == UNLIKE_OP   and value is None) or
                (operator == UNLIKE_OP   and not un_like_value_valid(value))):
                report_invalid_constraint(app["id"], constraint)
