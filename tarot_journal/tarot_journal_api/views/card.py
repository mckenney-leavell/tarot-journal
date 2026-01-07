from rest_framework import serializers
from tarot_journal_api.models import Card, Element, Value
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseServerError

class ElementSerializer(serializers.ModelSerializer):
    """JSON serializer for elements"""
    class Meta:
        model = Element
        fields = "__all__"

class ValueSerializer(serializers.ModelSerializer):
    """JSON serializer for values"""
    class Meta:
        model = Value
        fields = "__all__"

class CardSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for cards"""
    element = ElementSerializer(many=False)
    value = ValueSerializer(many=False)

    class Meta:
        model = Card
        fields = ( 'id', 'name', 'major_arcana', 'meaning_upright', 'meaning_reverse', 'element', 'value', 'url' ) 

class Cards(ViewSet):
    """View for interacting with cards"""

    def list(self, request):
        """
        @api {GET} /cards GET cards
        @apiName GetCards
        @apiGroup Cards

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611pbkdf2_sha256$150000$fHDURJBIASpx$trZS1MWc6YiNe5EYNBap+P+zMAwpNgNbUZH/b9bgvdw=

        @apiSuccessExample {json} Success
            [
                {
                    "id": 1,
                    "url": "http://localhost:8000/cards/1",
                    "user": "http://localhost:8000/users/3"
                    "title": "Career Spread"
                    "created_date": "2025-12-01",
                    "interpretation": "There are big changes coming your way--trust your intuition.",
                    "url": "url.example"
                }
            ]
        """
        try:
            card = Card.objects.all()
            serializer = CardSerializer(card, many=True, context={"request": request})

            return Response(serializer.data)
        
        except Card.DoesNotExist:
            return Response(
                {
                    "message": "The requested spread does not exist, or you do not have permission to access it."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        
        except Exception as ex:
            return HttpResponseServerError(ex)