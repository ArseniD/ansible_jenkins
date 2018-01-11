# -*- coding: utf-8 -*-

def get_mongo_src(args, os_family, release_num, mongo_v):
    if os_family and release_num and mongo_v is not None:
        matching = [param for param in args if os_family + release_num in param and mongo_v in param]
        return matching


class FilterModule(object):

    def filters(self):
        return {
            'get_mongo_src': get_mongo_src,
}