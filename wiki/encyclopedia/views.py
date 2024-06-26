from django.shortcuts import render
from markdown2 import Markdown
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