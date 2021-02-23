from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Enrty
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    #学习笔记的主页
    return render(request, 'learning_logs/index.html')
    
@login_required
def topics(request):
    #显示所有的主题
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    #显示单个主题以及其所有条目
    topic = get_object_or_404(Topic, id=topic_id)
    #确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.enrty_set.order_by('-date_added')
    context = {'topic': topic, 'entries':entries}
    #此处不是网址路径，而是文件存放路径
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    #添加新主题
    if request.method != 'POST':
    #未提交数据：创建一个新表单
        form = TopicForm()
    else:
    #POST提交的数据：对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user#设置用户
            new_topic.save()#存入数据库
            return redirect('learning_logs:topics')
            
    context={'form':form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    #在特定主题中添加新条目
    topic = get_object_or_404(Topic, id=topic_id)
    #确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
        
    if request.method != 'POST':
        #未提交数据：创建一个新表单
        form=EntryForm()
    else:
        #POST提交的数据：对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic#设置主题
            new_entry.save()#存入数据库
            return redirect('learning_logs:topic', topic_id=topic_id)
            
    context={'topic':topic,'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    #编辑既有的条目
    entry=get_object_or_404(Enrty, id=entry_id)
    topic = entry.topic
    #确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        #初次请求，使用当前条目填充表单
        form=EntryForm(instance=entry)
    else:
        #POST提交的数据：对数据进行处理
        form =EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context={'entry':entry,'topic':topic,'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)
    