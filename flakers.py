from faker import Faker
import random
import csv

fake = Faker('en-IN')

#cuisine_types = ["Italian", "Chinese", "Mexican", "Indian", "Japanese", "Thai", "French", "American"]
#order_status = ["Pending", "Delivered", "Cancelled"]
#pament_mode = ["Credit", "Card", "Cash", "UPI"] 

def generate_customers(num_customers):
  customers = []
  for _ in range(num_customers):
    customer = {
      "customer_id": _+ 1,
      "name": fake.name(),
      "location": fake.address(),
      "phone": fake.phone_number(),
      "email": fake.email(),
      "signup_date": fake.date_between(start_date='-1y', end_date='now'),
      "is_premium": fake.pybool(),
      "preferred_cuisine":random.choice(["Italian", "Chinese", "Mexican", "Indian", "Japanese", "Thai", "French", "American"]),
      "total_orders": fake.random_int(min=0, max=11),
      "average_rating" : fake.random_int(min=1, max=5)
    }
    customers.append(customer)
  return customers

def generate_restaurants(num_restaurants):
  restaurants = []
  for _ in range(num_restaurants):
    restaurant = {
       #"restaurant_id": fake.org_id(min=1,max=100),
      "restaurant_id" : _+ 101,
      "name": fake.company(),
      "cuisine_type": random.choice(["Italian", "Chinese", "Mexican", "Indian", "Japanese", "Thai", "French", "American"]),
      "location": fake.address(),
      "owner_name" : fake.name(),
      "average_delivery_time" : fake.random_int(min=40,max=120),
      "contact_number": fake.phone_number(),
      "rating" : fake.random_int(min=0, max=5),
      "total_orders" : fake.random_int(min=5, max=48),
      "is_active" : fake.pybool()
    }
    restaurants.append(restaurant)
  return restaurants

def generate_orders(num_orders, customers, restaurants):
  orders = []
  for _ in range(num_orders):
    customer = random.choice(customers)
    restaurant = random.choice(restaurants)
    order = {
      "order_id": _+ 151,
      "customer_id": customer["customer_id"],
      "restaurant_id": restaurant["restaurant_id"],
      "order_date": fake.date_time_between(start_date='-1y', end_date='now'),
      "delivery_time":fake.random_int(min=40,max=120),
      "status":random.choice(["Pending", "Delivered", "Cancelled"]),
      "payment_mode":random.choice(["Credit", "Card", "Cash", "UPI"]),
      "discount_applied":fake.pybool(),
      #"items": [fake.word() for _ in range(random.randint(1, 5))],
      "total_price": round(random.uniform(125, 1200), 50),
      #"order_time": fake.date(start_date='-1y', end_date='now'),
      "rating" : fake.random_int(min=0, max=5),
    }
    orders.append(order)
  return orders

def generate_deliveries(num_deliveries, orders):
  deliveries = []
  for order in orders:
    #order = random.choice(orders)
    delivery = {
      "delivery_id": fake.uuid4(),
      "order_id": order["order_id"],
      "delivery_person": fake.name(),
      "delivery_status": order["status"],
      "distance": round(random.uniform(1, 12),1),
      #"delivery_time": fake.date_time_between(start_date=order["order_time"], end_date='now'),
      "delivery_time": order["delivery_time"],
      #"estimated_time": fake.date_time_between(start_date=order["order_time"], end_date='now'),
      "estimated_time" : order["delivery_time"]+5,
      "delivery_fee": round(random.uniform(50, 150)),
      "vehicle_type": random.choice(["Motorcycle", "Car", "Bicycle"])
    }
    deliveries.append(delivery)
  return deliveries

# Generate data
num_customers = 100
num_restaurants = 50
num_orders = 250

customers = generate_customers(num_customers)
restaurants = generate_restaurants(num_restaurants)
orders = generate_orders(num_orders, customers, restaurants)
deliveries = generate_deliveries(num_orders, orders)

def export_to_csv(data, filename):
  with open(filename, 'w', newline='') as csvfile:
    fieldnames = data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)

# Export data to CSV
export_to_csv(customers, "customers.csv")
export_to_csv(restaurants, "restaurants.csv")
export_to_csv(orders, "orders.csv")
export_to_csv(deliveries, "deliveries.csv")
