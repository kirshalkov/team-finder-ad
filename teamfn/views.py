import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from core.constants import (
    AUTOCOMPLETE_LIMIT,
    PAGINATION_VALUE,
    STATUS_CLOSED,
    STATUS_OPEN,)

from teamfn.forms import ProjectForm
from teamfn.models import Project, Skill


class ProjectList(generic.ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = PAGINATION_VALUE

    def get_queryset(self):
        queryset = Project.objects.select_related(
            'owner').prefetch_related(
                'skills').order_by('-created_at')
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

    def get_queryset(self):
        return Project.objects.select_related(
            'owner').prefetch_related('skills')


class ProjectCompleteView(LoginRequiredMixin, generic.View):

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        if project.owner == request.user and project.status == STATUS_OPEN:
            project.status = STATUS_CLOSED
            project.save()
            return JsonResponse({"status": "ok",
                                 "project_status": STATUS_CLOSED})
        return HttpResponseForbidden()


class ProjectToggleParticipateView(LoginRequiredMixin, generic.View):

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        user = request.user

        if is_participant := project.participants.filter(pk=user.pk).exists():
            project.participants.remove(user)
        else:
            project.participants.add(user)

        return JsonResponse({"status": "ok",
                             "participant": not is_participant})


class SkillAutocompleteView(generic.View):

    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse([], safe=False)
        skills = Skill.objects.filter(
            name__istartswith=query
        ).order_by('name')[:AUTOCOMPLETE_LIMIT]
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
            if not project.skills.filter(pk=skill.pk).exists():
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
        if project.skills.filter(pk=skill.pk).exists():
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
