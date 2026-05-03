from django.urls import path

from teamfn import views


app_name = 'projects'


urlpatterns = [
    path('list/', views.ProjectList.as_view(), name='project_list'),
    path('<int:project_id>/', views.ProjectDetail.as_view(),
         name='project_detail'),
    path('skills/', views.SkillAutocompleteView.as_view(),
         name='skill_autocomplete'),
    path('<int:project_id>/skills/add/', views.SkillAddView.as_view(),
         name='skill_add'),
    path('<int:project_id>/skills/<int:skill_id>/remove/',
         views.SkillRemoveView.as_view(),
         name='skill_remove'),
    path('create-project/', views.ProjectCreateView.as_view(),
         name='project_create'),
    path('<int:project_id>/edit/', views.ProjectUpdateView.as_view(),
         name='project_edit'),
    path('<int:project_id>/complete/', views.ProjectCompleteView.as_view(),
         name='complete'),
    path('<int:project_id>/toggle-participate/',
         views.ProjectToggleParticipateView.as_view(),
         name='participate'),
]
