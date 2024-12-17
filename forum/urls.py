from django.urls import path
from forum.views import show_forum, add_forum, add_forum_khusus,show_forum_umum_json,show_forum_khusus_json

app_name = 'forum'

urlpatterns = [
    path('', show_forum, name='show-forum-umum'),
    path("add_forum/", add_forum, name= "add-forum"),
    path('forum/<int:id>/', add_forum_khusus, name='forum-khusus'),
    path("json/",show_forum_umum_json,name="show_forum_umum_json"),
    path("<int:id>/json/",show_forum_khusus_json,name="show_forum_khusus_json")
]