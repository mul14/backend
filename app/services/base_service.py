from app.models import db
from app.models.attendee import Attendee

class BaseService():

    def __init__(self, page=0, base_url='', total_items=0):
        self.page = page
        self.base_url = base_url
        self.total_items = total_items

    def paginate(self, query):
        results = query.paginate(int(self.page), int(self.perpage), False)
        self.paginated = {}
        links = {}

        links['prev'] = (self.base_url + '?page=' + str(results.prev_num)) if results.prev_num else None
        links['next'] = (self.base_url + '?page=' + str(results.next_num)) if results.next_num else None
        links['curr'] = self.base_url + '?page=' + str(self.page)
        links['total_items'] = self.total_items

        self.paginated['data'] = results.items
        self.paginated['links'] = links

        return self.paginated

    def include(self, fields):
        _results = []
        for item in self.paginated['data']:
            data = item.as_dict()
            for field in fields:
                data[field] = getattr(item, field).as_dict() if getattr(item, field) else None
            _results.append(data)
        self.paginated['data'] = _results
        return self.paginated


    def outer_include(self, data, fields):
        # TODO: add filterby key need to be dynamic to be able to used by other class than user
        for field in fields:
            prep = db.session.query(eval(field)).filter_by(user_id=data['id']).first()
            data[field.lower()] = prep.as_dict() if prep else None
        return data


    def transform(self):
        _results = []
        for item in self.paginated['data']:
            item = item.as_dict()
            _results.append(item)
        self.paginated['data'] = _results
        return self.paginated

    def filter_update_payload(self, payload):
        new_data = {}
        for key in payload:
            if payload[key] is not None:
                new_data[key] = payload[key]
        return new_data
