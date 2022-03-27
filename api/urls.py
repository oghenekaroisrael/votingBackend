from django.urls import include, path
from . import views

urlpatterns = [
    path('candidate/create', views.add_candidate),
    path('candidate/candidate', views.get_candidates),
    path('candidate/candidate/<int:election_id>', views.get_candidates_by_election),
    path('candidate/delete/<int:candidate_id>', views.delete_candidate),
    path('candidate/update/<int:candidate_id>', views.update_candidate),
    path('poll/create', views.add_poll),
    path('poll/poll', views.get_polls),
    path('poll/delete/<int:poll_id>', views.delete_poll),
    path('poll/update/<int:poll_id>', views.update_poll),
    path('election/create', views.add_election),
    path('election/', views.get_elections),
    path('election/delete/<int:election_id>', views.delete_election),
    path('election/<int:election_id>', views.get_elections_by_id),
    path('vote/', views.vote),
    path('vote/result/<int:election_id>', views.get_votes)
]
