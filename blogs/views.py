from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import EntryForm

def index(request):
    return render(request, 'blogs/index.html')

def about(request):
    return render(request, 'blogs/about.html')

def topics(request):
    '''Display all topics.'''
    return render(request, 'blogs/topics.html', {'topics': Topic.objects.order_by('name')})

def topic(request, slug):
    '''Display all public entries within a specific topic.'''
    topic = Topic.objects.get(slug=slug)
    entries = topic.entry_set.filter(public=True).order_by('-date_added')
    context = {
        'topic': topic,
        'entries': entries,
    }
    return render(request, 'blogs/topic.html', context)

def entry_detail(request, slug):
    entry = Entry.objects.get(slug=slug)
    if request.user.username != entry.owner.username and entry.public == False:
        raise Http404
    return render(request, 'blogs/entry_detail.html', {'entry': entry})

def user_entries(request, username):
    '''Display all entries (public and private) of an user for authenticated author user, public entries otherwise.'''
    if request.user.is_authenticated and request.user.username == username:
        filter_option = request.META.get('QUERY_STRING')
        # Check if there is any option
        if filter_option:
            filter_option = filter_option.split('=')
            # Check if the option is filter
            if filter_option[0] == 'filter':
                # Return public entries if filter == 'public', private entries if filter == 'private'
                if filter_option[1] == 'public':
                    filter_option = True
                elif filter_option[1] == 'private':
                    filter_option = False
                else:
                    filter_option = None
            else:
                filter_option = None
        else:                
            filter_option = None

        if filter_option is None:
            entries = Entry.objects.filter(owner__username=username).order_by('-date_added')
        else:
            entries = Entry.objects.filter(owner__username=username, public=filter_option).order_by('-date_added')
    else:
        entries = Entry.objects.filter(owner__username=username, public=True).order_by('-date_added')
    context = {
        'entries': entries,
        'author': username,
    }
    return render(request, 'blogs/user_entries.html', context)

@login_required
def new_entry(request, slug):
    '''Add a new entry.'''
    topic = Topic.objects.get(slug=slug)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.slug = form.cleaned_data.get('slug')
            new_entry.save()
            return redirect('blogs:topic', slug=slug)
        
    # Display blank or invalid form.
    context = {
        'topic': topic,
        'form': form,
    }
    return render(request, 'blogs/new_entry.html', context)

@login_required
def edit_entry(request, slug):
    '''Edit an entry.'''
    entry = Entry.objects.get(slug=slug)
    topic = entry.topic
    if entry.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # Pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            if 'title' in form.changed_data:
                edited_entry = form.save(commit=False)
                edited_entry.slug = form.cleaned_data.get('slug')
                edited_entry.save()
            else:
                form.save()
            return redirect('blogs:user_entries', username=entry.owner.username)
    
    context = {
        'entry': entry,
        'form': form,
    }
    return render(request, 'blogs/edit_entry.html', context)

@login_required
def delete_entry(request, slug):
    '''Delete an entry.'''
    entry = Entry.objects.get(slug=slug)
    topic = entry.topic
    if entry.owner != request.user:
        raise Http404
    if request.method != 'POST':
        return redirect('blogs:topic', slug=topic.slug)
    entry.delete()
    return redirect('blogs:user_entries', username=entry.owner.username)