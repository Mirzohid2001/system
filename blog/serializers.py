from rest_framework import serializers
from .models import Category, Announcement, AnnouncementImage ,Payment,Favorite,Comment,News,Message,Chat
from django.core.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category   
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        return CategoryTreeSerializer(obj.children.all(), many=True).data

class AnnouncementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementImage
        fields = ['id', 'image']


class AnnouncementSerializer(serializers.ModelSerializer):
    images = AnnouncementImageSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'description', 'category',
            'condition', 'location', 'status',
            'plan','price', 'priority', 'created_at', 'updated_at',
            'images', 'user'
        ]


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Announcement
        fields = [
            'title', 'description', 'category',
            'condition', 'location', 'status',
            'plan','price',
            'images'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        announcement = Announcement.objects.create(**validated_data)
        for image_data in images_data:
            AnnouncementImage.objects.create(announcement=announcement, image=image_data)
        return announcement

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for image_data in images_data:
            AnnouncementImage.objects.create(announcement=instance, image=image_data)
        return instance



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'announcement', 'plan', 'amount', 'payment_id', 'paid', 'created_at']
        read_only_fields = ['id', 'amount', 'payment_id', 'paid', 'created_at']

    def validate_announcement(self, announcement):
        user = self.context['request'].user
        if announcement.user != user:
            raise serializers.ValidationError("Вы можете оплатить только своё объявление.")
        return announcement

    def create(self, validated_data):
        plan = validated_data['plan']
        validated_data['amount'] = plan.amount
        return super().create(validated_data)

    
class FavoriteSerializer(serializers.ModelSerializer):
    announcement_title = serializers.ReadOnlyField(source='announcement.title')

    class Meta:
        model = Favorite
        fields = ['id', 'announcement', 'announcement_title', 'created_at']
        read_only_fields = ['id', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    announcement_title = serializers.ReadOnlyField(source='announcement.title')

    class Meta:
        model = Comment
        fields = [
            'id', 
            'announcement', 
            'announcement_title', 
            'user_name',
            'text', 
            'rating', 
            'created_at'
        ]
        read_only_fields = [
            'id', 
            'created_at', 
            'user_name', 
            'announcement_title'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        comment = Comment.objects.create(user=user, **validated_data)
        return comment

    
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content','image', 'created_at']
        read_only_fields = ['id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'created_at']


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = Chat
        fields = ['id', 'announcement', 'product', 'participants', 'messages', 'created_at']










