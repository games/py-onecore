# coding=utf-8
# funnylab.org
#
from bson.objectid import ObjectId

__author__ = 'valorzhong'

class ObjectMapper(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

class Model(object):

    def __init__(self):
        self._id = ObjectId()
        self.key = None

    def wrap(self, dict_data):
        for key in dict_data.keys():
            val = dict_data[key]
            if isinstance(val, list):
                tmp = []
                for el in val:
                    if isinstance(el, dict):
                        tmp.append(ObjectMapper(el))
                    else:
                        tmp.append(el)
                val = tmp
            setattr(self, key, val)
            if key == '_id':
                setattr(self, 'key', val)
        return self

    def to_mongo(self):
        def filter(m):
            return m[:1] != '_' and m != 'key'
        return self._format_to_json(filter)

    def json(self):
        def filter(m):
            return m[:1] != '_'
        return self._format_to_json(filter)

    def _format_to_json(self, filter):
        members = dir(self)
        result = {}
        for m in members:
            if filter(m):
                attr = getattr(self, m)
                val = self._format_member_to_json(attr)
                if val is not None:
                    result[m] = val
        return result

    def _format_member_to_json(self, member):
        result = None
        if isinstance(member, list):
            array = []
            for element in member:
                array.append(self._format_member_to_json(element))
            result = array
        elif isinstance(member, Model):
            result = member.format_to_storage()
        elif isinstance(member, ObjectId):
            result = str(member)
        elif not callable(member):
            result = member
        return result

    @classmethod
    def wrap_models_by_dict(cls, json_arr):
        result = []
        for o in json_arr:
            result.append(cls().wrap(o))
        return result

    @staticmethod
    def json_by_models(models):
        result = []
        for m in models:
            result.append(m.json())
        return result

if __name__ == '__main__':
    class C(Model):
        id = 0
        kk = ObjectId('4e90965a29624d0e4c000003')
        name = 'C name'

    arr = []
    models = []
    for i in range(0, 10):
        c = C()
        arr.append(c.json())
        models.append(c)

    print arr
    print C.wrap_models_by_dict(arr)
    print C.json_by_models(models)