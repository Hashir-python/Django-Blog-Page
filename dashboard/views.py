from django.shortcuts import render
from blogs.models import Category,Blog
from blogs.models import Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm,BlogForm
from django.shortcuts import redirect
from django.utils.text import slugify
from django.shortcuts import render,redirect,get_object_or_404


# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    Categories_count=Category.objects.all().count()
    Blogs_count=Blog.objects.all().count
    context={
        'Categories_count':Categories_count,
        'Blogs_count':Blogs_count
    }
    return render(request,'dashboard/dashboard.html',context)

def categories(request):
    return render(request,'dashboard/categories.html')

def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
        
    form=CategoryForm()
    context={
        'form':form,
    }
    return render(request,'dashboard/add_category.html',context)


def edit_category(request,pk):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category,
    }
    return render(request,'dashboard/edit_category.html',context)

def delete_category(request,pk):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    return redirect('categories')
    

def posts(request):
    posts=Blog.objects.all()
    context={
        'posts':posts
    }
    return render(request,'dashboard/posts.html',context)


def add_post(request):
    if request.method=='POST':
        form=BlogForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False) # Temporary Save the data
            post.author=request.user
            post.save()
            title=form.cleaned_data['title']+'-'+str(post.id)
            post.slug=slugify(title)
            post.save()
            return redirect('posts')
        else:
            print('error found')
            print(form.errors)
    form=BlogForm()
    context={
        'form':form
    }
    return render(request,'dashboard/add_post.html',context)

def edit_post(request,pk):
    post=get_object_or_404(Blog,pk=pk)
    if request.method=='POST':
        form=BlogForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save()
            title=form.cleaned_data['title']
            post.slug=slugify(title)+'-'+str(post.id)
            post.save()
            return redirect('posts')
    form=BlogForm(instance=post)
    context={
        'form':form,
        'post':post,
    }
    return render(request,'dashboard/edit_post.html',context)

def delete_post(request,pk):
    post=get_object_or_404(Blog,pk=pk)
    post.delete()
    return redirect('posts')