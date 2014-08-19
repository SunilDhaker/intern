from django.http import HttpResponse , HttpResponseRedirect
from django.template import RequestContext , loader
from polls.models import Poll , Choice
from django.shortcuts import render , get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic



class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		return Poll.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'
	

class ResultView(generic.DetailView):
	moddel = Poll
	template_name = 'polls/results.html'

def vote(request , poll_id) : 
	p = get_object_or_404(Poll , pk = poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except(KeyError ,Choice.DoesNotExist):
		return render(request , 'polls/detail.html', {
			'poll':p,
			'error message' : "you didn't select a choice." ,
			})
	else :
		selected_choice.votes += 1
		selected_choice.save()

		return HttpResponseRedirect(reverse('polls:results' , args=( p.id )))