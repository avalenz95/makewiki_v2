from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from wiki.models import Page
from wiki.forms import PageForm


class PageListView(ListView):
    """ Renders a list of all Pages. """
    model = Page

    def get(self, request):
        """ GET a list of Pages. """
        #pages = Page.objects.order_by('-created')
        #pages = Page.objects.order_by('created'.desc())
        pages = self.get_queryset().all().order_by('-created')
        #pages = self.get_queryset().all()
        return render(request, 'list.html', {
          'pages': pages
        })

class PageDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Page

    def get(self, request, slug):
        """ Returns a specific wiki page by slug. """
        page = self.get_queryset().get(slug__iexact=slug)
        
        return render(request, 'page.html', {
          'page': page
        })


#Page Create view sends the post request
class PageCreateView(CreateView):

  #user wants to submit form
  def get(self, request, *args, **kwargs):
      #get form
      context = {'form': PageForm()}
      #pass form to wiki/newpage and render template
      return render(request, 'newpage.html', context)

  #user has submitted form
  def post(self, request, *args, **kwargs):
      #form submitted via post request
      form = PageForm(request.POST)
      #form validation check
      if form.is_valid():
          #save form
          page = form.save()

          #redirect the user to home 
          return HttpResponseRedirect(reverse_lazy('wiki-list-page'))

      #render the form again if it is not valid
      return render(request, 'newpage.html', {'form': form})
