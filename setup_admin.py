# setup_admin.py
"""
Script to create the initial admin user for the Mental Health AI Copilot.
Run this script once to set up your admin account.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.db import create_admins_table, register_admin

def setup_admin():
    """Setup initial admin user."""
    print("🔐 Mental Health AI Copilot - Admin Setup")
    print("=" * 50)
    
    # Create admin table
    create_admins_table()
    print("✅ Admin table created successfully!")
    
    # Default admin credentials
    email = "admin@mentalhealth.com"
    password = "admin123"
    
    print(f"\n📝 Creating default admin user:")
    print(f"Email: {email}")
    print(f"Password: {password}")
    
    # Register admin
    if register_admin(email, password):
        print(f"✅ Admin user '{email}' created successfully!")
        print("\n🎉 Setup complete! You can now access the admin dashboard.")
        print("📊 Navigate to: pages/Admin.py")
        print("\n⚠️  IMPORTANT: Change the default password after first login!")
    else:
        print(f"❌ Failed to create admin user. Email '{email}' might already exist.")
        print("ℹ️  Admin user may already be set up.")

if __name__ == "__main__":
    setup_admin()
