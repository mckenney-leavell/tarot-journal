"""View module for handling requests about user spreads"""

# spread = id, user_id, created_date, interpretation
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from tarot_journal_api.models import Spread

class UserSpreadSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = User
        fields = ( 'id', 'first_name', 'last_name', )

class SpreadSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for user spreads"""
    user = UserSpreadSerializer(many=False)

    class Meta:
        model = Spread
        url = serializers.HyperlinkedIdentityField(
            view_name='spread',
            lookup_field='id'
        )
        fields = (
            'id', 
            'url',
            'user',
            'title',
            'created_date', 
            'interpretation',
        )

class Spreads(ViewSet):
    """View for interacting with user spreads"""

    def retrieve(self, request, pk=None):
        """
        @api {GET} /spread/:id GET single spread
        @apiName GetSpread
        @apiGroup Spreads

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611pbkdf2_sha256$150000$fHDURJBIASpx$trZS1MWc6YiNe5EYNBap+P+zMAwpNgNbUZH/b9bgvdw=

        @apiSuccess (200) {id} id Spread id
        @apiSuccess (200) {String} url Spread URI
        @apiSuccess (200) {String} user User URI
        @apiSuccess (200) {String} created_date Date spread was created
        @apiSuccess (200) {String} interpretation User's interpretation input
        

        @apiSuccessExample {json} Success
            {
                "id": 1,
                "url": "http://localhost:8000/spreads/1",
                "user": "http://localhost:8000/users/3",
                "title": "Career Spread",
                "created_date": "2025-12-01",
                "interpretation": "There are big changes coming your way--trust your intuition."
            }
        """
        try:
            user = request.auth.user
            spread = Spread.objects.get(pk=pk, user=user)
            serializer = SpreadSerializer(spread, context={"request": request})
            return Response(serializer.data)
        
        except Spread.DoesNotExist:
            return Response(
                {
                    "message": "The requested spread does not exist, or you do not have permission to access it."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        @api {GET} /spreads GET user spreads
        @apiName GetSpreads
        @apiGroup Spreads

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611pbkdf2_sha256$150000$fHDURJBIASpx$trZS1MWc6YiNe5EYNBap+P+zMAwpNgNbUZH/b9bgvdw=


        @apiSuccess (200) {id} id Spread id
        @apiSuccess (200) {String} url Spread URI
        @apiSuccess (200) {String} user User URI
        @apiSuccess (200) {String} created_date Date spread was created
        @apiSuccess (200) {String} interpretation User's interpretation input

        @apiSuccessExample {json} Success
            [
                {
                    "id": 1,
                    "url": "http://localhost:8000/spreads/1",
                    "user": "http://localhost:8000/users/3"
                    "title": "Career Spread"
                    "created_date": "2025-12-01",
                    "interpretation": "There are big changes coming your way--trust your intuition."
                }
            ]
        """
        user=request.auth.user
        spreads = Spread.objects.filter(user=user)

        json_spreads = SpreadSerializer(spreads, many=True, context={"request": request})

        return Response(json_spreads.data)

    def destroy(self, request, pk=None):
        """
            @api {DELETE} /spreads/:id DELETE product
            @apiName DeleteProduct
            @apiGroup Spread

            @apiHeader {String} Authorization Auth token
            @apiHeaderExample {String} Authorization
                Token 9ba45f09651c5b0c404f37a2d2572c026c146611pbkdf2_sha256$150000$fHDURJBIASpx$trZS1MWc6YiNe5EYNBap+P

            @apiParam {id} id Spread Id to delete
            @apiSuccessExample {json} Success
                HTTP/1.1 204 No Content
        """
        try:
            user = request.auth.user
            spread = Spread.objects.get(pk=pk, user=user)
            spread.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Spread.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# edit title, interpretation, or spreadcards, including deleting existing cards

    def update(self, request, pk=None):
        """
        @api {PUT} /spread/:id PUT changes for spread
        @apiName UpdateSpread
        @apiGroup Spreads

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611pbkdf2_sha256$150000$fHDURJBIASpx$trZS1MWc6YiNe5EYNBap+P

        @apiParam {id} id Spread Id route parameter

        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
                
        try:
            # user = request.auth.user
            spread = Spread.objects.get(pk=pk)
            spread.title = request.data["title"]
            spread.interpretation = request.data["interpretation"]

            spread.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Spread.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)