import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Blog

# Create your views here.
def get_all_blogs(request):
  blogs = Blog.objects.all()
  blog_list = [{'id': blog.id, 'title': blog.title, 'content': blog.content, 'author': blog.author} for blog in blogs]
  return JsonResponse({'status': 'success', 'data': blog_list})

def get_blog_by_id(request, blog_id):
    if request.method == 'GET':
        try:
            blog = Blog.objects.get(pk=blog_id)

            blog_details = {
                'id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'author': blog.author,
                'pub_date': blog.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
            }

            return JsonResponse({'status': 'success', 'data': blog_details})
        except Blog.DoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Blog does not exist with the given id.'}, status = status.not_found)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def post_add_blog(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        title = data.get('title')
        content = data.get('content')
        author = data.get('author')

        # Create a new Blog instance and save it
        new_blog = Blog(title=title, content=content, author=author)
        new_blog.save()

        return JsonResponse({'status': 'success', 'message': 'data added successfully', 'data': data}, status=201)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    

def post_update_blog(request, blog_id):
    if request.method == 'POST':
        try:
            # Retrieve the existing blog with the given ID or raise a DoesNotExist exception if not found
            existing_blog = Blog.objects.get(pk=blog_id)

            # Load JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Update the existing blog with the data from the request if the fields exist
            if 'title' in data:
                existing_blog.title = data['title']
            if 'content' in data:
                existing_blog.content = data['content']
            if 'author' in data:
                existing_blog.author = data['author']

            # Save the updated blog
            existing_blog.save()

            return JsonResponse({'status': 'success', 'message': 'Blog updated successfully', 'data': data}, status=200)
        except Blog.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Blog with the given ID does not exist.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
def delete_blog_by_id(request, blog_id):
    if request.method == 'DELETE':
        try:
            # Retrieve the existing blog with the given ID or raise a DoesNotExist exception if not found
            existing_blog = Blog.objects.get(pk=blog_id)

            # Delete the blog
            existing_blog.delete()

            return JsonResponse({'status': 'success', 'message': 'Blog deleted successfully'})
        except Blog.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Blog with the given ID does not exist.'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

