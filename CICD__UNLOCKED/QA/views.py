
from django.shortcuts import render

from QA.models import FAQ


# Create your views here.
def QA_Page(request):
    faqs = FAQ.objects.all()

    if request.method == 'POST':
       if request.POST.get('search_query'):
            search_query = request.POST.get('search_query')
            filtered_faqs = FAQ.objects.filter(question__icontains=search_query)

    context = {
        'faqs': faqs,
        'filtered_faqs': filtered_faqs if 'filtered_faqs' in locals() else None,
    }
    return render(request, 'QA_Page.html', context)


def handle_faq(request):

    if request.method == 'POST':
            if 'add_QA' in request.POST:
                # Handle adding a new FAQ
                question = request.POST.get('question')
                answer = request.POST.get('answer')
                FAQ.objects.create(question=question, answer=answer)
            if 'delete_QA' in request.POST:
                # Handle deleting an FAQ
                faq_id = request.POST.get('faq_id')
                FAQ.objects.filter(id=faq_id).delete()
            if 'update_QA' in request.POST:
                # Handle updating an FAQ
                faq_id = request.POST.get('faq_id')
                question = request.POST.get('question')
                answer = request.POST.get('answer')
                FAQ.objects.filter(id=faq_id).update(question=question, answer=answer)

    faqs = FAQ.objects.all()
    context= {
        'faqs': faqs
    }
    return render(request, 'LecturerPages/lecturer_manage_FAQ.html', context)