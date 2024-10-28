from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import Consultation
from .forms import ConsultationForm
import importlib 

def consultation_list(request):
    consultations = Consultation.objects.all()
    return render(request, 'consultation/consultation_list.html', {'consultations': consultations})

# def consultation_detail(request, pk):
#     consultation = get_object_or_404(Consultation, pk=pk)
#     return render(request, 'consultation/consultation_detail.html', {'consultation': consultation})

def consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    
    summarizer_module = importlib.import_module("Consultation.summarizer")
    generate_summary = getattr(summarizer_module, "generate_summary")
    
    summary = generate_summary(consultation.notes)

    return render(request, "consultation/consultation_detail.html", {
        "consultation": consultation,
        "summary": summary,
    })


def consultation_create(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultation_list')
    else:
        form = ConsultationForm()
    return render(request, 'consultation/consultation_form.html', {'form': form})

def consultation_update(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            return redirect('consultation_list')
    else:
        form = ConsultationForm(instance=consultation)
    return render(request, 'consultation/consultation_form.html', {'form': form})

def consultation_delete(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        consultation.delete()
        return redirect('consultation_list')
    return render(request, 'consultation/consultation_confirm_delete.html', {'consultation': consultation})

