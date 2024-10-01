import subprocess
from dotenv import load_dotenv
import os
from gui import create_gui  # Import the GUI function

# Load environment variables from .env file
load_dotenv()

# Get the keys from environment variables
PUBLIC_KEY = os.getenv("LOGO_DEV_PUBLIC_KEY")
SECRET_KEY = os.getenv("LOGO_DEV_SECRET_KEY")

# Call the GUI function
create_gui()