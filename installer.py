import shutil
import os

print("Installing GRAVITY...")
new_path = f"C:\\Users\\{os.getenv('username')}\\Documents"
shutil.move("GRAVITY", new_path)
print("Complete!")