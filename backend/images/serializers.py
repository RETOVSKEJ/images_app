from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import *


class ThumbnailSerializer(serializers.ModelSerializer):
    size = serializers.SlugRelatedField(slug_field='height', read_only=True)
    file = serializers.SerializerMethodField('get_file_url')

    class Meta:
        model = Thumbnail
        fields = ['size', 'file']
        read_only_fields = ['size', 'file']
    
    def get_file_url(self, obj):
        return f"http://127.0.0.1:8000/media/{obj.file}"

class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)
    # file = serializers.SerializerMethodField('get_image_file_url')

    class Meta:
        model = Image
        fields = '__all__'
        read_only_fields = ['owner']


    # def get_image_file_url(self, obj):
    #     return f"http://127.0.0.1:8000/media/{obj.file}"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context.get('request').user

        if not user.userprofile.tier.original_urls:
            data.pop('file')
        else:
            if data['file']:
                request = self.context.get('request')
                data['file'] = request.build_absolute_uri(f"/media/{instance.file}")

        return data

    def validate_owner(self, value):
        request = self.context.get('request')
        if value.user != request.user:
            raise ValidationError("You cannot choose another owner of an image")
        return value

    def validate_file(self, file):
        ACCEPTED_EXTENSIONS = ['image/png','image/jpeg']
        if file.size > 5 * 1024 * 1024:   # 5MB
            raise ValidationError("The Image is too big. 5MB is maximum")
        if file.content_type not in ACCEPTED_EXTENSIONS:
            raise ValidationError("The File is in the wrong format; only PNGs and JPGs are accepted")
        return file


