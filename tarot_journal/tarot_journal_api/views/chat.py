from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseServerError
from django.conf import settings
import json
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def chat(request):
    """Function making request to OpenAI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('input')

            completion = client.chat.completions.create(
                model="gpt-5-nano",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            ai_reply = completion.choices[0].message.content

            return Response({'reply': ai_reply}, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
