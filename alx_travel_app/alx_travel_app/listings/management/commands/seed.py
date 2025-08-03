from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from alx_travel_app.listings.models import Listing, Booking, Review
from decimal import Decimal
from datetime import date, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample listings, users, bookings, and reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--listings",
            type=int,
            default=10,
            help="Number of listings to create (default: 10)",
        )
        parser.add_argument(
            "--users",
            type=int,
            default=5,
            help="Number of users to create (default: 5)",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # Create sample users
        users_count = options["users"]
        users = self.create_users(users_count)
        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users"))

        # Create sample listings
        listings_count = options["listings"]
        listings = self.create_listings(listings_count, users)
        self.stdout.write(self.style.SUCCESS(f"Created {len(listings)} listings"))

        # Create sample bookings
        bookings = self.create_bookings(listings, users)
        self.stdout.write(self.style.SUCCESS(f"Created {len(bookings)} bookings"))

        # Create sample reviews
        reviews = self.create_reviews(listings, users)
        self.stdout.write(self.style.SUCCESS(f"Created {len(reviews)} reviews"))

        self.stdout.write(
            self.style.SUCCESS("Database seeding completed successfully!")
        )

    def create_users(self, count):
        """Create sample users"""
        users = []
        sample_users = [
            {
                "username": "john_doe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
            },
            {
                "username": "jane_smith",
                "email": "jane@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
            },
            {
                "username": "bob_wilson",
                "email": "bob@example.com",
                "first_name": "Bob",
                "last_name": "Wilson",
            },
            {
                "username": "alice_brown",
                "email": "alice@example.com",
                "first_name": "Alice",
                "last_name": "Brown",
            },
            {
                "username": "charlie_davis",
                "email": "charlie@example.com",
                "first_name": "Charlie",
                "last_name": "Davis",
            },
        ]

        for i in range(count):
            user_data = sample_users[i % len(sample_users)]
            username = (
                f"{user_data['username']}{i}"
                if i >= len(sample_users)
                else user_data["username"]
            )
            email = (
                f"{user_data['email'].split('@')[0]}{i}@example.com"
                if i >= len(sample_users)
                else user_data["email"]
            )

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                },
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        return users

    def create_listings(self, count, users):
        """Create sample listings"""
        listings = []
        sample_listings = [
            {
                "title": "Cozy Beach House",
                "description": "A beautiful beach house with stunning ocean views. Perfect for a relaxing getaway.",
                "location": "Malibu, CA",
                "price_per_night": Decimal("200.00"),
            },
            {
                "title": "Modern City Apartment",
                "description": "A sleek, modern apartment in the heart of downtown. Walking distance to all attractions.",
                "location": "New York, NY",
                "price_per_night": Decimal("150.00"),
            },
            {
                "title": "Mountain Cabin Retreat",
                "description": "Rustic cabin surrounded by nature. Great for hiking and outdoor activities.",
                "location": "Aspen, CO",
                "price_per_night": Decimal("180.00"),
            },
            {
                "title": "Luxury Villa with Pool",
                "description": "Spacious villa with private pool and garden. Perfect for families and groups.",
                "location": "Miami, FL",
                "price_per_night": Decimal("350.00"),
            },
            {
                "title": "Historic Downtown Loft",
                "description": "Charming loft in a historic building. Exposed brick walls and modern amenities.",
                "location": "Boston, MA",
                "price_per_night": Decimal("120.00"),
            },
            {
                "title": "Lakefront Cottage",
                "description": "Peaceful cottage on the lake shore. Fishing and kayaking available.",
                "location": "Lake Tahoe, CA",
                "price_per_night": Decimal("220.00"),
            },
            {
                "title": "Desert Oasis",
                "description": "Unique adobe-style home in the desert with panoramic views.",
                "location": "Sedona, AZ",
                "price_per_night": Decimal("190.00"),
            },
            {
                "title": "Ski Lodge Chalet",
                "description": "Cozy chalet near the ski slopes. Hot tub and fireplace included.",
                "location": "Park City, UT",
                "price_per_night": Decimal("280.00"),
            },
            {
                "title": "Tropical Paradise",
                "description": "Beachfront bungalow with private beach access. Snorkeling gear included.",
                "location": "Key West, FL",
                "price_per_night": Decimal("320.00"),
            },
            {
                "title": "Urban Studio",
                "description": "Compact but comfortable studio in trendy neighborhood. Great for solo travelers.",
                "location": "Portland, OR",
                "price_per_night": Decimal("80.00"),
            },
        ]

        for i in range(count):
            listing_data = sample_listings[i % len(sample_listings)]
            owner = random.choice(users)

            # Add variation to duplicate listings
            title = listing_data["title"]
            if i >= len(sample_listings):
                title += f" {i // len(sample_listings) + 1}"

            listing, created = Listing.objects.get_or_create(
                title=title,
                owner=owner,
                defaults={
                    "description": listing_data["description"],
                    "location": listing_data["location"],
                    "price_per_night": listing_data["price_per_night"],
                },
            )
            if created:
                listings.append(listing)

        return listings

    def create_bookings(self, listings, users):
        """Create sample bookings"""
        bookings = []

        for _ in range(min(15, len(listings) * 2)):  # Create up to 15 bookings
            listing = random.choice(listings)
            user = random.choice(
                [u for u in users if u != listing.owner]
            )  # User can't book their own listing

            # Generate random booking dates
            start_date = date.today() + timedelta(days=random.randint(1, 90))
            end_date = start_date + timedelta(days=random.randint(1, 14))
            guests = random.randint(1, 6)

            try:
                booking, created = Booking.objects.get_or_create(
                    listing=listing,
                    user=user,
                    start_date=start_date,
                    end_date=end_date,
                    defaults={"guests": guests},
                )
                if created:
                    bookings.append(booking)
            except Exception:
                # Skip if booking conflicts or other issues
                continue

        return bookings

    def create_reviews(self, listings, users):
        """Create sample reviews"""
        reviews = []
        sample_comments = [
            "Amazing place! Would definitely stay again.",
            "Great location and very clean. Highly recommended.",
            "Beautiful property with stunning views.",
            "Perfect for a weekend getaway.",
            "Host was very responsive and helpful.",
            "Exactly as described. No surprises.",
            "Lovely decor and comfortable beds.",
            "Great value for money.",
            "Peaceful and relaxing atmosphere.",
            "Would recommend to friends and family.",
        ]

        for listing in listings[:8]:  # Create reviews for first 8 listings
            # Random number of reviews per listing (1-3)
            num_reviews = random.randint(1, 3)

            for _ in range(num_reviews):
                user = random.choice([u for u in users if u != listing.owner])
                rating = random.randint(3, 5)  # Good ratings mostly
                comment = random.choice(sample_comments)

                try:
                    review, created = Review.objects.get_or_create(
                        listing=listing,
                        user=user,
                        defaults={
                            "rating": rating,
                            "comment": comment,
                        },
                    )
                    if created:
                        reviews.append(review)
                except Exception:
                    # Skip if review already exists or other issues
                    continue

        return reviews
