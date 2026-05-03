from django.views import generic
from .models import Project, Skill
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    JsonResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.shortcuts import get_object_or_404
from .forms import ProjectForm
from django.urls import reverse
import json


class ProjectList(generic.ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = Project.objects.all().order_by('-created_at')
        skill_name = self.request.GET.get('skill')
        if skill_name:
            queryset = queryset.filter(skills__name=skill_name).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_skills"] = Skill.objects.all()
        context["active_skill"] = self.request.GET.get('skill')
        return context


class ProjectDetail(generic.DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    pk_url_kwarg = 'project_id'
    context_object_name = 'project'


class ProjectCompleteView(LoginRequiredMixin, generic.View):

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        if project.owner == request.user and project.status == 'open':
            project.status = 'closed'
            project.save()
            return JsonResponse({"status": "ok", "project_status": "closed"})
        return HttpResponseForbidden()


class ProjectToggleParticipateView(LoginRequiredMixin, generic.View):

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        user = request.user
        if project.participants.filter(pk=user.pk).exists():
            project.participants.remove(user)
            participants = False
        else:
            project.participants.add(user)
            participants = True
        return JsonResponse({"status": "ok", "participant": participants})


class SkillAutocompleteView(generic.View):

    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse([], safe=False)
        skills = Skill.objects.filter(
            name__istartswith=query
        ).order_by('name')[:10]
        data = list(skills.values('id', 'name'))
        return JsonResponse(data, safe=False)


class SkillAddView(LoginRequiredMixin, generic.View):

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        if project.owner != request.user:
            return HttpResponseForbidden()
        skill_id = request.POST.get('skill_id')
        name = request.POST.get('name', '').strip()
        if not name and not skill_id and request.body:
            try:
                data = json.loads(request.body)
                skill_id = data.get('skill_id')
                name = data.get('name', '').strip() if data.get('name') else ''
            except json.JSONDecodeError:
                pass
        created = False
        added = False
        skill = None
        if skill_id:
            skill = get_object_or_404(Skill, pk=skill_id)
        elif name:
            skill, created = Skill.objects.get_or_create(name=name)
        if skill:
            if skill not in project.skills.all():
                project.skills.add(skill)
                added = True
        return JsonResponse({
            "id": skill.pk if skill else None,
            "created": created,
            "added": added,
            'name': skill.name if skill else None
        })


class SkillRemoveView(LoginRequiredMixin, generic.View):

    def post(self, request, project_id, skill_id):
        project = get_object_or_404(Project, pk=project_id)
        skill = get_object_or_404(Skill, pk=skill_id)
        if project.owner != request.user:
            return HttpResponseForbidden()
        if skill in project.skills.all():
            project.skills.remove(skill)
            return JsonResponse({"status": "ok", "id": skill.pk})
        return HttpResponseBadRequest()


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.participants.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse(
            'projects:project_detail',
            kwargs={'project_id': self.object.pk}
        )


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'
    pk_url_kwarg = 'project_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context

    def get_success_url(self):
        return reverse(
            'projects:project_detail',
            kwargs={'project_id': self.object.pk}
        )
