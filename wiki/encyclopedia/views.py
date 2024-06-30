from django.shortcuts import render
from markdown2 import Markdown
import random
from . import util

def convert_markdown(title):
    content = util.get_entry(title)
    md = Markdown()
    if content is None:
        return None
    else:
        return md.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = convert_markdown(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    
def search(request):
    query = request.POST['q']
    content = convert_markdown(query)
    if content is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": content
        })
    else:
        entries = util.list_entries()
        results = []
        for entry in entries:
            if query.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/search.html", {
            "results": results
        })
    
def new(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": "The page already exists."
            })
        else:
            util.save_entry(title, content)
            html_content = convert_markdown(title)
            return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
            })
    else:
        return render(request, "encyclopedia/new.html")
    
def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def saveEdit(request):
    title = request.POST['title']
    content = request.POST['content']
    util.save_entry(title, content)
    html_content = convert_markdown(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def randomEntry(request):
    entries = util.list_entries()
    title = random.choice(entries)
    content = convert_markdown(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })