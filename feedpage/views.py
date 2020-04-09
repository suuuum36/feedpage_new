from django.contrib.auth.models import User   
from django.shortcuts import render
from .models import Feed, FeedComment
from django.shortcuts import redirect

# Create your views here.

def index(request): # 원래 있던 index 함수 수정.
    if request.method == 'GET':
        feeds = Feed.objects.all()  #feed.objects.all = 모든 object
        context = {'feeds': feeds}
        return render(request, 'feedpage/index.html', context)

    elif request.method == 'POST': # create(form을 이용하여 submit한 형태) 
        title = request.POST['title']
        content = request.POST['content']
        Feed.objects.create(title=title, content=content, author = request.user)
        return redirect('/feeds')   # new에서 글을 만들고 저장하면 feeds에 추가되어 그 페이지로 가게 하기.

def new(request):
    return render(request, 'feedpage/new.html')

def show(request,id):
    feed=Feed.objects.get(id=id) #feed 중 그 id만을 가진 feed를 보여준다.
    context = {'feed':feed}
    return render(request, 'feedpage/show.html', context)

def edit(request, id):
    if request.method == 'GET':
        feed = Feed.objects.get(id=id)
        context = {'feed':feed}
        return render(request, 'feedpage/edit.html', context)

    elif request.method == 'POST':
        feed=Feed.objects.get(id=id)
        feed.title=request.POST['title']
        feed.content=request.POST['content']
        feed.save()
        feed.update_date()
        return redirect('/feeds/'+str(id)) 

def delete(request, id):
    feed = Feed.objects.get(id=id)
    feed.delete()
    return redirect('/feeds')

def delete_comment(request, id, cid):
    dComment = FeedComment.objects.get(id=cid) 
    dComment.delete()
    return redirect('/feeds')

def create_comment(request,id):
    content = request.POST['content']
    FeedComment.objects.create(feed_id=id, content=content, author = request.user)
    return redirect('/feeds')
