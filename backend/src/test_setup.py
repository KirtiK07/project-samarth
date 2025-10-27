"""
Quick test script to verify the setup
"""
import os
import sys

print("=" * 50)
print("Testing Samarth Setup")
print("=" * 50)

# Test 1: Check data files exist
print("\n1. Checking data files...")
data_dir = "../../data"
crop_file = os.path.join(data_dir, "crop_production.csv")
rainfall_file = os.path.join(data_dir, "rainfall_data.csv.csv")

if os.path.exists(crop_file):
    print(f"✓ Found crop_production.csv")
else:
    print(f"✗ Missing: {crop_file}")

if os.path.exists(rainfall_file):
    print(f"✓ Found rainfall_data.csv.csv")
else:
    print(f"✗ Missing: {rainfall_file}")

# Test 2: Check environment variables
print("\n2. Checking environment variables...")
groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    print(f"✓ GROQ_API_KEY is set")
else:
    print(f"✗ GROQ_API_KEY not found - Please create .env file with your Groq API key")

# Test 3: Try importing dependencies
print("\n3. Checking dependencies...")
try:
    import flask
    print(f"✓ Flask installed (version {flask.__version__})")
except ImportError:
    print("✗ Flask not installed - Run: pip install -r requirements.txt")

try:
    import pandas
    print(f"✓ Pandas installed (version {pandas.__version__})")
except ImportError:
    print("✗ Pandas not installed - Run: pip install -r requirements.txt")

try:
    import groq
    print(f"✓ Groq installed")
except ImportError:
    print("✗ Groq not installed - Run: pip install -r requirements.txt")

# Test 4: Try loading data
print("\n4. Testing data loading...")
try:
    from data_loader import DataLoader
    loader = DataLoader(data_dir=data_dir)
    summary = loader.get_data_summary()
    print(f"✓ Loaded {summary['crop_data']['rows']} crop data rows")
    print(f"✓ Loaded {summary['rainfall_data']['rows']} rainfall data rows")
except Exception as e:
    print(f"✗ Error loading data: {e}")

print("\n" + "=" * 50)
print("Setup test complete!")
print("=" * 50)

if groq_key:
    print("\n✓ Ready to start! Run: python app.py")
else:
    print("\n⚠ Please set GROQ_API_KEY in .env file before starting")
