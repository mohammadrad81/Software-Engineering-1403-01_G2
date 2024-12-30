from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


def home(request):
    return  render (request , 'group2.html' , {'group_number': '2'})

@ensure_csrf_cookie
def get_sentence(request):
    if request.method == 'POST':
        sentence = request.POST.get('sentence', '')
        # Process the sentence here
        result = {'message': f'Processed sentence: {sentence}'}
        return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request method'})

@ensure_csrf_cookie
def get_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file and file.name.endswith('.txt'):
            # Process the file here
            content = file.read().decode('utf-8')
            result = {'message': f'Processed file content: {content[:100]}...'}
            return JsonResponse(result)
        return JsonResponse({'error': 'Invalid file format'})
    return JsonResponse({'error': 'Invalid request method'})