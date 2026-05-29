"""
Seed command — populates the database with sample data so every page renders
nicely on first run.

Usage:
    python manage.py seed
    python manage.py seed --flush   # wipes & re-seeds

Creates:
    1 admin user, 2 staff users, 3 customers,
    5 destinations, 4 categories, 8 tour packages,
    3 bookings (one of each status), 2 inquiries.
"""
import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from apps.tours.models import Destination, TourCategory, TourPackage, Review
from apps.bookings.models import Booking, Payment
from apps.inquiries.models import Inquiry, InquiryReply


class Command(BaseCommand):
    help = 'Populate the database with sample data for GlobeTrek Adventures.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Wipe all non-superuser data before seeding.',
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write(self.style.WARNING('Flushing existing data...'))
            Review.objects.all().delete()
            Payment.objects.all().delete()
            Booking.objects.all().delete()
            InquiryReply.objects.all().delete()
            Inquiry.objects.all().delete()
            TourPackage.objects.all().delete()
            TourCategory.objects.all().delete()
            Destination.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.NOTICE('=== GlobeTrek Adventures: Seeding sample data ==='))

        # ============== USERS ==============
        self.stdout.write('Creating users...')

        # Admin
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@globetrek.lk',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        admin.set_password('admin@1234')
        admin.save()
        admin.profile.role = 'admin'
        admin.profile.phone = '+94 31 222 3344'
        admin.profile.save()

        # Staff
        for i in range(1, 3):
            s, _ = User.objects.get_or_create(
                username=f'staff{i}',
                defaults={
                    'email': f'staff{i}@globetrek.lk',
                    'first_name': f'Staff{i}',
                    'last_name': 'Member',
                    'is_staff': True,
                },
            )
            s.set_password('staff@1234')
            s.save()
            s.profile.role = 'staff'
            s.profile.phone = f'+94 77 111 {1000 + i}'
            s.profile.save()

        # Customers
        customer_data = [
            ('customer1', 'Nimali', 'Perera', 'nimali@example.com'),
            ('customer2', 'Saman', 'Fernando', 'saman@example.com'),
            ('customer3', 'Anushka', 'Silva', 'anushka@example.com'),
        ]
        for username, first, last, email in customer_data:
            c, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first,
                    'last_name': last,
                },
            )
            c.set_password('cust@1234')
            c.save()
            c.profile.role = 'customer'
            c.profile.phone = f'+94 71 {random.randint(1000000, 9999999)}'
            c.profile.address = f'{random.randint(10, 999)} Colombo Road, Negombo'
            c.profile.save()

        self.stdout.write(self.style.SUCCESS('  ✓ Users created'))

        # ============== CATEGORIES ==============
        categories_data = [
            ('Adventure', 'bi-mountain'),
            ('Honeymoon', 'bi-heart'),
            ('Cultural', 'bi-bank'),
            ('Family', 'bi-people-fill'),
        ]
        categories = []
        for name, icon in categories_data:
            cat, _ = TourCategory.objects.get_or_create(
                name=name, defaults={'icon': icon},
            )
            categories.append(cat)

        # ============== DESTINATIONS ==============
        dest_data = [
            ('Maldives', 'Maldives', 'Crystal-clear lagoons, over-water bungalows, and world-class diving. The ultimate tropical escape.', True),
            ('Bali', 'Indonesia', 'Lush rice terraces, ancient temples, and vibrant beach clubs. Bali blends spirituality with paradise.', True),
            ('Paris', 'France', 'The city of lights — Eiffel Tower, the Louvre, charming cafés, and unforgettable cuisine.', True),
            ('Dubai', 'UAE', 'Futuristic skyscrapers, golden deserts, luxury shopping, and the iconic Burj Khalifa.', True),
            ('Nuwara Eliya', 'Sri Lanka', 'Cool climate, tea plantations, colonial architecture, and the famed Little England of Sri Lanka.', False),
        ]
        destinations = []
        for name, country, desc, feat in dest_data:
            d, _ = Destination.objects.get_or_create(
                name=name,
                defaults={'country': country, 'description': desc, 'featured': feat},
            )
            destinations.append(d)

        self.stdout.write(self.style.SUCCESS('  ✓ Destinations & categories created'))

        # ============== TOUR PACKAGES ==============
        packages_data = [
            {
                'title': 'Maldives Luxury Honeymoon Escape',
                'destination': destinations[0],
                'category': categories[1],
                'description': 'Six unforgettable nights in a private over-water villa with sunset cruises, candle-lit dinners on the beach, and personalised spa treatments. Includes return flights from CMB and all transfers.',
                'duration_days': 6,
                'price': Decimal('385000'),
                'max_travellers': 2,
                'includes': '5★ over-water villa accommodation\nAll meals + selected beverages\nReturn airport transfers (speedboat)\nSunset cruise + couples spa\nReturn flights from Colombo',
                'excludes': 'Travel insurance\nPersonal expenses\nVisa fees',
                'rating': Decimal('4.9'),
            },
            {
                'title': 'Bali Cultural Discovery (7 Days)',
                'destination': destinations[1],
                'category': categories[2],
                'description': 'Discover the spiritual heart of Bali — visit Ubud temples, learn traditional cooking, hike to Mount Batur for sunrise, and unwind on the beaches of Seminyak.',
                'duration_days': 7,
                'price': Decimal('220000'),
                'max_travellers': 12,
                'includes': '4★ boutique hotel stays\nDaily breakfast + 4 dinners\nEnglish-speaking guide\nAll entrance fees and transfers\nMount Batur sunrise trek',
                'excludes': 'International flights\nLunches on selected days',
                'rating': Decimal('4.7'),
            },
            {
                'title': 'Paris in Springtime (5 Days)',
                'destination': destinations[2],
                'category': categories[2],
                'description': 'Five magical days in the City of Lights. Skip-the-line passes for the Eiffel Tower and Louvre, Seine river cruise, day trip to Versailles, and authentic Parisian dining experiences.',
                'duration_days': 5,
                'price': Decimal('445000'),
                'max_travellers': 16,
                'includes': '4★ central Paris hotel\nDaily breakfast + 2 group dinners\nSkip-the-line museum passes\nVersailles day-trip\nMetro pass',
                'excludes': 'Flights\nLunches\nOptional excursions',
                'rating': Decimal('4.8'),
            },
            {
                'title': 'Dubai Desert & City Adventure',
                'destination': destinations[3],
                'category': categories[0],
                'description': 'Combine luxury and adrenaline — Burj Khalifa observation deck, Dubai Mall shopping, desert safari with dune-bashing, BBQ dinner under the stars, and a visit to the Palm Jumeirah.',
                'duration_days': 4,
                'price': Decimal('165000'),
                'max_travellers': 20,
                'includes': '4★ hotel near Dubai Mall\nDaily breakfast\nDesert safari with BBQ dinner\nBurj Khalifa entry\nReturn airport transfers',
                'excludes': 'Flights\nVisa\nLunch and other dinners',
                'rating': Decimal('4.6'),
            },
            {
                'title': 'Nuwara Eliya Tea Country Getaway',
                'destination': destinations[4],
                'category': categories[3],
                'description': 'Family weekend in the hill country. Visit a working tea factory, ride the famous blue train through misty hills, picnic at Gregory Lake, and stay in a colonial-era bungalow.',
                'duration_days': 3,
                'price': Decimal('45000'),
                'max_travellers': 8,
                'includes': 'Colonial bungalow stay\nAll meals\nTea factory tour\nTrain ride Kandy → Nuwara Eliya\nPrivate van + driver',
                'excludes': 'Personal expenses\nOptional pony rides',
                'rating': Decimal('4.5'),
            },
            {
                'title': 'Maldives Diving Adventure (5 Days)',
                'destination': destinations[0],
                'category': categories[0],
                'description': 'For certified divers — explore manta rays, whale sharks, and pristine coral reefs at world-renowned dive sites. 8 dives included with PADI instructors.',
                'duration_days': 5,
                'price': Decimal('295000'),
                'max_travellers': 6,
                'includes': '4★ resort accommodation\nAll meals\n8 boat dives\nDive equipment\nPADI dive master',
                'excludes': 'Dive insurance\nCertification courses',
                'rating': Decimal('4.7'),
            },
            {
                'title': 'Bali Family Beach Holiday',
                'destination': destinations[1],
                'category': categories[3],
                'description': 'Kid-friendly Bali — splash parks, Waterbom Bali, monkey forest, easy beach days at Nusa Dua, and a half-day visit to the elephant sanctuary.',
                'duration_days': 6,
                'price': Decimal('180000'),
                'max_travellers': 10,
                'includes': 'Family resort with kids club\nDaily breakfast + 3 family dinners\nWaterbom Bali tickets\nElephant sanctuary visit\nAll transfers',
                'excludes': 'International flights\nLunches\nExtra excursions',
                'rating': Decimal('4.6'),
            },
            {
                'title': 'Paris Romantic Weekend',
                'destination': destinations[2],
                'category': categories[1],
                'description': 'A romantic 3-night escape — Eiffel Tower dinner, sunset Seine cruise, Montmartre walking tour, and a couples cooking class with a Parisian chef.',
                'duration_days': 3,
                'price': Decimal('320000'),
                'max_travellers': 2,
                'includes': '4★ boutique hotel\nDaily breakfast\nEiffel Tower dinner\nSeine sunset cruise\nCouples cooking class',
                'excludes': 'Flights\nMost lunches and dinners',
                'rating': Decimal('4.9'),
            },
        ]

        today = date.today()
        for pd in packages_data:
            pd['available_from'] = today + timedelta(days=14)
            pd['available_to'] = today + timedelta(days=365)
            TourPackage.objects.get_or_create(
                title=pd['title'], defaults=pd,
            )

        self.stdout.write(self.style.SUCCESS('  ✓ Tour packages created'))

        # ============== BOOKINGS + PAYMENTS ==============
        customers = list(User.objects.filter(profile__role='customer'))
        packages = list(TourPackage.objects.all())
        statuses_to_create = ['pending', 'confirmed', 'completed']

        for i, status in enumerate(statuses_to_create):
            cust = customers[i % len(customers)]
            pkg = packages[i % len(packages)]
            travel = today + timedelta(days=30 + i * 20)
            num = random.choice([1, 2, 3])
            total = pkg.price * num

            booking, created = Booking.objects.get_or_create(
                customer=cust, package=pkg,
                defaults={
                    'travel_date': travel,
                    'num_travellers': num,
                    'total_price': total,
                    'status': status,
                    'payment_status': 'paid' if status != 'pending' else 'unpaid',
                    'special_requests': 'Vegetarian meals preferred.' if i == 0 else '',
                },
            )
            if created and status != 'pending':
                Payment.objects.create(
                    booking=booking,
                    amount=total,
                    payment_method='card',
                    status='completed',
                    paid_at=timezone.now() - timedelta(days=i * 5),
                )
            # Sample review on the completed booking
            if status == 'completed' and created:
                Review.objects.get_or_create(
                    customer=cust, package=pkg,
                    defaults={
                        'rating': 5,
                        'comment': 'Absolutely fantastic experience! The GlobeTrek team handled everything perfectly.',
                    },
                )

        self.stdout.write(self.style.SUCCESS('  ✓ Bookings & payments created'))

        # ============== INQUIRIES ==============
        inquiries_data = [
            {
                'name': 'Ravi Kumar',
                'email': 'ravi@example.com',
                'phone': '+94 71 555 1234',
                'subject': 'Question about Bali Cultural Discovery',
                'message': 'Hello, I am interested in the Bali Cultural Discovery tour. Could you let me know if vegetarian meals are available throughout the trip? Also, what is the typical group size?',
                'customer': customers[0],
                'status': 'in_progress',
            },
            {
                'name': 'Sahan Bandara',
                'email': 'sahan@example.com',
                'subject': 'Group booking discount?',
                'message': 'We are a group of 12 looking to book the Dubai package for a corporate trip. Do you offer group discounts? Looking forward to hearing from you.',
                'customer': customers[1] if len(customers) > 1 else None,
                'status': 'open',
            },
        ]
        for d in inquiries_data:
            inq, created = Inquiry.objects.get_or_create(
                subject=d['subject'], email=d['email'], defaults=d,
            )
            # Add a sample staff reply on the in-progress one
            if created and d['status'] == 'in_progress':
                staff = User.objects.filter(profile__role='staff').first()
                InquiryReply.objects.create(
                    inquiry=inq, staff=staff,
                    reply='Hi Ravi, thanks for your interest! Vegetarian meals are absolutely available throughout the tour — we work with restaurants known for excellent veg options. Typical group size is 8-12 travellers. Let us know if you have any other questions!',
                )

        self.stdout.write(self.style.SUCCESS('  ✓ Inquiries created'))

        # ============== DONE ==============
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== ✓ Seeding complete! ==='))
        self.stdout.write('')
        self.stdout.write('You can now log in with any of these test accounts:')
        self.stdout.write(self.style.NOTICE('  Admin    →  admin       /  admin@1234'))
        self.stdout.write(self.style.NOTICE('  Staff    →  staff1      /  staff@1234'))
        self.stdout.write(self.style.NOTICE('  Customer →  customer1   /  cust@1234'))
        self.stdout.write('')
        self.stdout.write('Run the server: python manage.py runserver')
