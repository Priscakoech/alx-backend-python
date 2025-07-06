from seed import connect_to_prodev

def stream_user_ages():
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()

def compute_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average}")
if __name__ == "__main__":
    compute_average_age()