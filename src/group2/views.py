from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TextSerializer
from group2.utils.spell_checker import SpellChecker
from group2.utils.tokenizer import PositionalTokenizer
from group2.nlp.candidate_generator import CandidateGenerator
from group2.nlp.language_model import OneGramLanguageModel

onegram_language_model = OneGramLanguageModel() ## load once and cache for performance


def process(text):
    tokenizer = PositionalTokenizer()
    candidate_generator = CandidateGenerator()
    language_model = OneGramLanguageModel()
    spell_checker = SpellChecker(tokenizer, candidate_generator, language_model)

    corrections = spell_checker.process_text(text)

    corrected_text = text
    offset = 0
    for start, end, word, candidates in corrections:
        if candidates:
            replacement = candidates[0]
            corrected_text = corrected_text[:start + offset] + replacement + corrected_text[end + offset:]
            offset += len(replacement) - (end - start)

    formatted_corrections = []
    for start, end, word, candidates in corrections:
        formatted_corrections.append({
            'start': start,
            'end': end,
            'word': word,
            'candidates': candidates
        })

    return JsonResponse({
        'input_text': text,
        'corrections': formatted_corrections,
        'correctedText': corrected_text  # Add corrected text to the response
    })

def home(request):
    return  render (request , 'group2.html' , {'group_number': '2'})

@ensure_csrf_cookie
def get_sentence(request):
    if request.method == 'POST':
        sentence = request.POST.get('sentence', '')

        return process(sentence)
    return JsonResponse({'error': 'Invalid request method'})


@ensure_csrf_cookie
def get_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file and file.name.endswith('.txt'):
            # Process the file here
            content = file.read().decode('utf-8')

            return process(content)
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