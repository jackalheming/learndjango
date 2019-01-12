from django.shortcuts import render
from .models import Topic
from .forms import TopicForm ,EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    #主页
    # 将请求的数据套用到模板中，然后返回给浏览器
    # 第一个参数是原始请求对象，第二是可用于创建网页的模板
    return render(request, "learning_logs/index.html")
    
def topics(request):
    #显示所有主题
    topics = Topic.objects.order_by('date_added')
    context = {'topics':topics}
    return render(request,'learning_logs/topics.html',context)

def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    # 通过Topic的id获得所有条目
    topic = Topic.objects.get(id=topic_id)
    # 前面的减号表示降序排序
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)

def new_topic(request):
    if request.method != 'POST':
        #未提交数据：创建一个新表单
        form = TopicForm()
    else:
        #POST数据提交时，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html',context)
def new_entry(request, topic_id):
    #在特定的主题中添加新条目
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #如果未提交数据
        form =EntryForm()
    else:
        #POST数据提交，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry =form.save(commit=False)
            new_entry.topic =topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html',context)

    

