from flask import Flask, render_template, request, redirect, session, g,flash
import sqlite3
import math
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret123"

DATABASE = "database.db"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------------------------
# SIMPLE MULTI-LANGUAGE DICTIONARY
# ---------------------------------
translations = {
    "en": {
        "site_title": "Farm2Table | Welcome",
        "logo": "Farm2Table 🌾",

        "english": "English",
        "kannada": "Kannada",

        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "back": "Back",
        "back_to_dashboard": "Back to Dashboard",
        "back_to_farmer_dashboard": "Back to Farmer Dashboard",
        "back_to_buyer_dashboard": "Back to Buyer Dashboard",
        "open": "Open",
        "send": "Send",
        "create": "Create",
        "view_details": "View Details",
        "order_now": "Order Now",

        "phone_number": "Phone Number",
        "enter_phone_number": "Enter your phone number",
        "password": "Password",
        "enter_password": "Enter your password",
        "full_name": "Full Name",
        "enter_full_name": "Enter your full name",
        "enter_name": "Enter your name",
        "create_password": "Create a password",
        "description": "Description",
        "community_name": "Community Name",
        "crop_name": "Crop Name",
        "price_per_kg": "Price per Kg",
        "quantity_kg": "Quantity (Kg)",
        "available_quantity": "Available Quantity",
        "average_price": "Average Price",
        "price": "Price",
        "community": "Community",
        "farmer": "Farmer",
        "buyer": "Buyer",
        "name": "Name",
        "phone": "Phone",
        "quantity": "Quantity",
        "total_price": "Total Price",
        "order_date": "Order Date",
        "buyer_details": "Buyer Details",

        # Index
        "farmer_login": "Farmer Login",
        "buyer_login": "Buyer Login",
        "hyperlocal_tag": "Hyperlocal Agri Marketplace",
        "welcome_title": "Fresh Produce From Nearby Farmers Directly To Buyers",
        "welcome_subtitle": "Farm2Table helps farmers build local communities, add crop inventory and connect directly with nearby buyers without middlemen.",
        "enter_farmer": "Enter Farmer Portal",
        "enter_buyer": "Enter Buyer Portal",
        "platform_features": "Platform Features",
        "platform_subtitle": "Everything needed to connect farmers and buyers locally.",
        "farmer_dashboard": "Farmer Dashboard",
        "farmer_dashboard_desc": "Farmers can add crops, manage inventory and receive orders.",
        "buyer_dashboard": "Buyer Dashboard",
        "buyer_dashboard_desc": "Buyers can discover nearby farmers and place direct orders.",
        "nearby_communities": "Nearby Communities",
        "nearby_communities_desc": "GPS based community discovery within 10KM.",
        "live_crop_inventory": "Live Crop Inventory",
        "live_crop_inventory_desc": "See real crop stock added by farmers.",
        "community_selling": "Community Selling",
        "community_selling_desc": "Multiple farmers collaborate to fulfill buyer demand.",
        "farmer_communication": "Farmer Communication",
        "farmer_communication_desc": "Community chat for collaboration between farmers.",
        "cta_title": "A Smarter Way To Connect Farms And Families",
        "cta_desc": "Helping farmers sell better and buyers find fresh local produce easily.",
        "footer_text": "Connecting local farmers and buyers directly.",

        # Farmer Login
        "farmer_access": "Farmer Access",
        "welcome_back_farmer": "Welcome Back To Your Farm Dashboard",
        "farmer_login_desc_long": "Log in to manage your products, check incoming orders, stay connected with your farming community, and continue selling directly to nearby buyers.",
        "manage_crops_easily": "Manage Crops Easily",
        "manage_crops_easily_desc": "Update crop listings, pricing, quantity, and availability anytime.",
        "track_buyer_orders": "Track Buyer Orders",
        "track_buyer_orders_desc": "View all orders placed for your products in one simple dashboard.",
        "community_support": "Community Support",
        "community_support_desc": "Stay connected with nearby farmers through your local community system.",
        "better_local_selling": "Better Local Selling",
        "better_local_selling_desc": "Reach nearby buyers directly without depending on middlemen.",
        "enter_login_details_farmer": "Enter your login details to access your farmer portal.",
        "login_to_dashboard": "Login To Dashboard",
        "new_farmer": "New farmer?",
        "create_account": "Create an account",

        # Buyer Login
        "buyer_access": "Buyer Access",
        "buyer_login_title": "Buy Fresh Produce Directly From Nearby Farmers",
        "buyer_login_desc_long": "Log in to explore nearby farming communities, view real crop inventory, and place direct orders from local farmers without any middlemen.",
        "nearby_community_access": "Nearby Community Access",
        "nearby_community_access_desc": "Find communities close to your location using GPS-based matching.",
        "fresh_product_discovery": "Fresh Product Discovery",
        "fresh_product_discovery_desc": "View vegetables, fruits, grains, and other products directly added by farmers.",
        "direct_farmer_orders": "Direct Farmer Orders",
        "direct_farmer_orders_desc": "Place orders without middlemen and connect directly with local growers.",
        "trusted_local_produce": "Trusted Local Produce",
        "trusted_local_produce_desc": "Buy vegetables, fruits, and crops directly from local farms.",
        "enter_login_details_buyer": "Enter your details to access the buyer dashboard.",
        "new_buyer": "New buyer?",

        # Farmer Register
        "farmer_onboarding": "Farmer Onboarding",
        "start_selling_title": "Start Selling Fresh Crops Directly To Local Buyers",
        "start_selling_desc": "Create your farmer account to join Farm2Table. Build your local presence, connect with nearby communities, add your products, and receive direct orders from buyers without middlemen.",
        "community_based_selling": "Community-Based Selling",
        "community_based_selling_desc": "Join or create a local farmer community and supply buyers together.",
        "direct_orders": "Direct Orders",
        "direct_orders_desc": "Receive buyer orders directly for the products you actually add.",
        "local_reach": "Local Reach",
        "local_reach_desc": "Show your crops to buyers nearby for faster selling and better trust.",
        "simple_management": "Simple Management",
        "simple_management_desc": "Manage products, orders, and communication in one place.",
        "farmer_registration": "Farmer Registration",
        "farmer_registration_desc": "Create your account and begin listing your farm produce for nearby buyers.",
        "create_farmer_account": "Create Farmer Account",
        "already_registered": "Already registered?",

        # Buyer Register
        "buyer_onboarding": "Buyer Onboarding",
        "buyer_register_title": "Join To Discover Fresh Local Products Near You",
        "buyer_register_desc": "Create your buyer account to explore nearby farmer communities, view real product listings, and place direct orders from local farmers within your area.",
        "direct_ordering": "Direct Ordering",
        "direct_ordering_desc": "Place orders without middlemen and connect directly with local growers.",
        "better_accuracy": "Better Accuracy",
        "better_accuracy_desc": "Location-based visibility helps buyers discover only relevant nearby sellers.",
        "buyer_registration": "Buyer Registration",
        "buyer_registration_desc": "Create your account and start exploring nearby farmers and fresh local produce.",
        "create_buyer_account": "Create Buyer Account",
        "location_note": "Your location will be used to show farmer communities within 10KM. Please allow location access for better recommendations.",

        # Farmer Dashboard
        "smart_farming_panel": "Smart Farming Panel",
        "farmer_dashboard_desc_long": "Manage your community, products, buyer orders, and farmer communication from one modern workspace built for local agriculture.",
        "farmer_tools": "Farmer Tools",
        "buyer_discovery_radius": "Buyer Discovery Radius",
        "live_inventory": "Live Product Inventory",
        "create_community": "Create Community",
        "create_local_farmer_community": "Create a local farmer community and collaborate with nearby growers in your area.",
        "add_crop": "Add Crop",
        "add_new_farm_products": "Add new farm products with pricing, quantity, and stock details for nearby buyers.",
        "community_inventory": "Community Inventory",
        "view_all_available_products": "View all available products contributed by farmers inside your community.",
        "community_chat": "Community Chat",
        "communicate_fellow_farmers": "Communicate with fellow farmers, coordinate supply, and stay connected.",
        "buyer_orders": "Buyer Orders",
        "track_orders_manage": "Track orders placed by buyers, review quantity requested, and manage fulfillment.",

        # Create Community
        "community_setup": "Community Setup",
        "create_farmer_community_title": "Create A Farmer Community In Your Local Area",
        "create_farmer_community_desc": "Start a local farming community so nearby farmers can collaborate, manage inventory together, and improve availability for buyers in your region.",
        "gps_based_community": "GPS-Based Community",
        "gps_based_community_desc": "Your current location is captured automatically to place your community accurately.",
        "farmer_collaboration": "Farmer Collaboration",
        "farmer_collaboration_desc": "Communities allow multiple farmers to work together and serve more buyers.",
        "nearby_buyer_reach": "Nearby Buyer Reach",
        "nearby_buyer_reach_desc": "Buyers can discover your community based on local distance matching.",
        "smarter_selling": "Smarter Selling",
        "smarter_selling_desc": "A stronger community improves stock visibility, trust, and local fulfillment.",
        "create_community_desc_form": "Set your community name and let the platform capture your location automatically.",
        "enter_community_name": "Enter community name",
        "location_capture_note": "Your current latitude and longitude will be captured automatically. Please allow location access when prompted.",

        # Add Crop
        "crop_inventory": "Crop Inventory",
        "add_fresh_crops_title": "Add Fresh Crops To Your Farm Inventory",
        "add_fresh_crops_desc": "Add your products with price, quantity, and details so nearby buyers can discover exactly what you have available in your community.",
        "real_time_stock": "Real-Time Stock",
        "real_time_stock_desc": "Only added products are shown to buyers, making listings accurate and useful.",
        "better_visibility": "Better Visibility",
        "better_visibility_desc": "Your crops become visible to nearby buyers and communities in your local area.",
        "simple_product_entry": "Simple Product Entry",
        "simple_product_entry_desc": "Add crop name, price, quantity, and description in just a few fields.",
        "direct_local_orders": "Direct Local Orders",
        "direct_local_orders_desc": "Help buyers place direct orders from your available stock without middlemen.",
        "add_crop_desc_form": "Enter your crop details below to make them available to nearby buyers.",
        "enter_crop_name": "Enter crop name",
        "enter_price_per_kg": "Enter price per kg",
        "enter_available_quantity": "Enter available quantity",
        "enter_product_description": "Enter product description",
        "add_crop_inventory_button": "Add Crop To Inventory",

        # Buyer Dashboard
        "buyer_dashboard_desc_long": "Discover nearby farmer communities, explore fresh available products, and place direct orders from local growers near you.",
        "fresh_nearby_products": "Fresh Nearby Products",
        "available_products": "Available Products",
        "nearby_radius": "Nearby Radius",
        "nearby_farmer_communities": "Nearby Farmer Communities",
        "nearby_farmer_communities_desc": "These communities are available near your location, helping you discover trusted local farmers more accurately.",
        "farmers_in_this_community": "Farmers in this community:",
        "no_farmers_yet": "No farmers yet",
        "no_nearby_communities": "No Nearby Communities",
        "no_nearby_communities_desc": "No communities found within your nearby range.",
        "available_products_nearby": "Available Products from Nearby Farmers",
        "available_products_nearby_desc": "Browse products that farmers in your nearby communities have already added to their inventory.",
        "no_products_available": "No Products Available",
        "no_products_available_desc": "No products are currently available from nearby farmer communities.",
        "distance": "Distance",

        # Community Inventory
        "community_inventory_desc_long": "View crops contributed by farmers in your community, monitor stock availability, and understand the overall supply inside your local farming network.",
        "shared_crop_inventory": "Shared Crop Inventory",
        "available_crop_types": "Available Crop Types",
        "inventory_visibility": "Inventory Visibility",
        "farmer_contribution": "Farmer Contribution",
        "no_crops_available_desc": "No crops are currently available in your community inventory.",

        # Community Chat
        "community_chat_desc_long": "Connect with farmers in your community, coordinate stock, discuss availability, and collaborate more effectively.",
        "farmer_discussion_space": "Farmer Discussion Space",
        "community_messages": "Community Messages",
        "community_messages_desc": "Type a message or use the mic to convert speech into text.",
        "type_message": "Type your message...",
        "no_messages_yet": "No messages yet. Start the conversation!",
        "voice_not_supported": "Voice input is not supported in this browser.",
        "listening": "Listening... Speak now",
        "voice_captured": "Voice captured",
        "voice_error": "Voice error",

        # Farmer Orders
        "farmer_orders": "Farmer Orders",
        "farmer_orders_desc_long": "Review orders placed by buyers, track requested quantities, and manage crop fulfillment from your farm inventory.",
        "buyer_orders_overview": "Buyer Orders Overview",
        "total_orders": "Total Orders",
        "buyer_connections": "Buyer Connections",
        "order_tracking": "Order Tracking",
        "local_fulfillment": "Local Fulfillment",
        "no_orders_received": "No orders received yet.",

        # Place order
        "place_order": "Place Order",
        "order_quantity": "Order Quantity",
        "enter_quantity": "Enter quantity",
        "confirm_order": "Confirm Order",

        # Messages from routes
        "msg_farmer_registered": "Farmer Registered Successfully!",
        "msg_buyer_registered": "Buyer Registered Successfully!",
        "msg_invalid_credentials": "Invalid Credentials",
        "msg_allow_location": "Please allow location access.",
        "msg_community_created": "Community Created Successfully!",
        "msg_product_added": "Product Added Successfully!",
        "msg_not_in_community": "You are not part of any community.",
        "msg_buyer_not_found": "Buyer not found.",
        "msg_product_not_found": "Product not found",
        "msg_order_success": "Order placed successfully!",
        "msg_no_community": "You are not in any community.",
        "farm_trust_report": "Farm Trust Report",
        "farm_trust_desc": "See how this crop was grown, what inputs were used, and the AI-generated transparency summary.",
        "farming_details": "Farming Details",
        "farming_method": "Farming Method",
        "pesticide_used": "Pesticide Used",
        "fertilizer_used": "Fertilizer Used",
        "harvest_date": "Harvest Date",
        "storage_method": "Storage Method",
        "ai_health_insight": "AI Health Insight",
        "not_specified": "Not specified",
        "not_assigned": "Not assigned",
        "view_farm_trust_report": "View Farm Trust Report",
        "basic_product_details": "Basic Product Details",
        "farm_trust_details": "Farm Trust Report Details",
        "select_farming_method": "Select farming method",
        "organic_farming": "Organic Farming",
        "natural_farming": "Natural Farming",
        "regular_farming": "Regular Farming",
        "trust_report_hint": "These details will help buyers understand how the crop was grown and improve trust through a Farm Trust Report.",
        "ai_summary_text": "This crop was grown using {method} methods. Reported pesticide usage: {pesticide}.  Based on farmer-provided details, this product appears suitable for regular household use.",

        "low_chemical_use": "Low Chemical Use",
        "natural_protection": "Natural Protection Used",
        "chemical_use_declared": "Farmer Declared Chemical Use",
        "organic_crop": "Organic Crop",
        "fresh_harvest": "Fresh Harvest",
        "freshness_not_declared": "Freshness Not Declared",

        "farmer_ai_insights": "AI Smart Farming Insights",
        "ai_page_desc": "Visual insights to help farmers understand crop demand, profits, and buyer activity.",

        "products_listed": "Products Listed",
        "total_orders": "Total Orders",
        "total_revenue": "Total Revenue",
        "estimated_profit": "Estimated Profit",

        "crop_demand": "Crop Demand",
        "monthly_earnings": "Monthly Earnings",
        "price_trend": "Price Trend",
        "community_activity": "Community Activity",

        "farm_trust_score": "Farm Trust Score",
        "crop_transparency": "Crop Transparency",
        "natural_farming": "Natural Farming",
        "storage_quality": "Storage Quality",
        "freshness": "Freshness",

        "ai_suggestions": "AI Suggestions",
        "demand_tip": "Demand Tip",
        "price_tip": "Price Tip",
        "community_tip": "Community Tip",
        "weather_tip": "Weather Tip",

        "low_stock_alerts": "Low Stock Alerts",

        "profit_summary": "Profit Summary",
        "top_crop": "Top Crop",

        "join_or_create_community": "Join or Create Community",
        "join_or_create_desc": "See nearby farmer communities in your area, join an existing one, or create a new community if needed."
            },

    "kn": {
        "site_title": "Farm2Table | ಸ್ವಾಗತ",
        "logo": "Farm2Table 🌾",

        "english": "English",
        "kannada": "ಕನ್ನಡ",

        "login": "ಲಾಗಿನ್",
        "register": "ನೋಂದಣಿ",
        "logout": "ಲಾಗ್ಔಟ್",
        "back": "ಹಿಂದೆ",
        "back_to_dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹಿಂದಿರುಗಿ",
        "back_to_farmer_dashboard": "ರೈತ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹಿಂದಿರುಗಿ",
        "back_to_buyer_dashboard": "ಖರೀದಿದಾರ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹಿಂದಿರುಗಿ",
        "open": "ತೆರೆಯಿರಿ",
        "send": "ಕಳುಹಿಸಿ",
        "create": "ರಚಿಸಿ",
        "view_details": "ವಿವರಗಳನ್ನು ನೋಡಿ",
        "order_now": "ಈಗಲೇ ಆರ್ಡರ್ ಮಾಡಿ",

        "phone_number": "ದೂರವಾಣಿ ಸಂಖ್ಯೆ",
        "enter_phone_number": "ನಿಮ್ಮ ದೂರವಾಣಿ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ",
        "password": "ಪಾಸ್ವರ್ಡ್",
        "enter_password": "ನಿಮ್ಮ ಪಾಸ್ವರ್ಡ್ ನಮೂದಿಸಿ",
        "full_name": "ಪೂರ್ಣ ಹೆಸರು",
        "enter_full_name": "ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ನಮೂದಿಸಿ",
        "enter_name": "ನಿಮ್ಮ ಹೆಸರನ್ನು ನಮೂದಿಸಿ",
        "create_password": "ಪಾಸ್ವರ್ಡ್ ರಚಿಸಿ",
        "description": "ವಿವರಣೆ",
        "community_name": "ಸಮುದಾಯದ ಹೆಸರು",
        "crop_name": "ಬೆಳೆ ಹೆಸರು",
        "price_per_kg": "ಪ್ರತಿ ಕೆ.ಜಿ.ಗೆ ಬೆಲೆ",
        "quantity_kg": "ಪ್ರಮಾಣ (ಕೆ.ಜಿ.)",
        "available_quantity": "ಲಭ್ಯ ಪ್ರಮಾಣ",
        "average_price": "ಸರಾಸರಿ ಬೆಲೆ",
        "price": "ಬೆಲೆ",
        "community": "ಸಮುದಾಯ",
        "farmer": "ರೈತ",
        "buyer": "ಖರೀದಿದಾರ",
        "name": "ಹೆಸರು",
        "phone": "ದೂರವಾಣಿ",
        "quantity": "ಪ್ರಮಾಣ",
        "total_price": "ಒಟ್ಟು ಬೆಲೆ",
        "order_date": "ಆರ್ಡರ್ ದಿನಾಂಕ",
        "buyer_details": "ಖರೀದಿದಾರರ ವಿವರಗಳು",

        # Index
        "farmer_login": "ರೈತ ಲಾಗಿನ್",
        "buyer_login": "ಖರೀದಿದಾರ ಲಾಗಿನ್",
        "hyperlocal_tag": "ಸ್ಥಳೀಯ ಕೃಷಿ ಮಾರುಕಟ್ಟೆ",
        "welcome_title": "ಹತ್ತಿರದ ರೈತರಿಂದ ತಾಜಾ ಉತ್ಪನ್ನಗಳು ನೇರವಾಗಿ ಖರೀದಿದಾರರಿಗೆ",
        "welcome_subtitle": "Farm2Table ರೈತರಿಗೆ ಸ್ಥಳೀಯ ಸಮುದಾಯಗಳನ್ನು ನಿರ್ಮಿಸಲು, ಬೆಳೆ ಸ್ಟಾಕ್ ಸೇರಿಸಲು ಮತ್ತು ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲದೆ ಹತ್ತಿರದ ಖರೀದಿದಾರರೊಂದಿಗೆ ನೇರವಾಗಿ ಸಂಪರ್ಕಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
        "enter_farmer": "ರೈತ ಪೋರ್ಟಲ್‌ಗೆ ಪ್ರವೇಶಿಸಿ",
        "enter_buyer": "ಖರೀದಿದಾರ ಪೋರ್ಟಲ್‌ಗೆ ಪ್ರವೇಶಿಸಿ",
        "platform_features": "ವೇದಿಕೆಯ ವೈಶಿಷ್ಟ್ಯಗಳು",
        "platform_subtitle": "ರೈತರು ಮತ್ತು ಖರೀದಿದಾರರನ್ನು ಸ್ಥಳೀಯವಾಗಿ ಸಂಪರ್ಕಿಸಲು ಬೇಕಾದ ಎಲ್ಲವೂ.",
        "farmer_dashboard": "ರೈತ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "farmer_dashboard_desc": "ರೈತರು ಬೆಳೆಗಳನ್ನು ಸೇರಿಸಬಹುದು, ಸ್ಟಾಕ್ ನಿರ್ವಹಿಸಬಹುದು ಮತ್ತು ಆರ್ಡರ್‌ಗಳನ್ನು ಸ್ವೀಕರಿಸಬಹುದು.",
        "buyer_dashboard": "ಖರೀದಿದಾರ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "buyer_dashboard_desc": "ಖರೀದಿದಾರರು ಹತ್ತಿರದ ರೈತರನ್ನು ಕಂಡುಹಿಡಿದು ನೇರವಾಗಿ ಆರ್ಡರ್ ಮಾಡಬಹುದು.",
        "nearby_communities": "ಹತ್ತಿರದ ಸಮುದಾಯಗಳು",
        "nearby_communities_desc": "10 ಕಿಮೀ ಒಳಗಿನ GPS ಆಧಾರಿತ ಸಮುದಾಯ ಹುಡುಕಾಟ.",
        "live_crop_inventory": "ತಾಜಾ ಬೆಳೆ ಸ್ಟಾಕ್",
        "live_crop_inventory_desc": "ರೈತರು ಸೇರಿಸಿದ ನಿಜವಾದ ಬೆಳೆ ಸ್ಟಾಕ್ ನೋಡಿ.",
        "community_selling": "ಸಮುದಾಯ ಆಧಾರಿತ ಮಾರಾಟ",
        "community_selling_desc": "ಖರೀದಿದಾರರ ಬೇಡಿಕೆಯನ್ನು ಪೂರೈಸಲು ಅನೇಕ ರೈತರು ಒಟ್ಟಾಗಿ ಕೆಲಸ ಮಾಡುತ್ತಾರೆ.",
        "farmer_communication": "ರೈತರ ಸಂವಹನ",
        "farmer_communication_desc": "ರೈತರಿಂದ ರೈತರಿಗೆ ಸಹಕಾರದ ಸಮುದಾಯ ಚಾಟ್.",
        "cta_title": "ಕೃಷಿಭೂಮಿ ಮತ್ತು ಕುಟುಂಬಗಳನ್ನು ಸಂಪರ್ಕಿಸುವ ಸುಧಾರಿತ ಮಾರ್ಗ",
        "cta_desc": "ರೈತರಿಗೆ ಉತ್ತಮವಾಗಿ ಮಾರಾಟ ಮಾಡಲು ಮತ್ತು ಖರೀದಿದಾರರಿಗೆ ತಾಜಾ ಸ್ಥಳೀಯ ಉತ್ಪನ್ನಗಳನ್ನು ಸುಲಭವಾಗಿ ಹುಡುಕಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
        "footer_text": "ಸ್ಥಳೀಯ ರೈತರು ಮತ್ತು ಖರೀದಿದಾರರನ್ನು ನೇರವಾಗಿ ಸಂಪರ್ಕಿಸುತ್ತದೆ.",

        # Farmer Login
        "farmer_access": "ರೈತರ ಪ್ರವೇಶ",
        "welcome_back_farmer": "ನಿಮ್ಮ ಫಾರ್ಮ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಮತ್ತೆ ಸ್ವಾಗತ",
        "farmer_login_desc_long": "ನಿಮ್ಮ ಉತ್ಪನ್ನಗಳನ್ನು ನಿರ್ವಹಿಸಲು, ಬಂದ ಆರ್ಡರ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಲು, ನಿಮ್ಮ ಕೃಷಿ ಸಮುದಾಯದೊಂದಿಗೆ ಸಂಪರ್ಕದಲ್ಲಿರಲು ಮತ್ತು ಹತ್ತಿರದ ಖರೀದಿದಾರರಿಗೆ ನೇರವಾಗಿ ಮಾರಾಟ ಮುಂದುವರಿಸಲು ಲಾಗಿನ್ ಮಾಡಿ.",
        "manage_crops_easily": "ಬೆಳೆಗಳನ್ನು ಸುಲಭವಾಗಿ ನಿರ್ವಹಿಸಿ",
        "manage_crops_easily_desc": "ಬೆಳೆ ಪಟ್ಟಿ, ಬೆಲೆ, ಪ್ರಮಾಣ ಮತ್ತು ಲಭ್ಯತೆಯನ್ನು ಯಾವಾಗ ಬೇಕಾದರೂ ನವೀಕರಿಸಿ.",
        "track_buyer_orders": "ಖರೀದಿದಾರರ ಆರ್ಡರ್‌ಗಳನ್ನು ಗಮನಿಸಿ",
        "track_buyer_orders_desc": "ನಿಮ್ಮ ಉತ್ಪನ್ನಗಳಿಗಾಗಿ ಮಾಡಲಾದ ಎಲ್ಲಾ ಆರ್ಡರ್‌ಗಳನ್ನು ಒಂದೇ ಸರಳ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ ನೋಡಿ.",
        "community_support": "ಸಮುದಾಯ ಬೆಂಬಲ",
        "community_support_desc": "ನಿಮ್ಮ ಸ್ಥಳೀಯ ಸಮುದಾಯ ವ್ಯವಸ್ಥೆಯ ಮೂಲಕ ಹತ್ತಿರದ ರೈತರೊಂದಿಗೆ ಸಂಪರ್ಕದಲ್ಲಿರಿ.",
        "better_local_selling": "ಉತ್ತಮ ಸ್ಥಳೀಯ ಮಾರಾಟ",
        "better_local_selling_desc": "ಮಧ್ಯವರ್ತಿಗಳ ಮೇಲೆ ಅವಲಂಬಿಸದೆ ಹತ್ತಿರದ ಖರೀದಿದಾರರನ್ನು ನೇರವಾಗಿ ತಲುಪಿರಿ.",
        "enter_login_details_farmer": "ನಿಮ್ಮ ರೈತ ಪೋರ್ಟಲ್‌ಗೆ ಪ್ರವೇಶಿಸಲು ಲಾಗಿನ್ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ.",
        "login_to_dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಲಾಗಿನ್ ಮಾಡಿ",
        "new_farmer": "ಹೊಸ ರೈತರಾ?",
        "create_account": "ಖಾತೆ ರಚಿಸಿ",

        # Buyer Login
        "buyer_access": "ಖರೀದಿದಾರರ ಪ್ರವೇಶ",
        "buyer_login_title": "ಹತ್ತಿರದ ರೈತರಿಂದ ನೇರವಾಗಿ ತಾಜಾ ಉತ್ಪನ್ನಗಳನ್ನು ಖರೀದಿಸಿ",
        "buyer_login_desc_long": "ಹತ್ತಿರದ ಕೃಷಿ ಸಮುದಾಯಗಳನ್ನು ಅನ್ವೇಷಿಸಲು, ನಿಜವಾದ ಬೆಳೆ ಸ್ಟಾಕ್ ವೀಕ್ಷಿಸಲು ಮತ್ತು ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲದೆ ಸ್ಥಳೀಯ ರೈತರಿಂದ ನೇರ ಆರ್ಡರ್ ಮಾಡಲು ಲಾಗಿನ್ ಮಾಡಿ.",
        "nearby_community_access": "ಹತ್ತಿರದ ಸಮುದಾಯ ಪ್ರವೇಶ",
        "nearby_community_access_desc": "GPS ಆಧಾರಿತ ಹೊಂದಾಣಿಕೆಯಿಂದ ನಿಮ್ಮ ಸ್ಥಳದ ಹತ್ತಿರದ ಸಮುದಾಯಗಳನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ.",
        "fresh_product_discovery": "ತಾಜಾ ಉತ್ಪನ್ನ ಹುಡುಕಾಟ",
        "fresh_product_discovery_desc": "ರೈತರು ನೇರವಾಗಿ ಸೇರಿಸಿದ ತರಕಾರಿಗಳು, ಹಣ್ಣುಗಳು, ಧಾನ್ಯಗಳು ಮತ್ತು ಇತರ ಉತ್ಪನ್ನಗಳನ್ನು ನೋಡಿ.",
        "direct_farmer_orders": "ರೈತರಿಗೆ ನೇರ ಆರ್ಡರ್",
        "direct_farmer_orders_desc": "ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲದೆ ಆರ್ಡರ್ ಮಾಡಿ ಮತ್ತು ಸ್ಥಳೀಯ ಬೆಳೆಗಾರರೊಂದಿಗೆ ನೇರವಾಗಿ ಸಂಪರ್ಕಿಸಿ.",
        "trusted_local_produce": "ನಂಬಿಕಸ್ಥ ಸ್ಥಳೀಯ ಉತ್ಪನ್ನಗಳು",
        "trusted_local_produce_desc": "ತರಕಾರಿಗಳು, ಹಣ್ಣುಗಳು ಮತ್ತು ಬೆಳೆಗಳನ್ನು ಸ್ಥಳೀಯ ಫಾರ್ಮ್‌ಗಳಿಂದ ನೇರವಾಗಿ ಖರೀದಿಸಿ.",
        "enter_login_details_buyer": "ಖರೀದಿದಾರ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಪ್ರವೇಶಿಸಲು ನಿಮ್ಮ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ.",
        "new_buyer": "ಹೊಸ ಖರೀದಿದಾರರಾ?",

        # Farmer Register
        "farmer_onboarding": "ರೈತ ಸೇರ್ಪಡೆ",
        "start_selling_title": "ತಾಜಾ ಬೆಳೆಗಳನ್ನು ಸ್ಥಳೀಯ ಖರೀದಿದಾರರಿಗೆ ನೇರವಾಗಿ ಮಾರಾಟ ಪ್ರಾರಂಭಿಸಿ",
        "start_selling_desc": "Farm2Table ಸೇರಲು ನಿಮ್ಮ ರೈತ ಖಾತೆಯನ್ನು ರಚಿಸಿ. ನಿಮ್ಮ ಸ್ಥಳೀಯ ಹಾಜರಾತಿ ನಿರ್ಮಿಸಿ, ಹತ್ತಿರದ ಸಮುದಾಯಗಳೊಂದಿಗೆ ಸಂಪರ್ಕಿಸಿ, ನಿಮ್ಮ ಉತ್ಪನ್ನಗಳನ್ನು ಸೇರಿಸಿ ಮತ್ತು ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲದೆ ಖರೀದಿದಾರರಿಂದ ನೇರ ಆರ್ಡರ್‌ಗಳನ್ನು ಸ್ವೀಕರಿಸಿ.",
        "community_based_selling": "ಸಮುದಾಯ ಆಧಾರಿತ ಮಾರಾಟ",
        "community_based_selling_desc": "ಸ್ಥಳೀಯ ರೈತ ಸಮುದಾಯವನ್ನು ಸೇರಿ ಅಥವಾ ರಚಿಸಿ ಮತ್ತು ಒಟ್ಟಾಗಿ ಖರೀದಿದಾರರಿಗೆ ಪೂರೈಕೆ ಮಾಡಿ.",
        "direct_orders": "ನೇರ ಆರ್ಡರ್‌ಗಳು",
        "direct_orders_desc": "ನೀವು ಸೇರಿಸಿದ ಉತ್ಪನ್ನಗಳಿಗೆ ಖರೀದಿದಾರರಿಂದ ನೇರ ಆರ್ಡರ್‌ಗಳನ್ನು ಸ್ವೀಕರಿಸಿ.",
        "local_reach": "ಸ್ಥಳೀಯ ತಲುಪುವಿಕೆ",
        "local_reach_desc": "ವೇಗವಾದ ಮಾರಾಟ ಮತ್ತು ಉತ್ತಮ ನಂಬಿಕೆಗಾಗಿ ನಿಮ್ಮ ಬೆಳೆಗಳನ್ನು ಹತ್ತಿರದ ಖರೀದಿದಾರರಿಗೆ ತೋರಿಸಿ.",
        "simple_management": "ಸರಳ ನಿರ್ವಹಣೆ",
        "simple_management_desc": "ಉತ್ಪನ್ನಗಳು, ಆರ್ಡರ್‌ಗಳು ಮತ್ತು ಸಂವಹನವನ್ನು ಒಂದೇ ಸ್ಥಳದಲ್ಲಿ ನಿರ್ವಹಿಸಿ.",
        "farmer_registration": "ರೈತ ನೋಂದಣಿ",
        "farmer_registration_desc": "ನಿಮ್ಮ ಖಾತೆಯನ್ನು ರಚಿಸಿ ಮತ್ತು ಹತ್ತಿರದ ಖರೀದಿದಾರರಿಗಾಗಿ ನಿಮ್ಮ ಕೃಷಿ ಉತ್ಪನ್ನಗಳನ್ನು ಪಟ್ಟಿ ಮಾಡಲು ಪ್ರಾರಂಭಿಸಿ.",
        "create_farmer_account": "ರೈತ ಖಾತೆ ರಚಿಸಿ",
        "already_registered": "ಈಗಾಗಲೇ ನೋಂದಾಯಿಸಿದ್ದೀರಾ?",

        # Buyer Register
        "buyer_onboarding": "ಖರೀದಿದಾರ ಸೇರ್ಪಡೆ",
        "buyer_register_title": "ನಿಮ್ಮ ಹತ್ತಿರದ ತಾಜಾ ಸ್ಥಳೀಯ ಉತ್ಪನ್ನಗಳನ್ನು ಹುಡುಕಲು ಸೇರಿ",
        "buyer_register_desc": "ಹತ್ತಿರದ ರೈತ ಸಮುದಾಯಗಳನ್ನು ಅನ್ವೇಷಿಸಲು, ನಿಜವಾದ ಉತ್ಪನ್ನ ಪಟ್ಟಿಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಮತ್ತು ನಿಮ್ಮ ಪ್ರದೇಶದ ಸ್ಥಳೀಯ ರೈತರಿಂದ ನೇರ ಆರ್ಡರ್ ಮಾಡಲು ನಿಮ್ಮ ಖರೀದಿದಾರ ಖಾತೆಯನ್ನು ರಚಿಸಿ.",
        "direct_ordering": "ನೇರ ಆರ್ಡರ್",
        "direct_ordering_desc": "ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲದೆ ಆರ್ಡರ್ ಮಾಡಿ ಮತ್ತು ಸ್ಥಳೀಯ ಬೆಳೆಗಾರರೊಂದಿಗೆ ನೇರವಾಗಿ ಸಂಪರ್ಕಿಸಿ.",
        "better_accuracy": "ಉತ್ತಮ ಖಚಿತತೆ",
        "better_accuracy_desc": "ಸ್ಥಳ ಆಧಾರಿತ ದೃಶ್ಯತೆ ಖರೀದಿದಾರರಿಗೆ ಸಂಬಂಧಿತ ಹತ್ತಿರದ ಮಾರಾಟಗಾರರನ್ನು ಮಾತ್ರ ಕಂಡುಹಿಡಿಯಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
        "buyer_registration": "ಖರೀದಿದಾರ ನೋಂದಣಿ",
        "buyer_registration_desc": "ನಿಮ್ಮ ಖಾತೆಯನ್ನು ರಚಿಸಿ ಮತ್ತು ಹತ್ತಿರದ ರೈತರನ್ನು ಮತ್ತು ತಾಜಾ ಸ್ಥಳೀಯ ಉತ್ಪನ್ನಗಳನ್ನು ಅನ್ವೇಷಿಸಲು ಪ್ರಾರಂಭಿಸಿ.",
        "create_buyer_account": "ಖರೀದಿದಾರ ಖಾತೆ ರಚಿಸಿ",
        "location_note": "10 ಕಿಮೀ ಒಳಗಿನ ರೈತ ಸಮುದಾಯಗಳನ್ನು ತೋರಿಸಲು ನಿಮ್ಮ ಸ್ಥಳವನ್ನು ಬಳಸಲಾಗುತ್ತದೆ. ಉತ್ತಮ ಶಿಫಾರಸುಗಳಿಗಾಗಿ ದಯವಿಟ್ಟು ಸ್ಥಳ ಪ್ರವೇಶವನ್ನು ಅನುಮತಿಸಿ.",

        # Farmer Dashboard
        "smart_farming_panel": "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಪ್ಯಾನೆಲ್",
        "farmer_dashboard_desc_long": "ಸ್ಥಳೀಯ ಕೃಷಿಗಾಗಿ ನಿರ್ಮಿಸಲಾದ ಆಧುನಿಕ ಕೆಲಸದ ಸ್ಥಳದಿಂದ ನಿಮ್ಮ ಸಮುದಾಯ, ಉತ್ಪನ್ನಗಳು, ಖರೀದಿದಾರರ ಆರ್ಡರ್‌ಗಳು ಮತ್ತು ರೈತರ ಸಂವಹನವನ್ನು ನಿರ್ವಹಿಸಿ.",
        "farmer_tools": "ರೈತ ಉಪಕರಣಗಳು",
        "buyer_discovery_radius": "ಖರೀದಿದಾರರ ಹುಡುಕಾಟ ವ್ಯಾಪ್ತಿ",
        "live_inventory": "ತಾಜಾ ಉತ್ಪನ್ನ ಸ್ಟಾಕ್",
        "create_community": "ಸಮುದಾಯ ರಚಿಸಿ",
        "create_local_farmer_community": "ಸ್ಥಳೀಯ ರೈತ ಸಮುದಾಯವನ್ನು ರಚಿಸಿ ಮತ್ತು ನಿಮ್ಮ ಪ್ರದೇಶದ ಹತ್ತಿರದ ಬೆಳೆಗಾರರೊಂದಿಗೆ ಸಹಕರಿಸಿ.",
        "add_crop": "ಬೆಳೆ ಸೇರಿಸಿ",
        "add_new_farm_products": "ಹತ್ತಿರದ ಖರೀದಿದಾರರಿಗಾಗಿ ಬೆಲೆ, ಪ್ರಮಾಣ ಮತ್ತು ಸ್ಟಾಕ್ ವಿವರಗಳೊಂದಿಗೆ ಹೊಸ ಕೃಷಿ ಉತ್ಪನ್ನಗಳನ್ನು ಸೇರಿಸಿ.",
        "community_inventory": "ಸಮುದಾಯ ಸ್ಟಾಕ್",
        "view_all_available_products": "ನಿಮ್ಮ ಸಮುದಾಯದೊಳಗಿನ ರೈತರು ನೀಡಿರುವ ಎಲ್ಲಾ ಲಭ್ಯ ಉತ್ಪನ್ನಗಳನ್ನು ನೋಡಿ.",
        "community_chat": "ಸಮುದಾಯ ಚಾಟ್",
        "communicate_fellow_farmers": "ಇತರೆ ರೈತರೊಂದಿಗೆ ಸಂವಹನ ಮಾಡಿ, ಪೂರೈಕೆಯನ್ನು ಸಂಯೋಜಿಸಿ ಮತ್ತು ಸಂಪರ್ಕದಲ್ಲಿರಿ.",
        "buyer_orders": "ಖರೀದಿದಾರರ ಆರ್ಡರ್‌ಗಳು",
        "track_orders_manage": "ಖರೀದಿದಾರರು ಮಾಡಿದ ಆರ್ಡರ್‌ಗಳನ್ನು ಗಮನಿಸಿ, ಕೇಳಲಾದ ಪ್ರಮಾಣವನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಪೂರೈಕೆಯನ್ನು ನಿರ್ವಹಿಸಿ.",

        # Create Community
        "community_setup": "ಸಮುದಾಯ ಸಿದ್ಧತೆ",
        "create_farmer_community_title": "ನಿಮ್ಮ ಸ್ಥಳೀಯ ಪ್ರದೇಶದಲ್ಲಿ ರೈತ ಸಮುದಾಯವನ್ನು ರಚಿಸಿ",
        "create_farmer_community_desc": "ಹತ್ತಿರದ ರೈತರು ಸಹಕರಿಸಲು, ಒಟ್ಟಿಗೆ ಸ್ಟಾಕ್ ನಿರ್ವಹಿಸಲು ಮತ್ತು ನಿಮ್ಮ ಪ್ರದೇಶದ ಖರೀದಿದಾರರಿಗೆ ಲಭ್ಯತೆಯನ್ನು ಸುಧಾರಿಸಲು ಸ್ಥಳೀಯ ಕೃಷಿ ಸಮುದಾಯವನ್ನು ಪ್ರಾರಂಭಿಸಿ.",
        "gps_based_community": "GPS ಆಧಾರಿತ ಸಮುದಾಯ",
        "gps_based_community_desc": "ನಿಮ್ಮ ಸಮುದಾಯವನ್ನು ಸರಿಯಾಗಿ ಸ್ಥಾಪಿಸಲು ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಸ್ಥಳವನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ದಾಖಲಿಸಲಾಗುತ್ತದೆ.",
        "farmer_collaboration": "ರೈತರ ಸಹಕಾರ",
        "farmer_collaboration_desc": "ಸಮುದಾಯಗಳು ಅನೇಕ ರೈತರಿಗೆ ಒಟ್ಟಾಗಿ ಕೆಲಸ ಮಾಡಿ ಹೆಚ್ಚು ಖರೀದಿದಾರರಿಗೆ ಸೇವೆ ಮಾಡಲು ಅವಕಾಶ ಕೊಡುತ್ತವೆ.",
        "nearby_buyer_reach": "ಹತ್ತಿರದ ಖರೀದಿದಾರರನ್ನು ತಲುಪುವುದು",
        "nearby_buyer_reach_desc": "ಸ್ಥಳೀಯ ದೂರದ ಹೊಂದಾಣಿಕೆಯನ್ನು ಆಧರಿಸಿ ಖರೀದಿದಾರರು ನಿಮ್ಮ ಸಮುದಾಯವನ್ನು ಕಂಡುಹಿಡಿಯಬಹುದು.",
        "smarter_selling": "ಸ್ಮಾರ್ಟ್ ಮಾರಾಟ",
        "smarter_selling_desc": "ಬಲವಾದ ಸಮುದಾಯವು ಸ್ಟಾಕ್ ದೃಶ್ಯತೆ, ನಂಬಿಕೆ ಮತ್ತು ಸ್ಥಳೀಯ ಪೂರೈಕೆಯನ್ನು ಸುಧಾರಿಸುತ್ತದೆ.",
        "create_community_desc_form": "ನಿಮ್ಮ ಸಮುದಾಯದ ಹೆಸರನ್ನು ನಿಗದಿಪಡಿಸಿ ಮತ್ತು ವೇದಿಕೆ ನಿಮ್ಮ ಸ್ಥಳವನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಹಿಡಿಯಲು ಬಿಡಿ.",
        "enter_community_name": "ಸಮುದಾಯದ ಹೆಸರನ್ನು ನಮೂದಿಸಿ",
        "location_capture_note": "ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಅಕ್ಷಾಂಶ ಮತ್ತು ರೇಖಾಂಶವನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಸೆರೆಹಿಡಿಯಲಾಗುತ್ತದೆ. ಕೇಳಿದಾಗ ದಯವಿಟ್ಟು ಸ್ಥಳ ಪ್ರವೇಶವನ್ನು ಅನುಮತಿಸಿ.",

        # Add Crop
        "crop_inventory": "ಬೆಳೆ ಸ್ಟಾಕ್",
        "add_fresh_crops_title": "ನಿಮ್ಮ ಕೃಷಿ ಸ್ಟಾಕ್‌ಗೆ ತಾಜಾ ಬೆಳೆಗಳನ್ನು ಸೇರಿಸಿ",
        "add_fresh_crops_desc": "ಬೆಲೆ, ಪ್ರಮಾಣ ಮತ್ತು ವಿವರಗಳೊಂದಿಗೆ ನಿಮ್ಮ ಉತ್ಪನ್ನಗಳನ್ನು ಸೇರಿಸಿ, ಹತ್ತಿರದ ಖರೀದಿದಾರರು ನಿಮ್ಮ ಸಮುದಾಯದಲ್ಲಿ ಏನು ಲಭ್ಯವಿದೆ ಎಂದು ನಿಖರವಾಗಿ ತಿಳಿಯಲು.",
        "real_time_stock": "ರಿಯಲ್-ಟೈಮ್ ಸ್ಟಾಕ್",
        "real_time_stock_desc": "ಸೇರಿಸಿದ ಉತ್ಪನ್ನಗಳನ್ನು ಮಾತ್ರ ಖರೀದಿದಾರರಿಗೆ ತೋರಿಸಲಾಗುತ್ತದೆ, ಇದರಿಂದ ಪಟ್ಟಿಗಳು ನಿಖರ ಮತ್ತು ಉಪಯುಕ್ತವಾಗುತ್ತವೆ.",
        "better_visibility": "ಉತ್ತಮ ದೃಶ್ಯತೆ",
        "better_visibility_desc": "ನಿಮ್ಮ ಬೆಳೆಗಳು ನಿಮ್ಮ ಸ್ಥಳೀಯ ಪ್ರದೇಶದ ಹತ್ತಿರದ ಖರೀದಿದಾರರು ಮತ್ತು ಸಮುದಾಯಗಳಿಗೆ ಗೋಚರವಾಗುತ್ತವೆ.",
        "simple_product_entry": "ಸರಳ ಉತ್ಪನ್ನ ನಮೂದು",
        "simple_product_entry_desc": "ಕೆಲವೇ ಕ್ಷೇತ್ರಗಳಲ್ಲಿ ಬೆಳೆ ಹೆಸರು, ಬೆಲೆ, ಪ್ರಮಾಣ ಮತ್ತು ವಿವರಣೆಯನ್ನು ಸೇರಿಸಿ.",
        "direct_local_orders": "ನೇರ ಸ್ಥಳೀಯ ಆರ್ಡರ್‌ಗಳು",
        "direct_local_orders_desc": "ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲದೆ ನಿಮ್ಮ ಲಭ್ಯ ಸ್ಟಾಕ್‌ನಿಂದ ಖರೀದಿದಾರರು ನೇರ ಆರ್ಡರ್ ಮಾಡಲು ಸಹಾಯ ಮಾಡಿ.",
        "add_crop_desc_form": "ನಿಮ್ಮ ಬೆಳೆ ವಿವರಗಳನ್ನು ಕೆಳಗೆ ನಮೂದಿಸಿ, ಹತ್ತಿರದ ಖರೀದಿದಾರರಿಗೆ ಲಭ್ಯವಾಗುವಂತೆ ಮಾಡಿ.",
        "enter_crop_name": "ಬೆಳೆ ಹೆಸರನ್ನು ನಮೂದಿಸಿ",
        "enter_price_per_kg": "ಪ್ರತಿ ಕೆ.ಜಿ.ಗೆ ಬೆಲೆಯನ್ನು ನಮೂದಿಸಿ",
        "enter_available_quantity": "ಲಭ್ಯ ಪ್ರಮಾಣವನ್ನು ನಮೂದಿಸಿ",
        "enter_product_description": "ಉತ್ಪನ್ನ ವಿವರಣೆಯನ್ನು ನಮೂದಿಸಿ",
        "add_crop_inventory_button": "ಸ್ಟಾಕ್‌ಗೆ ಬೆಳೆ ಸೇರಿಸಿ",

        # Buyer Dashboard
        "buyer_dashboard_desc_long": "ಹತ್ತಿರದ ರೈತ ಸಮುದಾಯಗಳನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ, ಲಭ್ಯವಿರುವ ತಾಜಾ ಉತ್ಪನ್ನಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ಮತ್ತು ನಿಮ್ಮ ಹತ್ತಿರದ ಸ್ಥಳೀಯ ಬೆಳೆಗಾರರಿಂದ ನೇರ ಆರ್ಡರ್ ಮಾಡಿ.",
        "fresh_nearby_products": "ಹತ್ತಿರದ ತಾಜಾ ಉತ್ಪನ್ನಗಳು",
        "available_products": "ಲಭ್ಯವಿರುವ ಉತ್ಪನ್ನಗಳು",
        "nearby_radius": "ಹತ್ತಿರದ ವ್ಯಾಪ್ತಿ",
        "nearby_farmer_communities": "ಹತ್ತಿರದ ರೈತ ಸಮುದಾಯಗಳು",
        "nearby_farmer_communities_desc": "ಈ ಸಮುದಾಯಗಳು ನಿಮ್ಮ ಸ್ಥಳದ ಹತ್ತಿರ ಲಭ್ಯವಿದ್ದು, ನಂಬಿಕಸ್ತ ಸ್ಥಳೀಯ ರೈತರನ್ನು ಹೆಚ್ಚು ನಿಖರವಾಗಿ ಕಂಡುಹಿಡಿಯಲು ಸಹಾಯ ಮಾಡುತ್ತವೆ.",
        "farmers_in_this_community": "ಈ ಸಮುದಾಯದ ರೈತರು:",
        "no_farmers_yet": "ಇನ್ನೂ ರೈತರಿಲ್ಲ",
        "no_nearby_communities": "ಹತ್ತಿರದ ಸಮುದಾಯಗಳಿಲ್ಲ",
        "no_nearby_communities_desc": "ನಿಮ್ಮ ಹತ್ತಿರದ ವ್ಯಾಪ್ತಿಯಲ್ಲಿ ಯಾವುದೇ ಸಮುದಾಯಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",
        "available_products_nearby": "ಹತ್ತಿರದ ರೈತರಿಂದ ಲಭ್ಯವಿರುವ ಉತ್ಪನ್ನಗಳು",
        "available_products_nearby_desc": "ನಿಮ್ಮ ಹತ್ತಿರದ ಸಮುದಾಯಗಳ ರೈತರು ತಮ್ಮ ಸ್ಟಾಕ್‌ಗೆ ಈಗಾಗಲೇ ಸೇರಿಸಿದ ಉತ್ಪನ್ನಗಳನ್ನು ವೀಕ್ಷಿಸಿ.",
        "no_products_available": "ಯಾವುದೇ ಉತ್ಪನ್ನಗಳಿಲ್ಲ",
        "no_products_available_desc": "ಪ್ರಸ್ತುತ ಹತ್ತಿರದ ರೈತ ಸಮುದಾಯಗಳಿಂದ ಯಾವುದೇ ಉತ್ಪನ್ನಗಳು ಲಭ್ಯವಿಲ್ಲ.",
        "distance": "ದೂರ",

        # Community Inventory
        "community_inventory_desc_long": "ನಿಮ್ಮ ಸಮುದಾಯದ ರೈತರು ನೀಡಿರುವ ಬೆಳೆಗಳನ್ನು ನೋಡಿ, ಸ್ಟಾಕ್ ಲಭ್ಯತೆಯನ್ನು ಗಮನಿಸಿ ಮತ್ತು ನಿಮ್ಮ ಸ್ಥಳೀಯ ಕೃಷಿ ಜಾಲದ ಒಟ್ಟು ಪೂರೈಕೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ.",
        "shared_crop_inventory": "ಹಂಚಿಕೆಯ ಬೆಳೆ ಸ್ಟಾಕ್",
        "available_crop_types": "ಲಭ್ಯ ಬೆಳೆ ಪ್ರಕಾರಗಳು",
        "inventory_visibility": "ಸ್ಟಾಕ್ ದೃಶ್ಯತೆ",
        "farmer_contribution": "ರೈತರ ಕೊಡುಗೆ",
        "no_crops_available_desc": "ಪ್ರಸ್ತುತ ನಿಮ್ಮ ಸಮುದಾಯದ ಸ್ಟಾಕ್‌ನಲ್ಲಿ ಯಾವುದೇ ಬೆಳೆಗಳು ಲಭ್ಯವಿಲ್ಲ.",

        # Community Chat
        "community_chat_desc_long": "ನಿಮ್ಮ ಸಮುದಾಯದ ರೈತರೊಂದಿಗೆ ಸಂಪರ್ಕ ಸಾಧಿಸಿ, ಸ್ಟಾಕ್ ಸಂಯೋಜಿಸಿ, ಲಭ್ಯತೆಯನ್ನು ಚರ್ಚಿಸಿ ಮತ್ತು ಹೆಚ್ಚು ಪರಿಣಾಮಕಾರಿಯಾಗಿ ಸಹಕರಿಸಿ.",
        "farmer_discussion_space": "ರೈತರ ಚರ್ಚಾ ಸ್ಥಳ",
        "community_messages": "ಸಮುದಾಯ ಸಂದೇಶಗಳು",
        "community_messages_desc": "ಸಂದೇಶವನ್ನು ಟೈಪ್ ಮಾಡಿ ಅಥವಾ ಮಾತನ್ನು ಪಠ್ಯವಾಗಿ ಪರಿವರ್ತಿಸಲು ಮೈಕ್ ಬಳಸಿ.",
        "type_message": "ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಟೈಪ್ ಮಾಡಿ...",
        "no_messages_yet": "ಇನ್ನೂ ಯಾವುದೇ ಸಂದೇಶಗಳಿಲ್ಲ. ಸಂಭಾಷಣೆಯನ್ನು ಪ್ರಾರಂಭಿಸಿ!",
        "voice_not_supported": "ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಧ್ವನಿ ಇನ್‌ಪುಟ್ ಬೆಂಬಲಿತವಾಗಿಲ್ಲ.",
        "listening": "ಕೇಳಲಾಗುತ್ತಿದೆ... ಈಗ ಮಾತನಾಡಿ",
        "voice_captured": "ಧ್ವನಿ ದಾಖಲಿಸಲಾಗಿದೆ",
        "voice_error": "ಧ್ವನಿ ದೋಷ",

        # Farmer Orders
        "farmer_orders": "ರೈತ ಆರ್ಡರ್‌ಗಳು",
        "farmer_orders_desc_long": "ಖರೀದಿದಾರರು ಮಾಡಿದ ಆರ್ಡರ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ, ಕೇಳಲಾದ ಪ್ರಮಾಣವನ್ನು ಗಮನಿಸಿ ಮತ್ತು ನಿಮ್ಮ ಫಾರ್ಮ್ ಸ್ಟಾಕ್‌ನಿಂದ ಪೂರೈಕೆಯನ್ನು ನಿರ್ವಹಿಸಿ.",
        "buyer_orders_overview": "ಖರೀದಿದಾರರ ಆರ್ಡರ್ ಅವಲೋಕನ",
        "total_orders": "ಒಟ್ಟು ಆರ್ಡರ್‌ಗಳು",
        "buyer_connections": "ಖರೀದಿದಾರರ ಸಂಪರ್ಕಗಳು",
        "order_tracking": "ಆರ್ಡರ್ ಟ್ರ್ಯಾಕಿಂಗ್",
        "local_fulfillment": "ಸ್ಥಳೀಯ ಪೂರೈಕೆ",
        "no_orders_received": "ಇನ್ನೂ ಯಾವುದೇ ಆರ್ಡರ್‌ಗಳು ಬಂದಿಲ್ಲ.",

        # Place order
        "place_order": "ಆರ್ಡರ್ ಮಾಡಿ",
        "order_quantity": "ಆರ್ಡರ್ ಪ್ರಮಾಣ",
        "enter_quantity": "ಪ್ರಮಾಣ ನಮೂದಿಸಿ",
        "confirm_order": "ಆರ್ಡರ್ ದೃಢೀಕರಿಸಿ",

        # Messages from routes
        "msg_farmer_registered": "ರೈತ ಯಶಸ್ವಿಯಾಗಿ ನೋಂದಾಯಿಸಲಾಗಿದೆ!",
        "msg_buyer_registered": "ಖರೀದಿದಾರ ಯಶಸ್ವಿಯಾಗಿ ನೋಂದಾಯಿಸಲಾಗಿದೆ!",
        "msg_invalid_credentials": "ತಪ್ಪಾದ ವಿವರಗಳು",
        "msg_allow_location": "ದಯವಿಟ್ಟು ಸ್ಥಳ ಮಾಹಿತಿಗೆ ಅನುಮತಿ ನೀಡಿ.",
        "msg_community_created": "ಸಮುದಾಯ ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ!",
        "msg_product_added": "ಉತ್ಪನ್ನ ಯಶಸ್ವಿಯಾಗಿ ಸೇರಿಸಲಾಗಿದೆ!",
        "msg_not_in_community": "ನೀವು ಯಾವುದೇ ಸಮುದಾಯದ ಭಾಗವಾಗಿಲ್ಲ.",
        "msg_buyer_not_found": "ಖರೀದಿದಾರ ಕಂಡುಬಂದಿಲ್ಲ.",
        "msg_product_not_found": "ಉತ್ಪನ್ನ ಕಂಡುಬಂದಿಲ್ಲ",
        "msg_order_success": "ಆರ್ಡರ್ ಯಶಸ್ವಿಯಾಗಿ ಮಾಡಲಾಗಿದೆ!",
        "msg_no_community": "ನೀವು ಯಾವುದೇ ಸಮುದಾಯದಲ್ಲಿ ಇಲ್ಲ.",

        "farm_trust_report": "ಫಾರ್ಮ್ ಟ್ರಸ್ಟ್ ರಿಪೋರ್ಟ್",
        "farm_trust_desc": "ಈ ಬೆಳೆ ಹೇಗೆ ಬೆಳೆದಿತು, ಯಾವ ಇನ್‌ಪುಟ್‌ಗಳನ್ನು ಬಳಸಲಾಯಿತು ಮತ್ತು AI ರಚಿಸಿದ ಪಾರದರ್ಶಕತಾ ಸಾರಾಂಶವನ್ನು ನೋಡಿ.",
        "farming_details": "ಕೃಷಿ ವಿವರಗಳು",
        "farming_method": "ಕೃಷಿ ವಿಧಾನ",
        "pesticide_used": "ಬಳಸಿದ ಕೀಟನಾಶಕ",
        "fertilizer_used": "ಬಳಸಿದ ರಸಗೊಬ್ಬರ",
        "harvest_date": "ಕೊಯ್ಲು ದಿನಾಂಕ",
        "storage_method": "ಸಂಗ್ರಹ ವಿಧಾನ",
        "ai_health_insight": "AI ಆರೋಗ್ಯ ವಿಶ್ಲೇಷಣೆ",
        "not_specified": "ಸೂಚಿಸಲಾಗಿಲ್ಲ",
        "not_assigned": "ನಿಗದಿಪಡಿಸಲಾಗಿಲ್ಲ",
        "view_farm_trust_report": "ಫಾರ್ಮ್ ಟ್ರಸ್ಟ್ ರಿಪೋರ್ಟ್ ನೋಡಿ",
        "basic_product_details": "ಮೂಲ ಉತ್ಪನ್ನ ವಿವರಗಳು",
        "farm_trust_details": "ಫಾರ್ಮ್ ಟ್ರಸ್ಟ್ ರಿಪೋರ್ಟ್ ವಿವರಗಳು",
        "select_farming_method": "ಕೃಷಿ ವಿಧಾನವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "organic_farming": "ಸೈವಿಕ ಕೃಷಿ",
        "natural_farming": "ನೈಸರ್ಗಿಕ ಕೃಷಿ",
        "regular_farming": "ಸಾಮಾನ್ಯ ಕೃಷಿ",
        "trust_report_hint": "ಈ ವಿವರಗಳು ಖರೀದಿದಾರರಿಗೆ ಬೆಳೆ ಹೇಗೆ ಬೆಳೆದಿತು ಎಂಬುದನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಸಹಾಯ ಮಾಡುತ್ತವೆ ಮತ್ತು ಫಾರ್ಮ್ ಟ್ರಸ್ಟ್ ರಿಪೋರ್ಟ್ ಮೂಲಕ ನಂಬಿಕೆಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತವೆ.",
        "ai_summary_text": "ಈ ಬೆಳೆ {method} ವಿಧಾನವನ್ನು ಬಳಸಿಕೊಂಡು ಬೆಳೆದಿದೆ. ಬಳಸಿದ ಕೀಟನಾಶಕ: {pesticide}.  ರೈತ ನೀಡಿದ ಮಾಹಿತಿಯ ಆಧಾರದ ಮೇಲೆ ಈ ಉತ್ಪನ್ನ ಮನೆ ಬಳಕೆಗೆ ಸೂಕ್ತವಾಗಿದೆ.",

        "low_chemical_use": "ಕಡಿಮೆ ರಾಸಾಯನಿಕ ಬಳಕೆ",
        "natural_protection": "ನೈಸರ್ಗಿಕ ರಕ್ಷಣೆ ಬಳಸಲಾಗಿದೆ",
        "chemical_use_declared": "ರೈತ ಘೋಷಿಸಿದ ರಾಸಾಯನಿಕ ಬಳಕೆ",
        "organic_crop": "ಸೈವಿಕ ಬೆಳೆ",
        "fresh_harvest": "ತಾಜಾ ಕೊಯ್ಲು",
        "freshness_not_declared": "ತಾಜಾತನ ಘೋಷಿಸಲಾಗಿಲ್ಲ",

        "farmer_ai_insights": "ಎಐ ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಒಳನೋಟಗಳು",
        "ai_page_desc": "ಬೆಳೆ ಬೇಡಿಕೆ, ಲಾಭ ಮತ್ತು ಖರೀದಿದಾರರ ಚಟುವಟಿಕೆಗಳನ್ನು ರೈತರು ಸುಲಭವಾಗಿ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಸಹಾಯ ಮಾಡುವ ದೃಶ್ಯ ಮಾಹಿತಿ.",

        "products_listed": "ಪಟ್ಟಿಯಲ್ಲಿರುವ ಉತ್ಪನ್ನಗಳು",
        "total_orders": "ಒಟ್ಟು ಆದೇಶಗಳು",
        "total_revenue": "ಒಟ್ಟು ಆದಾಯ",
        "estimated_profit": "ಅಂದಾಜು ಲಾಭ",

        "crop_demand": "ಬೆಳೆ ಬೇಡಿಕೆ",
        "monthly_earnings": "ಮಾಸಿಕ ಆದಾಯ",
        "price_trend": "ಬೆಲೆ ಪ್ರವೃತ್ತಿ",
        "community_activity": "ಸಮುದಾಯ ಚಟುವಟಿಕೆ",

        "farm_trust_score": "ಫಾರ್ಮ್ ವಿಶ್ವಾಸ ಅಂಕ",
        "crop_transparency": "ಬೆಳೆ ಪಾರದರ್ಶಕತೆ",
        "natural_farming": "ಸ್ವಾಭಾವಿಕ ಕೃಷಿ",
        "storage_quality": "ಸಂಗ್ರಹ ಗುಣಮಟ್ಟ",
        "freshness": "ತಾಜಾತನ",

        "ai_suggestions": "ಎಐ ಸಲಹೆಗಳು",
        "demand_tip": "ಬೇಡಿಕೆ ಸಲಹೆ",
        "price_tip": "ಬೆಲೆ ಸಲಹೆ",
        "community_tip": "ಸಮುದಾಯ ಸಲಹೆ",
        "weather_tip": "ಹವಾಮಾನ ಸಲಹೆ",

        "low_stock_alerts": "ಕಡಿಮೆ ಸಂಗ್ರಹ ಎಚ್ಚರಿಕೆ",

        "profit_summary": "ಲಾಭ ಸಾರಾಂಶ",
        "top_crop": "ಅತ್ಯುತ್ತಮ ಬೆಳೆ",
        "join_or_create_community": "ಸಮುದಾಯಕ್ಕೆ ಸೇರಿ ಅಥವಾ ಹೊಸದು ರಚಿಸಿ",
        "join_or_create_desc": "ನಿಮ್ಮ ಹತ್ತಿರದ ರೈತ ಸಮುದಾಯಗಳನ್ನು ನೋಡಿ. ಈಗಾಗಲೇ ಇರುವ ಸಮುದಾಯಕ್ಕೆ ಸೇರಿ ಅಥವಾ ಅಗತ್ಯವಿದ್ದರೆ ಹೊಸ ಸಮುದಾಯವನ್ನು ರಚಿಸಿ."
    }
}



def get_lang():
    return session.get("lang", "en")


@app.context_processor
def inject_translator():
    lang = get_lang()
    return {
        "t": translations.get(lang, translations["en"]),
        "lang": lang
    }


@app.route("/set_language/<lang_code>")
def set_language(lang_code):
    if lang_code in ["en", "kn"]:
        session["lang"] = lang_code
    return redirect(request.referrer or "/")


# ---------------------------------
# HELPERS
# ---------------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371

    dLat = math.radians(float(lat2) - float(lat1))
    dLon = math.radians(float(lon2) - float(lon1))

    a = (
        math.sin(dLat / 2) ** 2
        + math.cos(math.radians(float(lat1)))
        * math.cos(math.radians(float(lat2)))
        * math.sin(dLon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def connect_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def generate_health_report(product):

    lang = get_lang()
    t = translations[lang]

    farming_method = (product["farming_method"] or "").strip()
    pesticide_used = (product["pesticide_used"] or "").strip()
    

    pesticide_lower = pesticide_used.lower()

    # Safety detection
    if pesticide_lower in ["none", "no", "not used", "nil"]:
        safety = t.get("low_chemical_use", "Low Chemical Use")
    elif "neem" in pesticide_lower or "organic" in pesticide_lower:
        safety = t.get("natural_protection", "Natural Protection Used")
    else:
        safety = t.get("chemical_use_declared", "Farmer Declared Chemical Use")

    # Farming badge
    if "organic" in farming_method.lower():
        badge = t.get("organic_crop", "Organic Crop")
    elif "natural" in farming_method.lower():
        badge = t.get("natural_farming", "Natural Farming")
    else:
        badge = t.get("regular_farming", "Regular Farming")

    # Freshness
    
    
    # Multilingual summary
    summary = t["ai_summary_text"].format(
        method=farming_method or t["not_specified"],
        pesticide=pesticide_used or t["not_specified"],
        
    )

    return {
        
        "safety": safety,
        "badge": badge,
        "summary": summary
    }

def get_product_fallback_image(product_name):
    name = (product_name or "").strip().lower()

    if "onion" in name:
        return "https://images.pexels.com/photos/4197445/pexels-photo-4197445.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "tomato" in name or "tomatoes" in name:
        return "https://images.pexels.com/photos/533280/pexels-photo-533280.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "carrot" in name or "carrots" in name:
        return "https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "potato" in name or "potatoes" in name or "aloo" in name:
        return "https://images.pexels.com/photos/144248/potatoes-vegetables-food-agriculture-144248.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "banana" in name:
        return "https://images.pexels.com/photos/2872755/pexels-photo-2872755.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "cabbage" in name:
        return "https://images.pexels.com/photos/5945904/pexels-photo-5945904.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "brinjal" in name or "eggplant" in name or "baingan" in name:
        return "https://images.pexels.com/photos/321551/pexels-photo-321551.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "chilli" in name or "chili" in name or "mirchi" in name:
        return "https://images.pexels.com/photos/1435904/pexels-photo-1435904.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "corn" in name or "maize" in name:
        return "https://images.pexels.com/photos/547263/pexels-photo-547263.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "rice" in name:
        return "https://images.pexels.com/photos/7421204/pexels-photo-7421204.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "wheat" in name:
        return "https://images.pexels.com/photos/326082/pexels-photo-326082.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "apple" in name:
        return "https://images.pexels.com/photos/102104/pexels-photo-102104.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "mango" in name:
        return "https://images.pexels.com/photos/918643/pexels-photo-918643.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "grapes" in name or "grape" in name:
        return "https://images.pexels.com/photos/708777/pexels-photo-708777.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "beans" in name or "bean" in name:
        return "https://images.pexels.com/photos/1435895/pexels-photo-1435895.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "spinach" in name or "palak" in name:
        return "https://images.pexels.com/photos/2329440/pexels-photo-2329440.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "cauliflower" in name:
        return "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=800"
    elif "okra" in name or "lady finger" in name or "bhindi" in name:
        return "https://images.pexels.com/photos/5507737/pexels-photo-5507737.jpeg?auto=compress&cs=tinysrgb&w=800"
    else:
        return "https://images.pexels.com/photos/2252584/pexels-photo-2252584.jpeg?auto=compress&cs=tinysrgb&w=800"




def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()


# ---------------------------------
# DATABASE TABLES
# ---------------------------------
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            password TEXT,
            community_id INTEGER,
            latitude REAL,
            longitude REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS communities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')

    cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    quantity REAL NOT NULL,
    unit TEXT NOT NULL,
    farming_method TEXT,
    pesticide_used TEXT,
    product_image TEXT,
    product_video TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(farmer_id) REFERENCES farmers(id)
)
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            password TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buyer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(buyer_id) REFERENCES buyers(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            community_id INTEGER,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER ,
            media_type TEXT,
            file_path TEXT,
            caption TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    conn.commit()
    conn.close()


create_tables()


# ---------------------------------
# ROUTES
# ---------------------------------
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/farmer_register', methods=['GET', 'POST'])
def farmer_register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO farmers (name, phone, password, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
            (name, phone, password, latitude, longitude)
        )
        conn.commit()
        conn.close()

        flash(translations[get_lang()]["msg_farmer_registered"],"success")
        return redirect('/farmer_login') 
    
    return render_template("farmer_register.html")

@app.route('/crop_report/<int:product_id>')
def crop_report(product_id):
    if 'buyer_id' not in session:
        return redirect('/buyer_login')

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            products.id,
            products.name,
            products.description,
            products.price,
            products.quantity,
            products.unit,
            products.farming_method,
            products.pesticide_used,
            products.product_image,
            products.product_video,
            farmers.name AS farmer_name,
            farmers.phone AS farmer_phone,
            communities.name AS community_name
        FROM products
        JOIN farmers ON products.farmer_id = farmers.id
        LEFT JOIN communities ON farmers.community_id = communities.id
        WHERE products.id = ?
    """, (product_id,))

    product = cursor.fetchone()
    conn.close()

    if not product:
        return translations[get_lang()]["msg_product_not_found"], 404

    report = generate_health_report(product)

    return render_template(
        "crop_report.html",
        product=product,
        report=report,
        t=translations[get_lang()],
        lang=get_lang()
    )

@app.route('/buyer_register', methods=['GET', 'POST'])
def buyer_register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO buyers (name, phone, password, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, password, latitude, longitude))
        conn.commit()
        conn.close()

        flash(translations[get_lang()]["msg_buyer_registered"],"success")
        return redirect('/buyer_login') 

    return render_template("buyer_register.html")


@app.route('/farmer_login', methods=['GET', 'POST'])
def farmer_login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM farmers WHERE phone=? AND password=?", (phone, password))
        farmer = cursor.fetchone()
        conn.close()

        if farmer:
            session['farmer_id'] = farmer[0]
            return redirect('/farmer_dashboard')
        else:
            flash(translations[get_lang()]["msg_invalid_credentials"], "error")
            return redirect('/farmer_login')

    return render_template("farmer_login.html")


@app.route('/farmer_dashboard')
def farmer_dashboard():
    if 'farmer_id' not in session:
        return redirect('/farmer_login')

    farmer_id = session['farmer_id']
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT communities.name
        FROM farmers
        LEFT JOIN communities ON farmers.community_id = communities.id
        WHERE farmers.id=?
    """, (farmer_id,))
    row = cursor.fetchone()
    community_name = row[0] if row and row[0] else "Not joined"

    cursor.execute("SELECT COUNT(*) FROM products WHERE farmer_id=?", (farmer_id,))
    total_products = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE products.farmer_id=?
    """, (farmer_id,))
    total_orders = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT products.name, SUM(orders.quantity) AS sold_qty
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE products.farmer_id=?
        GROUP BY products.id, products.name
        ORDER BY sold_qty DESC
        LIMIT 1
    """, (farmer_id,))
    row = cursor.fetchone()
    top_crop = row[0] if row else "No sales yet"

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE farmer_id=? AND quantity <= 5
    """, (farmer_id,))
    low_stock_count = cursor.fetchone()[0] or 0

    cursor.execute("PRAGMA table_info(products)")
    columns = [r[1] for r in cursor.fetchall()]
    col_index = {col: i for i, col in enumerate(columns)}

    cursor.execute("SELECT * FROM products WHERE farmer_id=?", (farmer_id,))
    product_rows = cursor.fetchall()

    trust_score = 0
    if total_products > 0:
        total_score = 0
        for p in product_rows:
            has_name = bool(p[col_index["name"]]) if "name" in col_index else False
            has_desc = bool(p[col_index["description"]]) if "description" in col_index else False
            has_farming = bool(p[col_index["farming_method"]]) if "farming_method" in col_index else False
            has_harvest = bool(p[col_index["harvest_date"]]) if "harvest_date" in col_index else False
            has_storage = bool(p[col_index["storage_method"]]) if "storage_method" in col_index else False
            has_image = bool(p[col_index["product_image"]]) if "product_image" in col_index else False

            filled = sum([has_name, has_desc, has_farming, has_harvest, has_storage, has_image])
            total_score += (filled / 6) * 100

        trust_score = round(total_score / total_products)

    if total_orders == 0:
        ai_demand_tip = "You have listed products, but no orders yet. Add clear crop details and photos."
    else:
        ai_demand_tip = f"{top_crop} is your best selling crop right now."

    if low_stock_count > 0:
        ai_stock_tip = f"You have {low_stock_count} low-stock product(s). Refill them soon."
    else:
        ai_stock_tip = "Your stock looks stable."

    ai_activity_tip = f"You have listed {total_products} products and received {total_orders} orders."

    conn.close()

    return render_template(
        "farmer_dashboard.html",
        t=translations[get_lang()],
        lang=get_lang(),
        community_name=community_name,
        total_products=total_products,
        total_orders=total_orders,
        top_crop=top_crop,
        low_stock_count=low_stock_count,
        trust_score=trust_score,
        ai_demand_tip=ai_demand_tip,
        ai_stock_tip=ai_stock_tip,
        ai_activity_tip=ai_activity_tip
    )

@app.route('/create_community', methods=['GET', 'POST'])
def create_community():
    if 'farmer_id' not in session:
        return redirect('/farmer_login')

    if request.method == 'POST':
        name = request.form['name'].strip()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        if not latitude or not longitude:
            return translations[get_lang()]["msg_allow_location"]

        conn = connect_db()
        cursor = conn.cursor()

        # Check if community already exists with same name
        cursor.execute("SELECT id FROM communities WHERE LOWER(name) = LOWER(?)", (name,))
        existing = cursor.fetchone()

        if existing:
            community_id = existing[0]
        else:
            cursor.execute("""
                INSERT INTO communities (name, latitude, longitude)
                VALUES (?, ?, ?)
            """, (name, latitude, longitude))
            conn.commit()
            community_id = cursor.lastrowid

        # Assign farmer to this community
        cursor.execute("""
            UPDATE farmers
            SET community_id = ?
            WHERE id = ?
        """, (community_id, session['farmer_id']))

        conn.commit()
        conn.close()

        flash(translations[get_lang()]["msg_community_created"],"success")
        return redirect('/farmer_dashboard') 

    return render_template(
        "create_community.html",
        t=translations[get_lang()],
        lang=get_lang()
    )

@app.route('/add_crop', methods=['GET', 'POST'])
def add_crop():
    if 'farmer_id' not in session:
        return redirect('/farmer_login')

    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        price = float(request.form['price'])
        quantity = float(request.form['quantity'])
        unit = request.form.get('unit', 'kg')

        farming_method = request.form.get('farming_method', '')
        pesticide_used = request.form.get('pesticide_used', '')
        

        product_image = request.files.get('product_image')
        product_video = request.files.get('product_video')

        image_filename = None
        video_filename = None

        if product_image and product_image.filename:
            image_filename = secure_filename(product_image.filename)
            product_image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        if product_video and product_video.filename:
            video_filename = secure_filename(product_video.filename)
            product_video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO products (
                farmer_id, name, description, price, quantity, unit,
                farming_method, pesticide_used, product_image, product_video
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session['farmer_id'],
            name,
            description,
            price,
            quantity,
            unit,
            farming_method,
            pesticide_used,
            image_filename,
            video_filename
        ))

        db.commit()
        flash(translations[get_lang()]["msg_product_added"],"success")
        return redirect('/farmer_dashboard')    
    return render_template("add_crop.html")


@app.route('/community_inventory')
def community_inventory():
    if 'farmer_id' not in session:
        return redirect('/farmer_login')

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT community_id FROM farmers WHERE id=?", (session['farmer_id'],))
    community = cursor.fetchone()

    if not community or not community[0]:
        conn.close()
        return translations[get_lang()]["msg_not_in_community"]

    community_id = community[0]

    cursor.execute("""
        SELECT products.name,
               AVG(products.price) as avg_price,
               SUM(products.quantity) as total_quantity
        FROM products
        JOIN farmers ON products.farmer_id = farmers.id
        WHERE farmers.community_id = ?
        GROUP BY products.name
    """, (community_id,))

    inventory = cursor.fetchall()
    conn.close()

    return render_template("community_inventory.html", inventory=inventory)


@app.route('/buyer_login', methods=['GET', 'POST'])
def buyer_login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buyers WHERE phone=? AND password=?", (phone, password))
        buyer = cursor.fetchone()
        conn.close()

        if buyer:
            session['buyer_id'] = buyer[0]
            return redirect('/buyer_dashboard')
        else:
            flash(translations[get_lang()]["msg_invalid_credentials"], "error")
        return redirect('/buyer_login')

    return render_template("buyer_login.html")


@app.route('/buyer_dashboard')
def buyer_dashboard():
    if 'buyer_id' not in session:
        return redirect('/buyer_login')

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT latitude, longitude FROM buyers WHERE id=?", (session['buyer_id'],))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return translations[get_lang()]["msg_buyer_not_found"]

    buyer_lat, buyer_lon = result

    cursor.execute("SELECT id, name, latitude, longitude FROM communities")
    all_communities = cursor.fetchall()

    nearby_communities = []
    for comm in all_communities:
        comm_id, comm_name, comm_lat, comm_lon = comm
        distance = calculate_distance(buyer_lat, buyer_lon, comm_lat, comm_lon)

        if distance <= 10:
            nearby_communities.append({
                "id": comm_id,
                "name": comm_name,
                "distance": round(distance, 2),
                "farmers": []
            })

    for comm in nearby_communities:
        cursor.execute("""
            SELECT id, name, phone
            FROM farmers
            WHERE community_id = ?
        """, (comm["id"],))

        farmers = cursor.fetchall()
        farmer_list = []

        for farmer in farmers:
            farmer_list.append({
                "id": farmer[0],
                "name": farmer[1],
                "phone": farmer[2],
                "distance": comm["distance"]
            })

        comm["farmers"] = farmer_list

    products = []
    for comm in nearby_communities:
        cursor.execute("""
            SELECT
                products.id,
                products.name,
                products.price,
                products.quantity,
                products.product_image,
                farmers.name,
                farmers.phone
            FROM products
            JOIN farmers ON products.farmer_id = farmers.id
            WHERE farmers.community_id = ?
        """, (comm['id'],))

        for row in cursor.fetchall():
            products.append({
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "quantity": row[3],
                "product_image": row[4],
                "farmer_name": row[5],
                "farmer_phone": row[6],
                "community_name": comm['name'],
                "distance": comm['distance']
            })

    conn.close()

    return render_template(
        "buyer_dashboard.html",
        nearby_communities=nearby_communities,
        products=products,
        t=translations[get_lang()],
        lang=get_lang()
    )

@app.route("/place_order/<int:product_id>", methods=["GET", "POST"])
def place_order(product_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    if not product:
        return translations[get_lang()]["msg_product_not_found"], 404

    if request.method == "POST":
        quantity = request.form.get("quantity")
        buyer_id = session.get('buyer_id')
        if not buyer_id:
            return redirect('/buyer_login')

        cursor.execute(
            "INSERT INTO orders (buyer_id, product_id, quantity) VALUES (?, ?, ?)",
            (buyer_id, product_id, quantity)
        )
        db.commit()
        flash(translations[get_lang()]["msg_order_placed"],"success")
        return redirect('/buyer_dashboard') 
    return render_template("place_order.html", product=product)


@app.route('/farmer_orders')
def farmer_orders():
    if 'farmer_id' not in session:
        return redirect('/farmer_login')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            orders.id,
            products.name AS product_name,
            orders.quantity,
            (orders.quantity * products.price) AS total_price,
            buyers.name AS buyer_name,
            buyers.phone AS buyer_phone,
            orders.order_date
        FROM orders
        JOIN products ON orders.product_id = products.id
        JOIN buyers ON orders.buyer_id = buyers.id
        WHERE products.farmer_id = ?
        ORDER BY orders.order_date DESC
    """, (session['farmer_id'],))

    orders = cursor.fetchall()
    return render_template("farmer_orders.html", orders=orders)


@app.route('/community_chat', methods=['GET', 'POST'])
def community_chat():
    if 'farmer_id' not in session:
        return redirect('/farmer_login')

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT community_id FROM farmers WHERE id=?", (session['farmer_id'],))
    result = cursor.fetchone()

    if not result or not result[0]:
        conn.close()
        return translations[get_lang()]["msg_no_community"]

    community_id = result[0]

    if request.method == 'POST':
        message = request.form['message']

        cursor.execute("""
            INSERT INTO messages (farmer_id, community_id, message)
            VALUES (?, ?, ?)
        """, (session['farmer_id'], community_id, message))

        conn.commit()

    cursor.execute("""
        SELECT farmers.name, messages.message
        FROM messages
        JOIN farmers ON messages.farmer_id = farmers.id
        WHERE messages.community_id = ?
        ORDER BY messages.created_at ASC
    """, (community_id,))

    chats = cursor.fetchall()
    conn.close()

    return render_template("community_chat.html", chats=chats)


@app.route('/view_products/<int:community_id>')
def view_products(community_id):
    if 'buyer_id' not in session:
        return redirect('/buyer_login')

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT products.name, products.price, products.quantity
        FROM products
        JOIN farmers ON products.farmer_id = farmers.id
        WHERE farmers.community_id = ?
    """, (community_id,))

    products = cursor.fetchall()
    conn.close()

    return render_template("view_products.html", products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'buyer_id' not in session:
        return redirect('/buyer_login')

    cart = session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        cart[pid] += 1
    else:
        cart[pid] = 1

    session['cart'] = cart
    flash("Product added to cart successfully.", "success")
    return redirect('/buyer_dashboard#products-section')

@app.route('/buyer_cart')
def buyer_cart():
    if 'buyer_id' not in session:
        return redirect('/buyer_login')

    cart = session.get('cart', {})
    conn = connect_db()
    cursor = conn.cursor()

    cart_items = []
    grand_total = 0

    for pid, qty in cart.items():
        cursor.execute("""
            SELECT products.id, products.name, products.price, products.quantity, farmers.name
            FROM products
            JOIN farmers ON products.farmer_id = farmers.id
            WHERE products.id = ?
        """, (pid,))
        product = cursor.fetchone()

        if product:
            subtotal = product[2] * qty
            grand_total += subtotal
            cart_items.append({
                "id": product[0],
                "name": product[1],
                "price": product[2],
                "available_quantity": product[3],
                "farmer_name": product[4],
                "cart_quantity": qty,
                "subtotal": subtotal
            })

    conn.close()

    return render_template(
        "buyer_cart.html",
        cart_items=cart_items,
        grand_total=grand_total,
        t=translations[get_lang()],
        lang=get_lang()
    )

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    session['cart'] = cart
    flash("Product removed from cart.", "success")
    return redirect('/buyer_cart')

@app.route('/place_cart_order', methods=['POST'])
def place_cart_order():
    if 'buyer_id' not in session:
        return redirect('/buyer_login')

    buyer_id = session['buyer_id']
    cart = session.get('cart', {})

    if not cart:
        flash("Your cart is empty.", "error")
        return redirect('/buyer_cart')

    conn = connect_db()
    cursor = conn.cursor()

    for pid, qty in cart.items():
        cursor.execute("""
            INSERT INTO orders (buyer_id, product_id, quantity)
            VALUES (?, ?, ?)
        """, (buyer_id, int(pid), qty))

    conn.commit()
    conn.close()

    session['cart'] = {}
    flash("Your order has been placed successfully.", "success")
    return redirect('/buyer_cart')

from datetime import datetime
import calendar

@app.route('/farmer_ai_insights')
def farmer_ai_insights():
    if 'farmer_id' not in session:
        return redirect('/farmer_login')

    farmer_id = session['farmer_id']
    conn = connect_db()
    cursor = conn.cursor()

    # ---------- basic stats ----------
    cursor.execute("SELECT COUNT(*) FROM products WHERE farmer_id=?", (farmer_id,))
    total_products = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE products.farmer_id=?
    """, (farmer_id,))
    total_orders = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(orders.quantity * products.price)
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE products.farmer_id=?
    """, (farmer_id,))
    total_revenue = cursor.fetchone()[0] or 0

    # ---------- top crop ----------
    cursor.execute("""
        SELECT products.name, SUM(orders.quantity) AS sold_qty
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE products.farmer_id=?
        GROUP BY products.id, products.name
        ORDER BY sold_qty DESC
        LIMIT 1
    """, (farmer_id,))
    top_crop_row = cursor.fetchone()
    top_crop = top_crop_row[0] if top_crop_row else "No sales yet"
    top_crop_qty = top_crop_row[1] if top_crop_row else 0

    # ---------- crop demand chart ----------
    cursor.execute("""
        SELECT products.name, SUM(orders.quantity) AS sold_qty
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE products.farmer_id=?
        GROUP BY products.id, products.name
        ORDER BY sold_qty DESC
        LIMIT 6
    """, (farmer_id,))
    demand_rows = cursor.fetchall()

    demand_labels = [row[0] for row in demand_rows] if demand_rows else ["No sales"]
    demand_values = [float(row[1]) for row in demand_rows] if demand_rows else [0]

    # ---------- monthly earnings: last 6 months from real orders ----------
    cursor.execute("""
        SELECT strftime('%Y-%m', orders.order_date) AS ym,
               SUM(orders.quantity * products.price) AS revenue
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE products.farmer_id=?
        GROUP BY ym
        ORDER BY ym DESC
        LIMIT 6
    """, (farmer_id,))
    month_rows = cursor.fetchall()
    month_rows.reverse()

    earnings_labels = []
    earnings_values = []

    for ym, revenue in month_rows:
        try:
            dt = datetime.strptime(ym, "%Y-%m")
            earnings_labels.append(dt.strftime("%b %Y"))
        except:
            earnings_labels.append(ym)
        earnings_values.append(round(float(revenue or 0), 2))

    if not earnings_labels:
        earnings_labels = ["No data"]
        earnings_values = [0]

    # ---------- buyer activity by weekday from real order dates ----------
    cursor.execute("""
        SELECT orders.order_date
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE products.farmer_id=?
    """, (farmer_id,))
    order_dates = cursor.fetchall()

    weekday_count = {
        "Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0,
        "Fri": 0, "Sat": 0, "Sun": 0
    }

    for row in order_dates:
        try:
            raw_date = row[0]
            dt = datetime.fromisoformat(str(raw_date).replace("Z", ""))
            day = dt.strftime("%a")
            if day in weekday_count:
                weekday_count[day] += 1
        except:
            pass

    activity_labels = list(weekday_count.keys())
    activity_values = list(weekday_count.values())

    # ---------- current crop prices (real current prices, not fake trend) ----------
    cursor.execute("""
        SELECT name, price
        FROM products
        WHERE farmer_id=?
        ORDER BY created_at DESC
        LIMIT 6
    """, (farmer_id,))
    price_rows = cursor.fetchall()

    price_labels = [row[0] for row in price_rows] if price_rows else ["No products"]
    price_values = [float(row[1]) for row in price_rows] if price_rows else [0]

    # ---------- low stock ----------
    cursor.execute("""
        SELECT name, quantity
        FROM products
        WHERE farmer_id=? AND quantity <= 5
        ORDER BY quantity ASC
        LIMIT 5
    """, (farmer_id,))
    low_stock_raw = cursor.fetchall()
    low_stock_items = [{"name": row[0], "quantity": row[1]} for row in low_stock_raw]

    # ---------- real trust score from available product details ----------
    cursor.execute("PRAGMA table_info(products)")
    product_columns = [row[1] for row in cursor.fetchall()]

    # fetch all farmer products
    cursor.execute("SELECT * FROM products WHERE farmer_id=?", (farmer_id,))
    products_raw = cursor.fetchall()

    trust_crop = 0
    trust_natural = 0
    trust_storage = 0
    trust_freshness = 0

    if total_products > 0:
        # map column names to indexes
        col_index = {col: idx for idx, col in enumerate(product_columns)}

        detail_filled = 0
        natural_count = 0
        storage_count = 0
        fresh_count = 0

        for row in products_raw:
            # details completeness
            has_name = bool(row[col_index["name"]]) if "name" in col_index else False
            has_desc = bool(row[col_index["description"]]) if "description" in col_index else False
            has_image = bool(row[col_index["product_image"]]) if "product_image" in col_index else False
            if has_name and has_desc and has_image:
                detail_filled += 1

            # natural / organic
            if "farming_method" in col_index:
                fm = str(row[col_index["farming_method"]] or "").lower()
                if "organic" in fm or "natural" in fm:
                    natural_count += 1

            # storage
            if "storage_method" in col_index:
                if str(row[col_index["storage_method"]] or "").strip():
                    storage_count += 1

            # freshness
            if "harvest_date" in col_index:
                if str(row[col_index["harvest_date"]] or "").strip():
                    fresh_count += 1

        trust_crop = round((detail_filled / total_products) * 100)
        trust_natural = round((natural_count / total_products) * 100)
        trust_storage = round((storage_count / total_products) * 100) if "storage_method" in col_index else 0
        trust_freshness = round((fresh_count / total_products) * 100) if "harvest_date" in col_index else 0

    # ---------- real farmer-friendly insights ----------
    if total_orders == 0:
        ai_demand_tip = "You have not received orders yet. Add more crop details and clear crop photos."
    else:
        ai_demand_tip = f"{top_crop} is your best selling crop with {top_crop_qty} kg sold."

    if low_stock_items:
        ai_price_tip = f"{low_stock_items[0]['name']} stock is low. Refill it soon to avoid missed orders."
    else:
        ai_price_tip = "Your current stock looks stable."

    busiest_day = activity_labels[activity_values.index(max(activity_values))] if max(activity_values) > 0 else "No active day yet"
    ai_community_tip = f"Buyer activity is highest on {busiest_day}."

    if total_revenue > 0:
        weather_tip = f"You have earned ₹{round(total_revenue, 2)} in total sales so far."
    else:
        weather_tip = "Start listing more crops to improve visibility and get first orders."

    ai_summary = (
        f"You have listed {total_products} products and received {total_orders} orders. "
        f"Your total sales value is ₹{round(total_revenue, 2)}. "
        f"{top_crop} is currently your strongest crop."
    )

    conn.close()

    return render_template(
        "farmer_ai_insights.html",
        t=translations[get_lang()],
        lang=get_lang(),

        total_products=total_products,
        total_orders=total_orders,
        total_revenue=round(total_revenue, 2),
        total_cost=None,
        total_profit=None,
        top_crop=top_crop,

        demand_labels=demand_labels,
        demand_values=demand_values,

        earnings_labels=earnings_labels,
        earnings_values=earnings_values,

        price_labels=price_labels,
        price_values=price_values,

        activity_labels=activity_labels,
        activity_values=activity_values,

        low_stock_items=low_stock_items,

        ai_summary=ai_summary,
        ai_demand_tip=ai_demand_tip,
        ai_price_tip=ai_price_tip,
        ai_community_tip=ai_community_tip,
        weather_tip=weather_tip,

        trust_crop=trust_crop,
        trust_natural=trust_natural,
        trust_storage=trust_storage,
        trust_freshness=trust_freshness
    )

@app.route('/select_community')
def select_community():
    if 'farmer_id' not in session:
        return redirect('/farmer_login')

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT latitude, longitude FROM farmers WHERE id=?", (session['farmer_id'],))
    farmer = cursor.fetchone()

    if not farmer:
        conn.close()
        return "Farmer not found"

    farmer_lat, farmer_lon = farmer

    cursor.execute("SELECT id, name, latitude, longitude FROM communities")
    all_communities = cursor.fetchall()

    nearby_communities = []

    for comm in all_communities:
        comm_id, comm_name, comm_lat, comm_lon = comm
        distance = calculate_distance(farmer_lat, farmer_lon, comm_lat, comm_lon)

        if distance <= 10:
            cursor.execute("SELECT COUNT(*) FROM farmers WHERE community_id=?", (comm_id,))
            farmer_count = cursor.fetchone()[0]

            nearby_communities.append({
                "id": comm_id,
                "name": comm_name,
                "distance": round(distance, 2),
                "farmer_count": farmer_count
            })

    conn.close()

    return render_template(
        "select_community.html",
        nearby_communities=nearby_communities,
        t=translations[get_lang()],
        lang=get_lang()
    )

@app.route('/join_community/<int:community_id>')
def join_community(community_id):
    if 'farmer_id' not in session:
        return redirect('/farmer_login')

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE farmers SET community_id=? WHERE id=?",
        (community_id, session['farmer_id'])
    )

    conn.commit()
    conn.close()

    flash("Joined community successfully!", "success")
    return redirect('/farmer_dashboard')

@app.route("/delete_crop/<int:crop_id>", methods=["POST"])
def delete_crop(crop_id):

    if 'farmer_id' not in session:
        return redirect("/farmer_login")

    conn = sqlite3.connect("farmers.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=? AND farmer_id=?",
        (crop_id, session['farmer_id'])
    )

    conn.commit()
    conn.close()

    flash("Product removed from inventory", "success")

    return redirect("/community_inventory")



if __name__ == '__main__':
    port=int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
