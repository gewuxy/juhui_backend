# -*- coding: utf8 -*-
from django.http import JsonResponse
from apps import get_response_data
from apps.commentary.models import Blog, BlogComment, Likes, CommentLikes, Notice
from apps.account.models import Jh_User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from apps.commentary import views_lib
import logging

_logger = logging.getLogger('commentary')


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def save_blog(request):
    '''
    存储短频／长文
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
        parent_blog_id = int(request.POST.get('parent_blog_id', 0))
    except Exception:
        res = get_response_data('000004')
        return JsonResponse(res)
    title = request.POST.get('title', '')
    abstract = request.POST.get('abstract', '')
    content = request.POST.get('content')
    if not content:
        return JsonResponse(get_response_data('000002'))
    first_img = request.POST.get('first_img', '')
    area = request.POST.get('area', '')
    friends = request.POST.get('friends', [])
    if friends:
        try:
            friends = friends.split('|')
        except Exception:
            return JsonResponse(get_response_data('000002'))
    wines = request.POST.get('wines', [])
    if wines:
        try:
            wines = wines.split('|')
        except Exception:
            return JsonResponse(get_response_data('000002'))

    blog = Blog(author=jh_user,
                title=title,
                abstract=abstract,
                content=content,
                first_img=first_img,
                area=area,
                parent_blog_id=parent_blog_id)
    blog.save()
    create_time = blog.create_time.strftime('%Y-%m-%d %H:%M:%S')

    # 通知用户
    views_lib.notice_friends('new_commentary', '新短评', create_time)
    _logger.info('new_commentary | 新短评 | {0}'.format(create_time))

    return JsonResponse(get_response_data('000000'))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def save_comment(request):
    '''
    存储短频／长文的评论
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        res = get_response_data('000004')
        return JsonResponse(res)
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    if not (blog_id and content):
        return JsonResponse(get_response_data('000002'))
    try:
        blog = Blog.objects.get(id=blog_id)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    comment = BlogComment(blog=blog, author=jh_user, content=content)
    comment.save()

    # 通知被评论用户
    create_time = comment.create_time.strftime('%Y-%m-%d %H:%M:%S')
    views_lib.notice_friends('comment', content, create_time, blog.author.id,
                             jh_user.id, jh_user.nickname, jh_user.img_url)
    _logger.info('comment | {0} | {1} | {2} | {3} | {4} | {5}'.format(
        content, create_time, blog.author.id, jh_user.id, jh_user.nickname, jh_user.img_url))

    return JsonResponse(get_response_data('000000'))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def save_like(request):
    '''
    存储短频／长文的赞
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        res = get_response_data('000004')
        return JsonResponse(res)
    blog_id = request.POST.get('blog_id')
    try:
        blog = Blog.objects.get(id=blog_id)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    like = Likes(blog=blog, author=jh_user)
    like.save()

    # 通知被赞用户
    create_time = like.create_time.strftime('%Y-%m-%d %H:%M:%S')
    views_lib.notice_friends('like', '赞', create_time, blog.author.id, jh_user.id, jh_user.nickname, jh_user.img_url)
    _logger.info('like | 点赞 | {0} | {1} | {2} | {3} | {4}'.format(
        create_time, blog.author.id, jh_user.id, jh_user.nickname, jh_user.img_url))

    return JsonResponse(get_response_data('000000'))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def save_comment_like(request):
    '''
    存储评论的赞
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        res = get_response_data('000004')
        return JsonResponse(res)
    comment_id = request.POST.get('comment_id')
    try:
        comment = BlogComment.objects.get(id=comment_id)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    like = CommentLikes(comment=comment, author=jh_user)
    like.save()

    # 通知被赞用户
    create_time = like.create_time.strftime('%Y-%m-%d %H:%M:%S')
    views_lib.notice_friends('like', '赞', create_time, comment.author.id, jh_user.id, jh_user.nickname, jh_user.img_url)
    _logger.info('like | 点赞 | {0} | {1} | {2} | {3} | {4}'.format(
        create_time, comment.author.id, jh_user.id, jh_user.nickname, jh_user.img_url))

    return JsonResponse(get_response_data('000000'))


def get_blog_detail(request):
    '''
    获取短评／长文的详细内容
    '''
    blog_id = request.GET.get('blog_id')
    if not blog_id:
        return JsonResponse(get_response_data('000002'))
    try:
        blog = Blog.objects.get(id=blog_id)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    blog_json = blog.to_json()
    likes_count = views_lib.get_likes_count(blog)  # 获取获赞数
    blog_json['likes_count'] = likes_count
    comments_count = views_lib.get_comments_count(blog)  # 获取评论数
    blog_json['comments_count'] = comments_count
    first_page_comments = views_lib.get_comments(blog)  # 获取第一页的评论
    blog_json['first_page_comments'] = first_page_comments
    return JsonResponse(get_response_data('000000', blog_json))


def get_blog_list(request):
    '''
    获取短评／长文列表
    '''
    page = request.GET.get('page', 1)
    page_num = request.GET.get('page_num', 10)
    try:
        page = int(page)
        page_num = int(page_num)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        jh_user = None
    blogs = views_lib.get_blog_list(page, page_num, jh_user)
    return JsonResponse(get_response_data('000000', blogs))


def get_comments(request):
    '''
    获取短评／长文的评论
    '''
    blog_id = request.GET.get('blog_id')
    if not blog_id:
        return JsonResponse(get_response_data('000002'))
    try:
        blog = Blog.objects.get(id=blog_id)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    page = request.GET.get('page', 1)
    page_num = request.GET.get('page_num', 10)
    try:
        page = int(page)
        page_num = int(page_num)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    comments = views_lib.get_comments(blog, page, page_num)
    return JsonResponse(get_response_data('000000', comments))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_blog(request):
    '''
    删除短评／长文
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        res = get_response_data('000004')
        return JsonResponse(res)
    blog_id = request.POST.get('blog_id')
    if not blog_id:
        return JsonResponse(get_response_data('000002'))
    try:
        blog = Blog.objects.get(id=blog_id, author=jh_user, is_delete=False)
    except Exception:
        return JsonResponse(get_response_data('000000'))
    blog.is_delete = True
    blog.save()
    return JsonResponse(get_response_data('000000'))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_comment(request):
    '''
    删除短评／长文的评论
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        res = get_response_data('000004')
        return JsonResponse(res)
    comment_id = request.POST.get('comment_id')
    if not comment_id:
        return JsonResponse(get_response_data('000002'))
    try:
        comment = BlogComment.objects.get(id=comment_id, is_delete=False)
    except Exception:
        return JsonResponse(get_response_data('000000'))
    blog_author = comment.blog.author
    comment_author = comment.author
    if jh_user not in [blog_author, comment_author]:
        return JsonResponse(get_response_data('300001'))
    comment.is_delete = True
    comment.save()
    return JsonResponse(get_response_data('000000'))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_like(request):
    '''
    取消短评／长文的赞
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        res = get_response_data('000004')
        return JsonResponse(res)
    blog_id = request.POST.get('blog_id')
    if not blog_id:
        return JsonResponse(get_response_data('000002'))
    try:
        blog = Blog.objects.get(id=blog_id, is_delete=False)
        like = Likes.objects.get(blog=blog, author=jh_user, is_delete=False)
        like.is_delete = True
        like.save()
    except Exception:
        return JsonResponse(get_response_data('000000'))
    return JsonResponse(get_response_data('000000'))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_comment_like(request):
    '''
    取消评论的赞
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        res = get_response_data('000004')
        return JsonResponse(res)
    comment_id = request.POST.get('comment_id')
    if not comment_id:
        return JsonResponse(get_response_data('000002'))
    try:
        comment = BlogComment.objects.get(id=comment_id, is_delete=False)
        like = CommentLikes.objects.get(comment=comment, author=jh_user, is_delete=False)
        like.is_delete = True
        like.save()
    except Exception:
        return JsonResponse(get_response_data('000000'))
    return JsonResponse(get_response_data('000000'))


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_notices(request):
    '''
    获取提醒消息列表
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        res = get_response_data('000004')
        return JsonResponse(res)
    page = request.GET.get('page', 1)
    page_num = request.GET.get('page_num', 10)
    try:
        page = int(page)
        page_num = int(page_num)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    notices = Notice.objects.filter(to_user=jh_user).order_by('-create_time')
    start = (page - 1) * page_num
    end = page * page_num
    notices_json = []
    for notice in notices[start:end]:
        notices_json.append(notice.to_json())
        notice.is_read = True
        notice.save()
    return JsonResponse(get_response_data('000000', notices_json))