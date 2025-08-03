from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "location",
            "price_per_night",
            "owner",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]


class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "listing",
            "listing_id",
            "user",
            "start_date",
            "end_date",
            "guests",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate(self, data):
        """
        Validate that end_date is after start_date
        """
        if data["end_date"] <= data["start_date"]:
            raise serializers.ValidationError("End date must be after start date.")
        return data
