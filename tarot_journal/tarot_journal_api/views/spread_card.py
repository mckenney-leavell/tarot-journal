from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from tarot_journal_api.models import SpreadCard, Spread, Card

class CardSerializer(serializers.ModelSerializer):
    """JSON serializer for cards"""

    class Meta:
        model = Card
        url = serializers.HyperlinkedIdentityField(
            view_name="card", lookup_field="id"
        )
        fields = "__all__"

class SpreadCardSerializer(serializers.ModelSerializer):
    """JSON serializer"""
    card = CardSerializer(many=False)

    class Meta:
        model = SpreadCard
        fields = ( 'id', 'card', 'spread' )

class SpreadCards(ViewSet):
    """View for interacting with spread cards"""
    def destroy(self, request, pk=None):
        """
            @api {DELETE} /spreadcards/:id DELETE spreadcard
            @apiName DeleteSpreadCard
            @apiGroup SpreadCard

            @apiHeader {String} Authorization Auth token
            @apiHeaderExample {String} Authorization
                Token 9ba45f09651c5b0c404f37a2d2572c026c146611pbkdf2_sha256$150000$fHDURJBIASpx$trZS1MWc6YiNe5EYNBap+P

            @apiParam {id} id SpreadCard Id to delete
            @apiSuccessExample {json} Success
                HTTP/1.1 204 No Content
        """
        try:
            spread_card = SpreadCard.objects.get(pk=pk)
            spread_card.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except SpreadCard.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request):
        """
        @api {POST} /spread_card POST new spread_card
        @apiName CreateSpreadCard
        @apiGroup SpreadCard

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611pbkdf2_sha256$150000$fHDURJBIASpx$trZS1MWc6YiNe5EYNBap+P

        @apiSuccess (200) {Object} spread_card Created spread_card
        @apiSuccess (200) {id} spread_card.id spread_card Id
        @apiSuccess (200) {Object} spread_card.spread Spread of spread_card
        @apiSuccess (200) {Object} spread_card.card Card of spread_card
        @apiSuccessExample {json} Success
            {
                "id": 12,
                "url": "http://localhost:8000/spread_cards/12",
                "spread_id": 1
                "card_id": 16
            }                

        """

        new_spread_card = SpreadCard()
        
        spread = Spread.objects.get(pk=request.data["spread_id"])
        new_spread_card.spread = spread

        card = Card.objects.get(pk=request.data["card_id"])
        new_spread_card.card = card

        new_spread_card.save()

        serializer = SpreadCardSerializer(new_spread_card, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)