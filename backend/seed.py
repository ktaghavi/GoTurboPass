#!/usr/bin/env python3
"""
Seed script for Phase 1 demo data.

Creates:
- Admin user (admin@goturbopass.com / admin123)
- Reviewer user (reviewer@goturbopass.com / reviewer123)
- 2 sample modules with quizzes
"""
from datetime import datetime, date
from app import create_app
from models import db
from models.user import User, UserRole
from models.module import Module
from models.quiz import Quiz, Question
from services.auth_service import AuthService


def seed_database():
    """Seed demo data."""
    app = create_app()

    with app.app_context():
        print("🌱 Seeding database...")

        # Clear existing data (dev only!)
        print("  Clearing existing data...")
        db.drop_all()
        db.create_all()

        # 1. Create Admin user
        print("  Creating Admin user...")
        admin = User(
            role=UserRole.ADMIN,
            email='admin@goturbopass.com',
            email_verified_at=datetime.utcnow(),
            password_hash=AuthService.hash_password('admin123'),
            full_name='Admin User',
            dob=None,
            ca_dl_hash=None,
            ca_dl_last4=None
        )
        db.session.add(admin)

        # 2. Create Reviewer user
        print("  Creating Reviewer user...")
        reviewer = User(
            role=UserRole.REVIEWER,
            email='reviewer@goturbopass.com',
            email_verified_at=datetime.utcnow(),
            password_hash=AuthService.hash_password('reviewer123'),
            full_name='Reviewer User',
            dob=None,
            ca_dl_hash=None,
            ca_dl_last4=None
        )
        db.session.add(reviewer)

        # 3. Create sample modules with quizzes
        print("  Creating sample modules...")

        # Module 1: Introduction to Traffic Safety
        module1 = Module(
            index=1,
            title='Introduction to Traffic Safety',
            min_seconds=600,  # 10 minutes
            content_html='''
                <h1>Module 1: Introduction to Traffic Safety</h1>
                <h2>Welcome to GoTurboPass Traffic School</h2>
                <p>This course is designed to help you become a safer driver and understand California traffic laws.</p>
                <h3>Course Objectives</h3>
                <ul>
                    <li>Understand basic traffic laws and regulations</li>
                    <li>Learn defensive driving techniques</li>
                    <li>Recognize and avoid common driving hazards</li>
                    <li>Reduce your risk of future traffic violations</li>
                </ul>
                <h3>California Traffic Laws Overview</h3>
                <p>California has specific laws designed to keep roads safe for all users, including drivers, pedestrians, and cyclists.</p>
                <p>In this module, we will cover the fundamental concepts of traffic safety and introduce you to the structure of this course.</p>
            ''',
            active=True
        )
        db.session.add(module1)
        db.session.flush()  # Get module1.id

        # Quiz 1
        quiz1 = Quiz(module_id=module1.id, pass_percent=70)
        db.session.add(quiz1)
        db.session.flush()

        # Questions for Quiz 1
        questions1 = [
            Question(
                quiz_id=quiz1.id,
                stem='What is the primary purpose of traffic laws?',
                options={
                    'A': 'To generate revenue for the state',
                    'B': 'To ensure safety for all road users',
                    'C': 'To make driving more difficult',
                    'D': 'To limit vehicle speeds'
                },
                answer_key='B'
            ),
            Question(
                quiz_id=quiz1.id,
                stem='Who is responsible for following traffic laws?',
                options={
                    'A': 'Only professional drivers',
                    'B': 'Only new drivers',
                    'C': 'All drivers on the road',
                    'D': 'Only drivers with violations'
                },
                answer_key='C'
            ),
            Question(
                quiz_id=quiz1.id,
                stem='What should you do if you are unsure about a traffic law?',
                options={
                    'A': 'Ignore it and drive as you think is best',
                    'B': 'Follow what other drivers are doing',
                    'C': 'Consult the California Driver Handbook or a legal resource',
                    'D': 'Ask a passenger'
                },
                answer_key='C'
            ),
            Question(
                quiz_id=quiz1.id,
                stem='Defensive driving means:',
                options={
                    'A': 'Driving aggressively to avoid other vehicles',
                    'B': 'Anticipating potential hazards and driving to minimize risk',
                    'C': 'Always driving at the minimum speed limit',
                    'D': 'Honking at other drivers frequently'
                },
                answer_key='B'
            ),
        ]
        for q in questions1:
            db.session.add(q)

        module1.quiz_id = quiz1.id

        # Module 2: Speed Limits and Right-of-Way
        module2 = Module(
            index=2,
            title='Speed Limits and Right-of-Way',
            min_seconds=600,  # 10 minutes
            content_html='''
                <h1>Module 2: Speed Limits and Right-of-Way</h1>
                <h2>Understanding Speed Limits</h2>
                <p>Speed limits are established to maintain safe traffic flow and reduce accidents.</p>
                <h3>California Speed Limits</h3>
                <ul>
                    <li><strong>Residential areas:</strong> 25 mph (unless posted otherwise)</li>
                    <li><strong>School zones:</strong> 15-25 mph (when children are present)</li>
                    <li><strong>Business districts:</strong> 25 mph</li>
                    <li><strong>Highway/Freeway:</strong> 65 mph (or as posted)</li>
                </ul>
                <h2>Right-of-Way Rules</h2>
                <p>Right-of-way rules prevent confusion and collisions at intersections and crossings.</p>
                <h3>Key Right-of-Way Principles</h3>
                <ul>
                    <li>Yield to vehicles already in an intersection</li>
                    <li>Yield to pedestrians in crosswalks</li>
                    <li>At a 4-way stop, the first vehicle to arrive has the right-of-way</li>
                    <li>Emergency vehicles with lights/sirens always have right-of-way</li>
                </ul>
            ''',
            active=True
        )
        db.session.add(module2)
        db.session.flush()

        # Quiz 2
        quiz2 = Quiz(module_id=module2.id, pass_percent=70)
        db.session.add(quiz2)
        db.session.flush()

        # Questions for Quiz 2
        questions2 = [
            Question(
                quiz_id=quiz2.id,
                stem='What is the default speed limit in a residential area in California?',
                options={
                    'A': '15 mph',
                    'B': '25 mph',
                    'C': '35 mph',
                    'D': '45 mph'
                },
                answer_key='B'
            ),
            Question(
                quiz_id=quiz2.id,
                stem='When must you yield the right-of-way?',
                options={
                    'A': 'Only at stop signs',
                    'B': 'To pedestrians in crosswalks and vehicles already in intersections',
                    'C': 'Never, if you have a green light',
                    'D': 'Only to emergency vehicles'
                },
                answer_key='B'
            ),
            Question(
                quiz_id=quiz2.id,
                stem='At a 4-way stop, who has the right-of-way?',
                options={
                    'A': 'The largest vehicle',
                    'B': 'The vehicle on the right',
                    'C': 'The first vehicle to arrive',
                    'D': 'The fastest vehicle'
                },
                answer_key='C'
            ),
            Question(
                quiz_id=quiz2.id,
                stem='What should you do when an emergency vehicle with lights and sirens approaches?',
                options={
                    'A': 'Speed up to get out of the way',
                    'B': 'Pull over to the right and stop',
                    'C': 'Continue driving normally',
                    'D': 'Turn left at the next intersection'
                },
                answer_key='B'
            ),
        ]
        for q in questions2:
            db.session.add(q)

        module2.quiz_id = quiz2.id

        # Commit all
        db.session.commit()

        print("✅ Seed complete!")
        print("\n🔑 Demo Credentials:")
        print("  Admin:    admin@goturbopass.com / admin123")
        print("  Reviewer: reviewer@goturbopass.com / reviewer123")
        print("\n📚 Sample Modules:")
        print("  Module 1: Introduction to Traffic Safety (4 quiz questions)")
        print("  Module 2: Speed Limits and Right-of-Way (4 quiz questions)")


if __name__ == '__main__':
    seed_database()
