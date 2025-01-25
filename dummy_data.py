import os , django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


import random
from faker import Faker
from django.contrib.auth.models import User
from graduation_project.models import GraduationProject, Category, Review

# Initialize Faker
fake = Faker()

def seed_users(n):
    """Create dummy users."""
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = 'password123'  # Default password for dummy users
        User.objects.create_user(username=username, email=email, password=password)
    print(f"Seeded {n} users successfully.")




def seed_categories(n):
    """Create dummy categories."""
    for _ in range(n):
        Category.objects.create(
            name=fake.word(),
            description=fake.text(max_nb_chars=200)
        )
    print(f"Seeded {n} categories successfully.")

def seed_projects(n):
    """Create dummy graduation projects."""
    categories = Category.objects.all()
    users = User.objects.all()


    dummy_images = [
        "dummy_images_books/2.jpg",
        "dummy_images_books/1.jpg",
        "dummy_images_books/3.jpg",
        "dummy_images_books/4.jpg",
        "dummy_images_books/5.jpeg",
        "dummy_images_books/6.jpg",
        "dummy_images_books/7.jpg",
        "dummy_images_books/8.jpeg",
        "dummy_images_books/9.jpg",
    ]

    for _ in range(n):
        GraduationProject.objects.create(
            title=fake.sentence()[:50],  # Truncate the title to 50 characters            description=fake.text(max_nb_chars=1000),
            sub_description=fake.text(max_nb_chars=500),
            graduation_year=random.randint(2010, 2025),
            status=random.choice(['pending', 'accepted', 'rejected']),
            doctor=random.choice(users.filter(profile__is_doctor=True)),
            category=random.choice(categories),
            book_pdf=None,  # You can add logic to upload dummy PDFs if needed
            images=random.choice(dummy_images),  # Assign a random image

            # images=None,  # You can add logic to upload dummy images if needed
            video=fake.url(),
            view_count=random.randint(0, 600),
        )
    print(f"Seeded {n} graduation projects successfully.")


def seed_reviews(n):
    """Create dummy reviews."""
    projects = GraduationProject.objects.all()
    users = User.objects.all()

    for _ in range(n):
        Review.objects.create(
            project=random.choice(projects),
            reviewer=random.choice(users),
            comments=fake.text(max_nb_chars=500),
            rating=random.randint(1, 5)
        )
    print(f"Seeded {n} reviews successfully.")



def seed_all():
    """Seed all data."""
    # seed_users(10)  # Create 10 dummy users
    # seed_categories(5)  # Create 5 dummy categories
    seed_projects(500)  # Create 20 dummy projects
    seed_reviews(200)  # Create 50 dummy reviews
    print("All data seeded successfully.")

# Run the seeding process
if __name__ == "__main__":
    seed_all()