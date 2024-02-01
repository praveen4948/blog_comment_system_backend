import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Comment
from blog.models import Blog

# Create your views here.
def get_all_comments(request):
    comments = Comment.objects.all()
    comment_list = [{'id': comment.id,'blog_id':comment.blog_id, 'content': comment.content, 'author': comment.author} for comment in comments]
    return JsonResponse({'status': 'success', 'data': comment_list})

def get_comment_by_id(request, comment_id):
    if request.method == 'GET':
        try:
            comment = Comment.objects.get(pk=comment_id)

            comment_details = {
                'id': comment.id,
                'content': comment.content,
                'author': comment.author,
                'pub_date': comment.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
            }

            return JsonResponse({'status': 'success', 'data': comment_details})
        except Comment.DoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Comment does not exist with the given id.'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def post_add_comment(request, blog_id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        content = data.get('content')
        author = data.get('author')
        blog = Blog.objects.get(pk=blog_id)

        new_comment = Comment(blog=blog, content=content, author=author)
        new_comment.save()

        return JsonResponse({'status': 'success', 'message': 'Comment added successfully', 'data': data}, status=201)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def post_update_comment(request, comment_id):
    if request.method == 'POST':
        try:
            existing_comment = Comment.objects.get(pk=comment_id)

            data = json.loads(request.body.decode('utf-8'))

            if 'content' in data:
                existing_comment.content = data['content']
            if 'author' in data:
                existing_comment.author = data['author']

            existing_comment.save()

            return JsonResponse({'status': 'success', 'message': 'Comment updated successfully', 'data': data}, status=200)
        except Comment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Comment with the given ID does not exist.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def delete_comment_by_id(request, comment_id):
    if request.method == 'DELETE':
        try:
            existing_comment = Comment.objects.get(pk=comment_id)
            existing_comment.delete()

            return JsonResponse({'status': 'success', 'message': 'Comment deleted successfully'})
        except Comment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Comment with the given ID does not exist.'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    

def get_comments_by_blog_id(request, blog_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(blog_id=blog_id)

        comment_list = [
            {
                'id': comment.id,
                'content': comment.content,
                'author': comment.author,
                'pub_date': comment.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for comment in comments
        ]

        return JsonResponse({'status': 'success', 'blog_id': blog_id, 'comments': comment_list})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})