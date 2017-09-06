# -*- coding: utf8 -*-
from django.http import JsonResponse
from apps import get_response_data
from apps.commentary.models import Blog, BlogComment, Likes
from apps.account.models import Jh_User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from apps.commentary import views_lib


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def save_blog(request):
    '''
    存储短频／长文
    '''
    try:
        jh_user = Jh_User.objects.get(user=request.user)
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
                area=area)
    blog.save()

    # 通知用户
    views_lib.notice_friends()

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
    views_lib.notice_friends()

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
    views_lib.notice_friends()

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
    like_id = request.POST.get('like_id')
    if not like_id:
        return JsonResponse(get_response_data('000002'))
    try:
        like = Likes.objects.get(id=like_id, author=jh_user, is_delete=False)
    except Exception:
        return JsonResponse(get_response_data('000000'))
    like.is_delete = True
    like.save()
    return JsonResponse(get_response_data('000000'))