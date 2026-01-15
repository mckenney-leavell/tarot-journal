# from rest_framework.response import Response
# from rest_framework import status
# # from django.http import HttpResponseServerError
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# import json
# from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_exempt
def chat(request):
    """Function making request to OpenAI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message')

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            ai_reply = completion.choices[0].message.content

            return JsonResponse({'reply': ai_reply})

        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=500)
