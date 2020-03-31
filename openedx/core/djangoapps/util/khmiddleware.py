from arfrontconfig.models import NewerguideRecord


class DemonMiddleware(object):
    
    def process_request(self, request):
        user_id = request.user.id
        request.domon_type = ''
        if user_id is not None:
            res = NewerguideRecord.objects.filter(user_id=user_id, live_guide=True)
            if not res:
                request.domon_type = 'live'
