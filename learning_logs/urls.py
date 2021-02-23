"""
定义learning_logs的URL模式
"""
from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    #主页
    path('', views.index, name='index'),
    #显示所有的主题
    path('topics/', views.topics, name='topics'),
    #显示特定主题的详细页面
    path('topics/<int:topic_id>/', views.topic, name='topic'),#topic_id的数值来自于topics中的遍历取id值
    #用于添加新主题的页面
    path('new_topic/', views.new_topic, name='new_topic'),
    #用于添加新条目的页面
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),#topic_id的数值来自于topics中的遍历取id值
    #用于编辑条目页面
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),#entry_id来自topic中的循环
]