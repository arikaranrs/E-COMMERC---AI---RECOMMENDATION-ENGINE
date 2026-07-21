"""
Seed script to populate SQLite database with test data.
Includes products, categories, brands, users, reviews, ratings, and recommendation cache.
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.product import Category, Brand, Product, Rating, Review, UserActivity
from app.models.order import Order, OrderItem, Cart, CartItem, Wishlist, RecommendationCache
from app.services.auth_service import hash_password

def seed_data():
    print("Initializing database...")
    # Recreate tables to start clean
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("Seeding Categories & Brands...")
        # 1. Seed Categories
        categories = {
            "Electronics": Category(name="Electronics", description="Gadgets, devices, and accessories.", icon_url="https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=100&auto=format&fit=crop&q=60"),
            "Books": Category(name="Books", description="Novels, textbooks, and guidebooks.", icon_url="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=100&auto=format&fit=crop&q=60"),
            "Fashion": Category(name="Fashion", description="Apparel, shoes, and clothing accessories.", icon_url="https://images.unsplash.com/photo-1483985988355-763728e1935b?w=100&auto=format&fit=crop&q=60"),
            "Home & Kitchen": Category(name="Home & Kitchen", description="Kitchenware, appliances, and decor.", icon_url="https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=100&auto=format&fit=crop&q=60"),
        }
        for cat in categories.values():
            db.add(cat)

        # 2. Seed Brands
        brands = {
            "TechCorp": Brand(name="TechCorp", description="High-end consumer electronics."),
            "ReadPress": Brand(name="ReadPress", description="Publishers of educational and fictional literature."),
            "StyleCo": Brand(name="StyleCo", description="Modern everyday fashion and accessories."),
            "HomeEase": Brand(name="HomeEase", description="Convenient and quality home items."),
        }
        for brand in brands.values():
            db.add(brand)

        db.commit()

        # Refresh to get IDs
        for cat in categories.values():
            db.refresh(cat)
        for brand in brands.values():
            db.refresh(brand)

        print("Seeding Products...")
        # 3. Seed Products
        products_data = [
            # Electronics
            {
                "name": "TechCorp QuietMax Wireless Headphones",
                "description": "Premium active noise-cancelling headphones with 40-hour battery life, high-fidelity sound, and memory foam earcups.",
                "price": 199.99,
                "category": "Electronics",
                "brand": "TechCorp",
                "stock": 120,
                "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60",
                "sku": "ELEC-HD-001"
            },
            {
                "name": "TechCorp OLED Ultra HD 55-inch Smart TV",
                "description": "Stunning 4K OLED display with Dolby Vision, HDR10+, variable refresh rate for gaming, and smart assistant integration.",
                "price": 899.99,
                "category": "Electronics",
                "brand": "TechCorp",
                "stock": 15,
                "image": "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=500&auto=format&fit=crop&q=60",
                "sku": "ELEC-TV-002"
            },
            {
                "name": "TechCorp Mechanical Wireless Keyboard",
                "description": "Tactile blue switches, custom RGB lighting, multi-device bluetooth pairing, and robust aluminum top frame.",
                "price": 99.99,
                "category": "Electronics",
                "brand": "TechCorp",
                "stock": 85,
                "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60",
                "sku": "ELEC-KB-003"
            },
            {
                "name": "TechCorp ActiveFit Smart Watch",
                "description": "Fitness tracking smartwatch with heart rate monitoring, GPS tracking, sleep coaching, and 7-day battery life.",
                "price": 149.99,
                "category": "Electronics",
                "brand": "TechCorp",
                "stock": 140,
                "image": "https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=500&auto=format&fit=crop&q=60",
                "sku": "ELEC-SW-004"
            },
            
            # Books
            {
                "name": "Python Programming Masterclass",
                "description": "The comprehensive guide to software development in Python. Covers data structures, OOP, web frameworks, and ML basics.",
                "price": 39.99,
                "category": "Books",
                "brand": "ReadPress",
                "stock": 250,
                "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500&auto=format&fit=crop&q=60",
                "sku": "BOOK-PY-001"
            },
            {
                "name": "Designing Microservices Architecture",
                "description": "Deep dive into building scalable, fault-tolerant distributed systems. Learn service discovery, event sourcing, and API gateways.",
                "price": 49.99,
                "category": "Books",
                "brand": "ReadPress",
                "stock": 90,
                "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500&auto=format&fit=crop&q=60",
                "sku": "BOOK-MS-002"
            },
            {
                "name": "Shadows of the Cosmos: Space Opera",
                "description": "An epic sci-fi space adventure detailing the survival of a rogue crew navigating intergalactic conflicts and ancient alien technologies.",
                "price": 14.99,
                "category": "Books",
                "brand": "ReadPress",
                "stock": 310,
                "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=500&auto=format&fit=crop&q=60",
                "sku": "BOOK-SF-003"
            },
            {
                "name": "The Art of Clean Code",
                "description": "Essential principles of code craftmanship. Learn how to write readable, reusable, and highly maintainable software.",
                "price": 29.99,
                "category": "Books",
                "brand": "ReadPress",
                "stock": 180,
                "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=60",
                "sku": "BOOK-CC-004"
            },

            # Fashion
            {
                "name": "StyleCo Classic Leather Jacket",
                "description": "100% genuine full-grain leather jacket. Vintage tailored fit, sturdy metallic zippers, and interior quilted lining.",
                "price": 129.99,
                "category": "Fashion",
                "brand": "StyleCo",
                "stock": 45,
                "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&auto=format&fit=crop&q=60",
                "sku": "FASH-LJ-001"
            },
            {
                "name": "StyleCo Slim Fit Denim Jeans",
                "description": "Stretchable classic blue denim jeans featuring a modern tapered cut, reinforced seams, and five-pocket styling.",
                "price": 49.99,
                "category": "Fashion",
                "brand": "StyleCo",
                "stock": 200,
                "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500&auto=format&fit=crop&q=60",
                "sku": "FASH-DJ-002"
            },
            {
                "name": "StyleCo Canvas Daily Sneakers",
                "description": "Breathable cotton canvas sneakers with durable vulcanized rubber soles. Light, stylish, and comfortable for daily wear.",
                "price": 29.99,
                "category": "Fashion",
                "brand": "StyleCo",
                "stock": 150,
                "image": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=500&auto=format&fit=crop&q=60",
                "sku": "FASH-SN-003"
            },
            {
                "name": "StyleCo Polarized Aviator Sunglasses",
                "description": "Timeless aviator styling with lightweight metal frames and high-performance polarized lenses. 100% UVA/UVB protection.",
                "price": 24.99,
                "category": "Fashion",
                "brand": "StyleCo",
                "stock": 300,
                "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&auto=format&fit=crop&q=60",
                "sku": "FASH-SG-004"
            },

            # Home & Kitchen
            {
                "name": "HomeEase Precision Espresso Machine",
                "description": "Professional 15-bar Italian pump espresso maker. Equipped with milk frothing wand and precise digital temperature controls.",
                "price": 249.99,
                "category": "Home & Kitchen",
                "brand": "HomeEase",
                "stock": 30,
                "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500&auto=format&fit=crop&q=60",
                "sku": "HOME-EM-001"
            },
            {
                "name": "HomeEase Digital XL Air Fryer",
                "description": "6-quart capacity air fryer utilizing rapid hot air circulation. 8 preset digital modes for quick, oil-free meals.",
                "price": 89.99,
                "category": "Home & Kitchen",
                "brand": "HomeEase",
                "stock": 95,
                "image": "https://images.unsplash.com/photo-1621972750749-0fbb1abb7736?w=500&auto=format&fit=crop&q=60",
                "sku": "HOME-AF-002"
            },
            {
                "name": "HomeEase Robot Vacuum & Mop",
                "description": "Smart lidar-navigating robotic vacuum. Features 3000Pa suction power, custom zone mapping app, and integrated wet mop system.",
                "price": 199.99,
                "category": "Home & Kitchen",
                "brand": "HomeEase",
                "stock": 40,
                "image": "https://images.unsplash.com/photo-1518310383802-640c2de311b2?w=500&auto=format&fit=crop&q=60",
                "sku": "HOME-RV-003"
            },
            {
                "name": "HomeEase Ceramic Non-Stick Skillet",
                "description": "Eco-friendly 10-inch skillet with double-layer ceramic non-stick coating. Induction compatible base and cool-touch handle.",
                "price": 34.99,
                "category": "Home & Kitchen",
                "brand": "HomeEase",
                "stock": 110,
                "image": "https://images.unsplash.com/photo-1599940824399-b87987ceb72a?w=500&auto=format&fit=crop&q=60",
                "sku": "HOME-NS-004"
            }
        ]

        products = []
        for p_data in products_data:
            p = Product(
                name=p_data["name"],
                description=p_data["description"],
                price=p_data["price"],
                category_id=categories[p_data["category"]].id,
                brand_id=brands[p_data["brand"]].id,
                stock_quantity=p_data["stock"],
                image_url=p_data["image"],
                sku=p_data["sku"],
                rating=0.0,
                review_count=0
            )
            db.add(p)
            products.append(p)

        db.commit()

        # Refresh products to get IDs
        for p in products:
            db.refresh(p)

        print("Seeding Users...")
        # 4. Seed Mock Users
        users_data = [
            {
                "email": "sarah.bookworm@example.com",
                "first_name": "Sarah",
                "last_name": "Readings",
                "bio": "Avid reader, tech-hobbyist, and professional software engineer.",
                "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=60"
            },
            {
                "email": "david.techie@example.com",
                "first_name": "David",
                "last_name": "Gates",
                "bio": "Gadget reviewer and smart home enthusiast. I love everything with a microchip.",
                "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=60"
            },
            {
                "email": "emily.stylist@example.com",
                "first_name": "Emily",
                "last_name": "Vogue",
                "bio": "Fashion designer, vintage collector, and home lifestyle blogger.",
                "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&auto=format&fit=crop&q=60"
            },
            {
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "bio": "System administrator.",
                "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=60",
                "is_admin": True
            }
        ]

        users = {}
        for u_data in users_data:
            u = User(
                email=u_data["email"],
                password_hash=hash_password("Password123!"),
                first_name=u_data["first_name"],
                last_name=u_data["last_name"],
                bio=u_data["bio"],
                avatar_url=u_data["avatar"],
                is_admin=u_data.get("is_admin", False),
                is_active=True
            )
            db.add(u)
            users[u_data["email"]] = u

        db.commit()

        # Refresh users to get IDs
        for u in users.values():
            db.refresh(u)

        print("Seeding Ratings & Reviews...")
        # 5. Seed Ratings and Reviews to construct user profile vectors
        # Sarah loves Books, dislikes some fashion item, bought home items
        reviews_data = [
            # Sarah
            ("sarah.bookworm@example.com", "Python Programming Masterclass", 5, "Life saver!", "This book taught me everything I needed to know about Django and Python syntax. Very clean explanations!"),
            ("sarah.bookworm@example.com", "The Art of Clean Code", 5, "Brilliant", "Highly recommended for junior developers. Excellent tips on layout, testing, and naming variables."),
            ("sarah.bookworm@example.com", "Designing Microservices Architecture", 4, "Very Comprehensive", "Good details, though could have more diagrams on kubernetes orchestration patterns."),
            ("sarah.bookworm@example.com", "StyleCo Polarized Aviator Sunglasses", 2, "Too fragile", "Look nice but the hinges feel extremely loose and fragile. Disappointed."),
            ("sarah.bookworm@example.com", "HomeEase Precision Espresso Machine", 4, "Good brew", "Makes a delicious espresso shot daily. Heating up takes about 2 minutes, which is acceptable."),
            
            # David
            ("david.techie@example.com", "TechCorp QuietMax Wireless Headphones", 5, "Perfect Sound", "Phenomenal active noise-cancelling. I use them at the office daily and it completely silences chatter."),
            ("david.techie@example.com", "TechCorp OLED Ultra HD 55-inch Smart TV", 5, "Mind-blowing OLED colors", "The blacks are perfect. High refresh rate makes gaming on next-gen consoles buttery smooth!"),
            ("david.techie@example.com", "TechCorp Mechanical Wireless Keyboard", 4, "Clicky and durable", "Excellent tactile typing experience. The bluetooth syncs across my Mac and PC instantly."),
            ("david.techie@example.com", "TechCorp ActiveFit Smart Watch", 5, "Accurate stats", "Tracks my heart rate and gym logs flawlessly. Battery easily lasts 6-7 days."),
            ("david.techie@example.com", "HomeEase Robot Vacuum & Mop", 4, "Saves so much time", "Navigates my living room easily. Mop function is okay for minor dust, but vacuum power is great."),
            ("david.techie@example.com", "Python Programming Masterclass", 4, "Learnt scripting", "Good tutorial for a tech enthusiast trying to learn data analytics scripting."),

            # Emily
            ("emily.stylist@example.com", "StyleCo Classic Leather Jacket", 5, "Stunning Leather Quality", "Genuine leather, premium heavy zippers. Tailored cut is perfect! Must buy."),
            ("emily.stylist@example.com", "StyleCo Slim Fit Denim Jeans", 5, "Super comfy", "Perfect stretch jeans that fit like a glove. Will buy in black color too."),
            ("emily.stylist@example.com", "StyleCo Canvas Daily Sneakers", 4, "Simple and neat", "Basic daily sneakers. Soft sole and doesn't get dirty easily."),
            ("emily.stylist@example.com", "StyleCo Polarized Aviator Sunglasses", 5, "Sleek and classy", "Elegant gold metal frame and works great under heavy sunlight."),
            ("emily.stylist@example.com", "HomeEase Digital XL Air Fryer", 5, "Cooks everything perfectly", "French fries, chicken wings, veggies, all crisp without oil. Clean up is very easy!"),
            ("emily.stylist@example.com", "HomeEase Precision Espresso Machine", 2, "Too complicated", "A bit tedious to clean and dial in the ground size. I prefer simple drip coffee.")
        ]

        # Helper to find product by name
        def find_product_by_name(name):
            for prod in products:
                if prod.name == name:
                    return prod
            return None

        for user_email, prod_name, score, title, review_text in reviews_data:
            user = users[user_email]
            product = find_product_by_name(prod_name)
            if user and product:
                # Add rating
                rating = Rating(user_id=user.id, product_id=product.id, rating=score)
                db.add(rating)
                
                # Add review
                review = Review(
                    user_id=user.id,
                    product_id=product.id,
                    title=title,
                    content=review_text,
                    helpful_count=random.randint(1, 10),
                    unhelpful_count=0
                )
                db.add(review)

        db.commit()

        # Update product average ratings and review counts
        for p in products:
            ratings = db.query(Rating).filter(Rating.product_id == p.id).all()
            if ratings:
                p.rating = round(sum(r.rating for r in ratings) / len(ratings), 1)
                p.review_count = len(ratings)
            db.add(p)
        db.commit()

        print("Seeding Recommendation Cache...")
        # 6. Seed precomputed recommendations for different profiles
        # Precomputed product ID arrays
        elec_ids = [p.id for p in products if p.category_id == categories["Electronics"].id]
        book_ids = [p.id for p in products if p.category_id == categories["Books"].id]
        fashion_ids = [p.id for p in products if p.category_id == categories["Fashion"].id]
        home_ids = [p.id for p in products if p.category_id == categories["Home & Kitchen"].id]
        
        # Mix profiles
        sarah = users["sarah.bookworm@example.com"]
        sarah_recs = {
            "personalized": [find_product_by_name("Designing Microservices Architecture").id, find_product_by_name("Python Programming Masterclass").id, find_product_by_name("The Art of Clean Code").id],
            "collaborative": [find_product_by_name("Designing Microservices Architecture").id, find_product_by_name("TechCorp Mechanical Wireless Keyboard").id, find_product_by_name("HomeEase Robot Vacuum & Mop").id],
            "content_based": [find_product_by_name("Python Programming Masterclass").id, find_product_by_name("The Art of Clean Code").id, find_product_by_name("Designing Microservices Architecture").id],
            "hybrid": [find_product_by_name("Designing Microservices Architecture").id, find_product_by_name("The Art of Clean Code").id, find_product_by_name("HomeEase Precision Espresso Machine").id, find_product_by_name("TechCorp Mechanical Wireless Keyboard").id],
            "trending": [find_product_by_name("TechCorp QuietMax Wireless Headphones").id, find_product_by_name("HomeEase Digital XL Air Fryer").id, find_product_by_name("StyleCo Classic Leather Jacket").id]
        }

        david = users["david.techie@example.com"]
        david_recs = {
            "personalized": [find_product_by_name("TechCorp OLED Ultra HD 55-inch Smart TV").id, find_product_by_name("TechCorp Mechanical Wireless Keyboard").id, find_product_by_name("TechCorp QuietMax Wireless Headphones").id],
            "collaborative": [find_product_by_name("TechCorp ActiveFit Smart Watch").id, find_product_by_name("HomeEase Robot Vacuum & Mop").id, find_product_by_name("Python Programming Masterclass").id],
            "content_based": [find_product_by_name("TechCorp ActiveFit Smart Watch").id, find_product_by_name("TechCorp OLED Ultra HD 55-inch Smart TV").id, find_product_by_name("TechCorp QuietMax Wireless Headphones").id],
            "hybrid": [find_product_by_name("TechCorp QuietMax Wireless Headphones").id, find_product_by_name("TechCorp OLED Ultra HD 55-inch Smart TV").id, find_product_by_name("HomeEase Precision Espresso Machine").id],
            "trending": [find_product_by_name("TechCorp OLED Ultra HD 55-inch Smart TV").id, find_product_by_name("HomeEase Digital XL Air Fryer").id, find_product_by_name("StyleCo Classic Leather Jacket").id]
        }

        emily = users["emily.stylist@example.com"]
        emily_recs = {
            "personalized": [find_product_by_name("StyleCo Classic Leather Jacket").id, find_product_by_name("StyleCo Slim Fit Denim Jeans").id, find_product_by_name("StyleCo Polarized Aviator Sunglasses").id],
            "collaborative": [find_product_by_name("StyleCo Canvas Daily Sneakers").id, find_product_by_name("HomeEase Digital XL Air Fryer").id, find_product_by_name("HomeEase Precision Espresso Machine").id],
            "content_based": [find_product_by_name("StyleCo Classic Leather Jacket").id, find_product_by_name("StyleCo Slim Fit Denim Jeans").id, find_product_by_name("StyleCo Polarized Aviator Sunglasses").id],
            "hybrid": [find_product_by_name("StyleCo Classic Leather Jacket").id, find_product_by_name("StyleCo Polarized Aviator Sunglasses").id, find_product_by_name("HomeEase Digital XL Air Fryer").id],
            "trending": [find_product_by_name("StyleCo Classic Leather Jacket").id, find_product_by_name("HomeEase Digital XL Air Fryer").id, find_product_by_name("TechCorp QuietMax Wireless Headphones").id]
        }

        admin = users["admin@example.com"]
        default_recs = {
            "personalized": [p.id for p in products[:4]],
            "collaborative": [p.id for p in products[4:8]],
            "content_based": [p.id for p in products[8:12]],
            "hybrid": [p.id for p in products[12:16]],
            "trending": [p.id for p in products[:6]]
        }

        all_cached = [
            (sarah, sarah_recs),
            (david, david_recs),
            (emily, emily_recs),
            (admin, default_recs)
        ]

        for user_obj, rec_map in all_cached:
            for rec_type, pids in rec_map.items():
                clean_pids = [int(pid) for pid in pids if pid is not None]
                cache_entry = RecommendationCache(
                    user_id=user_obj.id,
                    product_ids=clean_pids,
                    recommendation_type=rec_type,
                    expires_at=datetime.utcnow() + timedelta(days=7)
                )
                db.add(cache_entry)

        db.commit()
        print("Database seeded successfully with all tables populated!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
