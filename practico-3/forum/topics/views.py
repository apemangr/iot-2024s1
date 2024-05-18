from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Response 
from .forms import TopicForm, ResponseForm


def topic_list(request):
    topics = Topic.objects.all().order_by('-created_at')
    return render(request, 'topics/topic_list.html', {'topics': topics})

def topic_create(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('topic_list')
    else:
        form = TopicForm()
    return render(request, 'topics/topic_form.html', {'form': form})

def topic_detail(request, pk):
    topic = Topic.objects.get(pk=pk)
    responses = topic.responses.all().order_by('-created_at')
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.topic = topic
            response.save()
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = ResponseForm()
    return render(request, 'topics/topic_detail.html', {'topic': topic, 'responses': responses, 'form': form})

def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        topic.delete()
        return redirect('topic_list')
    return render(request, 'topics/topic_confirm_delete.html', {'topic': topic})