from django.conf.urls import patterns, url

urlpatterns = patterns(
    'knowledge.vote.views',

    url(r'^(?P<slug>[\w-]+)/((?P<vote>-?\d+))$', 'vote', name='vote'),
)
