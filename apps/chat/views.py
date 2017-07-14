from django.http import JsonResponse
from apps.chat.models import Comment
from apps.wine.models import WineInfo
from apps.account.models import Jh_User
from apps import get_response_data
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from config.settings.common import ROOT_DIR
from apps.chat.chat_view_lib import set_video_img_1
import time


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


def save_comment(request):
    user_id = request.POST.get('user_id')
    wine_code = request.POST.get('wine_code')
    msg_type = request.POST.get('msg_type')
    content = request.POST.get('content')
    video_img = request.POST.get('video_img', '')
    create_at = request.POST.get('create_at')
    if not (user_id and wine_code and msg_type and content and create_at):
        return JsonResponse(get_response_data('000002'))
    try:
        wine = WineInfo.objects.get(code=wine_code)
        user = Jh_User.objects.get(id=user_id)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    comment = Comment(
        wine=wine,
        user=user,
        content=content,
        video_img_url=video_img,
        type=msg_type,
        create_at=create_at
    )
    comment.save()
    return JsonResponse(get_response_data('000000'))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def upload(request):
    file = request.FILES.get('file')
    if not file:
        return JsonResponse(get_response_data('200001'))
    file_name = file.name
    timestamp = str(int(time.time() * 1000))
    print('file name is {0}'.format(file_name))
    try:
        file_type = file_name.split('.')[1]
    except Exception:
        return JsonResponse(get_response_data('200002'))
    video_img_url = ''
    root_str= str(ROOT_DIR)
    if file_type in ['jpg', 'JPG', 'JPEG', 'jpeg', 'png', 'PNG']:
        file_path = root_str + '/media/chat/img/' + timestamp + '_' + file_name
        media_url = request.build_absolute_uri('/') + 'media/chat/img/' + timestamp + '_' + file_name
    elif file_type in ['mp3', 'MP3', 'amr', 'AMR', 'aac', 'AAC']:
        file_path = root_str + '/media/chat/voice/' + timestamp + '_' + file_name
        media_url = request.build_absolute_uri('/') + 'media/chat/voice/' + timestamp + '_' + file_name
    elif file_type in ['mp4', 'MP4']:
        file_path = root_str + '/media/chat/video/' + timestamp + '_' + file_name
        media_url = request.build_absolute_uri('/') + 'media/chat/video/' + timestamp + '_' + file_name
        video_img_path = root_str + '/media/chat/video/' + timestamp + '.jpg'
        video_img_url = request.build_absolute_uri('/') + 'media/chat/video/' + timestamp + '.jpg'
    else:
        return JsonResponse(get_response_data('200002'))
    print('file path is {0}'.format(file_path))
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    data = {'media_url': media_url, 'media_img_url': ''}
    if video_img_url:
        rval = set_video_img_1(file_path, video_img_path)
        if rval:
            data['media_img_url'] = video_img_url

    return JsonResponse(get_response_data('000000', data))
