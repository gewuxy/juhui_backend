from django.http import JsonResponse
from apps.chat.models import Comment
from apps.wine.models import WineInfo
from apps import get_response_data


def get_comment(request):
    wine_code = request.GET.get('code')
    if not wine_code:
        return JsonResponse(get_response_data('000002'))
    count = request.GET.get('count', 100)
    try:
        count = int(count)
        wine = WineInfo.objects.get(code=wine_code)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    comments = Comment.objects.filter(wine=wine).order_by('-create_at')[:100]
    data = []
    for comment in comments:
        tmp_comment = {}
        tmp_comment['mobile'] = comment.user.mobile
        tmp_comment['img_url'] = comment.user.img_url
        tmp_comment['nickname'] = comment.user.nickname
        tmp_comment['wine_name'] = comment.wine.name
        tmp_comment['wine_code'] = comment.wine.code
        tmp_comment['content'] = comment.content
        tmp_comment['type'] = comment.type
        tmp_comment['create_at'] = comment.create_at
        data.append(tmp_comment)
    return JsonResponse(get_response_data('000000', data))
