from django.test import TestCase
from apps.chat.models import Comment
from apps.wine.models import WineInfo
from apps.account.models import Jh_User
import time
from django.http import JsonResponse
from apps import get_response_data

# Create your tests here.

def create_comment(request):
    wine = WineInfo.objects.get(code='147108')
    for user in Jh_User.objects.all():
        timestamp = int(time.time() * 1000)
        comment = Comment(
            wine=wine,
            user=user,
            content = 'this message was created at {0}'.format(timestamp),
            type = 0,
            create_at=str(timestamp)
        )
        comment.save()
    return JsonResponse(get_response_data('000000'))