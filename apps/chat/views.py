from django.http import JsonResponse
from apps.chat.models import Comment
from apps.wine.models import WineInfo
from apps import get_response_data
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from config.settings.common import ROOT_DIR


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_comment(request):
    wine_code = request.GET.get('code')
    if not wine_code:
        return JsonResponse(get_response_data('000002'))
    page = request.GET.get('page', 1)
    page_num = request.GET.get('page_num', 50)
    # count = request.GET.get('count', 100)
    try:
        # count = int(count)
        page = int(page)
        page_num = int(page_num)
        start = (page - 1) * page_num
        end = page * page_num
        wine = WineInfo.objects.get(code=wine_code)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    comments = Comment.objects.filter(wine=wine).order_by('-create_at')[start: end]
    data = []
    for comment in comments:
        tmp_comment = {}
        tmp_comment['user_id'] = comment.user.id
        tmp_comment['mobile'] = comment.user.mobile
        tmp_comment['user_img_url'] = comment.user.img_url
        tmp_comment['nickname'] = comment.user.nickname
        tmp_comment['wine_name'] = comment.wine.name
        tmp_comment['wine_code'] = comment.wine.code
        tmp_comment['content'] = comment.content
        tmp_comment['video_img_url'] = comment.video_img_url
        tmp_comment['type'] = comment.type
        tmp_comment['create_at'] = comment.create_at
        data.append(tmp_comment)
    return JsonResponse(get_response_data('000000', data))


@api_view(['POST'])
@permission_classes((IsADirectoryError, ))
def upload(request):
    file = request.FILES.get('file')
    if not file:
        return JsonResponse(get_response_data('200001'))
    file_name = file.name
    print('file name is {0}'.format(file_name))
    try:
        file_type = file_name.split('.')[1]
    except Exception:
        return JsonResponse(get_response_data('200002'))
    if file_type in ['jpg', 'JPG', 'JPEG', 'jpeg', 'png', 'PNG']:
        file_path = ROOT_DIR + 'media/img/' + file_name
        media_url = request.build_absolute_uri('media/img/' + file_name)
    elif file_type in ['mp3', 'MP3', 'amr', 'AMR']:
        file_path = ROOT_DIR + 'media/voice/' + file_name
        media_url = request.build_absolute_uri('media/voice/' + file_name)
    elif file_type in ['mp4', 'MP4']:
        file_path = ROOT_DIR + 'media/video/' + file_name
        media_url = request.build_absolute_uri('media/video/' + file_name)
    else:
        return JsonResponse(get_response_data('200002'))
    print('file path is {0}'.format(file_path))
    with open(str(file_path), 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    data = {'media_url': media_url}

    return JsonResponse(get_response_data('000000', data))