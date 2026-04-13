# documents/serializers.py  (create this file)

from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    # ModelSerializer works like ModelForm —
    # it reads your model and auto-creates fields for you

    owner = serializers.ReadOnlyField(source="owner.username")
    # ReadOnlyField means this field is included in responses
    # but ignored on create/update — users can't fake who the owner is
    # source="owner.username" means: follow the owner ForeignKey
    # and return the username string instead of the user's pk number

    conversion_type_display = serializers.CharField(
        source="get_conversion_type_display",
        read_only=True
    )
    # source="get_conversion_type_display" calls that Django method
    # which returns "Word to PDF" instead of "word_to_pdf"
    # This is a computed field — it's not a real model field
    # read_only=True because you can't set it directly

    converted_file_url = serializers.SerializerMethodField()
    # SerializerMethodField lets you add any custom computed value
    # DRF will call get_converted_file_url() automatically

    def get_converted_file_url(self, obj):
        # obj is the Document instance being serialized
        # This method returns the full URL of the converted file
        if obj.converted_file:
            request = self.context.get("request")
            # self.context["request"] gives access to the HTTP request
            # We need it to build an absolute URL
            if request:
                return request.build_absolute_uri(obj.converted_file.url)
        return None
        # Return None if no converted file exists yet

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "owner",
            "conversion_type",
            "conversion_type_display",
            "converted",
            "converted_file_url",
            "created_at",
        ]
        read_only_fields = ["id", "owner", "converted", "created_at"]
        # read_only_fields are included in responses
        # but ignored if the client tries to set them
        # Users can't manually set their own id or mark converted=True
