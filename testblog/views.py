from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse, resolve
from .models import * 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse

# Create your views here.
def index(request):
    print(request.user)
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(author=request.user, created_at__isnull=False)
        return render(request, "testblog/index.html", 
            {"blogs":  blogs}
     )

    else:
        return render(request, "testblog/login.html")



def drafts(request):
    if request.method == "GET":
        drafts = Blog.objects.all().filter(author=request.user, created_at__isnull=True)

        return render(request, "testblog/drafts.html", {'drafts': drafts})
    



def post_blog(request):
    
    if request.method == "GET":

        # if referer is '/blog_detail/{blog_id}' , render new_blog_post page with pre-populated draft values 
        print(request.META['HTTP_REFERER'])
        full_path = request.META['HTTP_REFERER']


        foo = urlparse(full_path)

        try:
            resolved_path = resolve(foo.path)
            print(foo)
            if foo.path == '/':
                return render(request, "testblog/new_blog.html")
            else:
                draft_id = resolved_path.kwargs['blog_id']
                print(draft_id)
                draft = Blog.objects.get(pk=draft_id)
                return render(request, "testblog/new_blog.html", {
                    "draft": draft,
                    'purpose': 'editing draft'
                })
        
        except Http404:
                return HttpResponseRedirect(reverse('index'))


        return render(request, "testblog/new_blog.html")
    else:

        title = request.POST.get('title')
        content = request.POST.get('content')
        submit = request.POST.get('submit')

        print(submit)
        blog = Blog.objects.create(author=request.user)      
        blog.title = title
        blog.content = content

        if submit == "post":
            
            blog.publish()
            blog.save()
            

        elif submit == "save as draft":
            
            blog.save()


        return HttpResponseRedirect(reverse('index'))



def blog_detail(request, blog_id):
    if request.method == "GET":

        #get the blog and pass it to the detail page
        try:
            blog = Blog.objects.get(pk=blog_id)
            print(f"blog created_at:= {blog.created_at}" )

            if blog.created_at == None:
                return render(request, "testblog/blog_detail.html",{
                    "draft": blog,
                    "purpose": "draft_detail"
                })

            else:
                return render(request, "testblog/blog_detail.html", {
                   "blog": blog,
                   "purpose": "blog_detail"
                
                })

        except Blog.DoesNotExist:
            return render(request, "testblog/blog_detail.html", {"message": "this blog does not exists!"})


def post_comments(request, blog_id):

    if request.method == "POST":
        content = request.POST.get("comment")

        blog = Blog.objects.get(pk=blog_id)

        comment = Comment.objects.create(blog=blog, written_by=request.user)
 
        comment.content = content
        comment.parent = None
        

        comment.save()

        return HttpResponseRedirect(reverse('detail', args=(blog_id,)))


def post_reply(request, blog_id):

    if request.method == "POST":
        content = request.POST.get("reply")
        parent_comment_id = request.POST.get("parent")

        parent_comment = Comment.objects.get(pk=parent_comment_id)
        blog = Blog.objects.get(pk=blog_id)

        #insert a comment
        reply = Comment.objects.create(blog=blog, written_by=request.user, parent=parent_comment)

        reply.content = content
        reply.save()

        return HttpResponseRedirect(reverse('detail', args=(blog_id,)))


@login_required(login_url="/login/")
def edit_blog(request, blog_id):
    if request.method == "GET":
        blog = Blog.objects.get(pk=blog_id)
        return render(request, "testblog/blog_detail.html", 
            {
                "blog": blog,
                "purpose": "edit"
            }
        )
    


def bookmarks(request):
    pass



def register(request):
    if request.method == "GET":
        return render(request, "testblog/register.html")
    else:

        try:

            first_name  = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = User.objects.create(username=username)

            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)

            user.save()

            #login the user
            login(request, user)

            return HttpResponseRedirect(reverse('index'))

        except KeyError:
            return render(request,"testblog/register.html", {"message": "some fields are empty!"})
        
        except IntegrityError:
            return render(request, "testblog/register.html", {"message": "user already exists!"})
        


def login_view(request):
    if request.method == "GET":
        return render(request, "testblog/login.html")
    else:

        try:
            username = request.POST.get("username")
            password = request.POST.get("password")

            print(username)
            

            usr = User.objects.filter(username=username)
            if(len(usr) != 0 and  not usr[0].check_password(password)):
                usr[0].set_password(password)

            print(usr[0].password)

            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, "testblog/login.html", {"message": "username/password not valid..."})


        except KeyError:
            return render(request, "testblog/login.html", {"message": "don't keep the fields empty!"})
            



def logout_view(request):
    logout(request) 
    return HttpResponseRedirect(reverse('index'))




