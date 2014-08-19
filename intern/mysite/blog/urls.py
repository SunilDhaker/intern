from django.conf.urls import patterns , include , urls
from django.views.generic import ListView
from blog.models import Post

urlpatterns = patterns('' , 
						url(r'^' ,ListView.as_view(
							queryset = Post.object.all()order_by"-date")[:10] ,
							template_name = "blog.html")),