from django.db.models import fields
from rest_framework import serializers

from applications.review.models import Like, Review

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        # print(request.user)
        validated_data['user_id'] = request.user.id
        # print(request.user.id)
        review = Review.objects.create(**validated_data)
        return review

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('id')
        representation['user'] = f'{instance.user}'
        representation['like'] = instance.reviews.filter(like=True).count()
        return representation

