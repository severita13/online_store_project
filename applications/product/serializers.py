from django.db import models
from django.db.models import fields
from rest_framework import serializers
from applications.product.models import Product, ProductImage
from applications.review.serializers import ReviewSerializer


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image', )

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            # print(url)
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
                print(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.review.all())
        total_rating = [i.rating for i in instance.review.all()]
        # print(total_rating)
        if len(total_rating) > 0:
            representation['total_rating'] = sum(total_rating) / len(total_rating)
        representation['images'] = ProductImageSerializer(ProductImage.objects.filter(product=instance.id), many=True, context=self.context).data
        return representation


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total_rating = [i.rating for i in instance.review.all()]
        if len(total_rating) > 0:
            representation['total_rating'] = sum(total_rating) / len(total_rating)
        representation['images'] = ProductImageSerializer(ProductImage.objects.filter(product=instance.id), many=True, context=self.context).data
        representation['reviews'] = ReviewSerializer(instance.review.filter(product=instance.id), many=True).data
        return representation