from django.urls import path
from wiki.views import PageListView , PageCreateView, PageDetailView


urlpatterns = [
    path('', PageListView.as_view(), name='wiki-list-page'),
    path('<str:slug>/', PageDetailView.as_view(), name='wiki-details-page'),
    path('create-post', PageCreateView.as_view(), name='page-create')
]
