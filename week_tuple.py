from collections import namedtuple


# data structure for better handling of iso-calendar weeks, removes week day
Week_tuple = namedtuple("Week_tuple", ["year", "week"])
