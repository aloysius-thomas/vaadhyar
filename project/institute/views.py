from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from institute.forms import ComplaintForm
from institute.forms import InterviewForm
from institute.forms import StudyMaterialForm
from institute.models import Complaint
from institute.models import Interview
from institute.models import StudyMaterial


@login_required
def interview_create_list_view(request):
    user = request.user
    if user.is_superuser:
        list_items = Interview.objects.all()
    elif user.user_type in ['trainer', 'trainee']:
        profile = user.get_profile
        list_items = Interview.objects.filter(course=profile.course)
    else:
        list_items = []
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Success")
            return redirect('interviews')
    else:
        form = InterviewForm()
    context = {
        'form': form,
        'title': 'Interviews',
        'list_items': list_items,
        'btn_text': "Add Interview",
    }
    return render(request, 'institute/interview-create-list.html', context)


@login_required()
def study_material_list_add_view(request, material_type):
    title = material_type.replace('-', ' ')
    title = title.title()
    user = request.user
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.material_type = material_type
            material.uploaded_by = request.user
            material.save()
            return redirect('study-materials', material_type)
    else:
        form = StudyMaterialForm()
    list_items = StudyMaterial.objects.filter(material_type=material_type)
    if user.user_type == 'teacher':
        profile = user.get_profile
        list_items = list_items.filter(subject=profile.subject)
    elif user.user_type == 'trainer':
        profile = user.get_profile
        list_items = list_items.filter(course=profile.course)
    elif user.user_type == 'student':
        profile = user.get_profile
        list_items = list_items.filter(subject=profile.subject)
    elif user.user_type == 'trainee':
        profile = user.get_profile
        list_items = list_items.filter(course=profile.course)
    else:
        list_items = list_items
    context = {
        'form': form,
        'title': title,
        'material_type': material_type,
        'list_items': list_items,
        'btn_text': f"Add {title}",
    }
    return render(request, 'institute/study-materials-create-list.html', context)


@login_required()
def complaint_create_list_view(request):
    user = request.user
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('', )
    else:
        form = ComplaintForm()
    list_items = Complaint.objects.filter(user=user)
    context = {
        'form': form,
        'title': "Register a Complaint",
        'list_items': list_items,
        'btn_text': f"New",
    }
    return render(request, 'institute/complaint-create-list.html', context)
