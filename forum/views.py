from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from fnb.models import Fnb
from forum.models import Forum, ForumKhusus
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
import json
from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.db.models import Count

# Create your views here.
def show_forum(request):
    # context = {
    #     "forums" : Forum.objects.all()
    # }

    # return render(request,"forum_umum.html",context)
    filter_unanswered = request.GET.get('filter_unanswered', 'false') == 'true'

    if filter_unanswered:
        forums = Forum.objects.annotate(comment_count=Count('forum_khusus')).filter(comment_count=1)
    else:
        forums = Forum.objects.all()

    context = {
        "forums": forums,
        "filter_unanswered": filter_unanswered,  # Pass the filter state to the template
    }
    return render(request, 'forum_umum.html', context)

@login_required
@csrf_exempt  
def add_forum(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get('name'))
        comment_text = strip_tags(data.get('comment'))

        if name and comment_text:
            
            new_forum = Forum(name=name, text=comment_text, user=request.user)
            new_forum.save()

            new_comment = ForumKhusus(text=comment_text, forum=new_forum, user=request.user)
            # new_comment.forum = new_forum
            new_comment.save()


            context = {'name': name, 'comment': comment_text, 
                       'time_created': new_forum.time_created.strftime('%Y-%m-%d %H:%M'),
                        'forum': new_forum }

            print(context)
            try:
                html = render_to_string('forum_card.html', context)
            except Exception as e:
                print(e)
                html = "error"
            # return JsonResponse({
            #     'name': name,
            #     'comment': comment_text,
            #     'time_created': new_forum.time_created.strftime('%Y-%m-%d %H:%M')
            # })
            return JsonResponse({"html" : html})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def add_forum_khusus(request, id):
    forum = get_object_or_404(Forum, pk=id)

    if request.method == 'POST':
        data = json.loads(request.body)
        comment_text = strip_tags(data.get('comment'))
        if comment_text:
            new_comment = ForumKhusus.objects.create(text=comment_text, forum=forum, user=request.user)

            html = render_to_string('comment.html', {
                'comment': new_comment
            })

            return JsonResponse({
                'html': html
            })
            # return JsonResponse({
            #     'comment_text': new_comment.text,
            #     'time_created': new_comment.time_created.strftime('%Y-%m-%d %H:%M'),
            #     'username': new_comment.user.username
            # })
        return JsonResponse({'error': 'Comment text is required'}, status=400)

    comments = forum.forum_khusus.all()
    return render(request, 'forum_khusus.html', {'forum': forum, 'comments': comments})