import pandas as pd
import random
from faker import Faker

# Initialize Faker to generate realistic names and addresses
fake = Faker()

# Define the possible year_grade options
year_grades = ['1', '2', '3', '4', 'not_student']

# List to store the user data
user_data = []

# Generate 100 users
for _ in range(5):
    # Generate fake data for each user
    username = f"{random.randint(100000000, 999999999)}"  # Simulating National ID as username
    first_name = fake.first_name()
    last_name = fake.last_name()
    name = f"{first_name} {last_name}"  # Combine first and last name
    email = fake.email()
    phone_number = f"+20{random.randint(100000000, 999999999)}"
    year_grade = random.choice(year_grades)
    is_leader = random.choice([True, False])
    is_doctor = random.choice([True, False])
    is_teaching_assistant = random.choice([True, False])
    address = fake.address().replace("\n", " ")  # Make the address single-line
    national_id = f"{random.randint(10000000000000, 99999999999999)}"  # Simulate National ID

    # Append the generated data as a dictionary (fields ordered)
    user_data.append({
        'name': name,                # Full Name
        'national_id': national_id,  # National ID as first field
        'username': username,        # Username (simulated National ID)
        'first_name': first_name,    
        'last_name': last_name,      
        'email': email,              
        'phone_number': phone_number,
        'year_grade': year_grade,    
        'is_leader': is_leader,      
        'is_doctor': is_doctor,      
        'is_teaching_assistant': is_teaching_assistant,
        'address': address           
    })

# Create a DataFrame from the generated user data
df = pd.DataFrame(user_data)

# Save the DataFrame to an Excel file
file_path = 'user_data_with_name.xlsx'  # Specify your file path
df.to_excel(file_path, index=False)

print(f"File '{file_path}' has been created.")
