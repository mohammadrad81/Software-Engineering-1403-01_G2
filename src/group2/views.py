from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TextSerializer
from .spell_checker import SpellChecker
from .tokenizer import PositionalTokenizer
from .candidate_generator import CandidateGenerator
from .language_model import OneGramLanguageModel

onegram_language_model = OneGramLanguageModel() ## load once and cache for performance

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

class TextSpellCorrectorAPIView(APIView):

    def post(self, request):
        serializer = TextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        candidate_generator = CandidateGenerator()
        positional_tokenizer = PositionalTokenizer()
        text = serializer.validated_data["text"]
        spell_checker = SpellChecker(tokenizer=positional_tokenizer,
                                     candidate_generator=candidate_generator,
                                     language_model=onegram_language_model)
        generated_suggestions = spell_checker.process_text(text=text)
        result = {
            "suggestions":[
                {
                    "start": start,
                    "end": end,
                    "word": word,
                    "candidates": candidates,
                }
                for start, end, word, candidates in generated_suggestions
            ]
        }
        return Response(data=result, status=status.HTTP_200_OK)