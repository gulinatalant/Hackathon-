from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Comment, Rating, Like


class CommentSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = self.Meta.model.objects.create(author=user, **validated_data)
        return comment


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, rating):
        if rating > 10:
            raise serializers.ValidationError(
                'Rating can\'t be more than 10'
            )
        return rating

    def create(self, validated_data):
        user = self.context.get('request').user
        rating = self.Meta.model.objects.create(author=user, **validated_data)
        return rating


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        like = self.Meta.model.objects.create(author=user, **validated_data)
        return like

    def validate(self, attrs):
        event = attrs.get('event')
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(event=event, author=user).exists():
            raise serializers.ValidationError('You already liked it')
        return attrs