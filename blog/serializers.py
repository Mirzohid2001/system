from rest_framework import serializers
from .models import Category, Announcement, AnnouncementImage, Payment, Favorite, Comment, News, Message, Chat, Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image', 'alt_text']

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
    category = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'description', 'category',
            'condition', 'location', 'status',
            'plan', 'price', 'priority',
            'created_at', 'updated_at',
            'images', 'user'
        ]

    def get_category(self, obj):
        if obj.category:
            return {
                "id": obj.category.id,
                "name": obj.category.name,
                "image": obj.category.image.url if obj.category.image else None
            }
        return None

class AnnouncementCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Announcement
        fields = [
            'title', 'description', 'category',
            'condition', 'location', 'status',
            'plan', 'price',
            'images'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        announcement = Announcement.objects.create(**validated_data)
        for image_data in images_data:
            AnnouncementImage.objects.create(announcement=announcement, image=image_data)
        return announcement

    def to_representation(self, instance):
        return AnnouncementSerializer(instance, context=self.context).data

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

class CategoryDetailSerializer(serializers.ModelSerializer):
    announcements = AnnouncementSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'announcements']

class FavoriteSerializer(serializers.ModelSerializer):
    announcement_title = serializers.ReadOnlyField(source='announcement.title')
    announcement_images = AnnouncementImageSerializer(source='announcement.images', many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'announcement', 'announcement_title', 'announcement_images', 'created_at']
        read_only_fields = ['id', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    announcement_title = serializers.ReadOnlyField(source='announcement.title')

    class Meta:
        model = Comment
        fields = [
            'id', 'announcement', 'announcement_title',
            'user_name', 'text', 'rating', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user_name', 'announcement_title']

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(user=user, **validated_data)

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'created_at']
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
        fields = ['id', 'announcement', 'participants', 'messages', 'created_at']
