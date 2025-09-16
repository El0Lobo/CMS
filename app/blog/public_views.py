from django.shortcuts import render
def blog_index(request): return render(request,'blog/public_list.html', {'posts':[{'title':'Welcome','slug':'welcome'}]})