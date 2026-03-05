from app import create_app, db
from app.models import Vehicle
import os # Import os to check for instance folder

app = create_app()

def add_vehicles():
    """Adds placeholder vehicles to the database."""
    
    # Ensure the instance folder exists before trying database operations
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        try:
            os.makedirs(instance_path)
            print(f"Created instance folder at: {instance_path}")
        except OSError as e:
            print(f"Error creating instance folder: {e}")
            return # Exit if instance folder cannot be created

    # All database logic MUST be inside the app context
    with app.app_context():
        print("Deleting old vehicles...")
        # Use try-except for robustness during deletion
        try:
            num_deleted = Vehicle.query.delete()
            db.session.commit() # Commit deletion
            print(f"Deleted {num_deleted} old vehicle records.")
        except Exception as e:
            db.session.rollback() # Rollback if delete fails
            print(f"Error deleting vehicles: {e}")
            # Decide if you want to proceed or stop if deletion fails
            # return 

        vehicles = [
            # Hatchbacks
            Vehicle(name='Maruti Suzuki Swift', description='A popular and reliable hatchback, perfect for zipping through city traffic.',
                    image_file='swift.jpg',  # <-- LOCAL FILENAME
                    price_per_day=2200, category='Hatchback', passenger_capacity=5, fuel_type='Petrol'),
            Vehicle(name='Hyundai i20', description='A premium hatchback with a sporty design and feature-packed interior.',
                    image_file='i20.jpg',  # <-- LOCAL FILENAME
                    price_per_day=2500, category='Hatchback', passenger_capacity=5, fuel_type='Petrol'),
            Vehicle(name='Tata Altroz', description='A stylish Indian hatchback known for its 5-star safety rating.',
                    image_file='altroz.jpg',  # <-- LOCAL FILENAME
                    price_per_day=2400, category='Hatchback', passenger_capacity=5, fuel_type='Diesel'),
            
            # Sedans
            Vehicle(name='Honda City', description='The benchmark for comfort and refinement in the sedan category.',
                    image_file='city.jpg',  # <-- LOCAL FILENAME
                    price_per_day=3500, category='Sedan', passenger_capacity=5, fuel_type='Petrol'),
            Vehicle(name='Hyundai Verna', description='A powerful and feature-loaded sedan with a striking design.',
                    image_file='verna.jpg',  # <-- LOCAL FILENAME
                    price_per_day=3400, category='Sedan', passenger_capacity=5, fuel_type='Diesel'),
            
            # SUVs
            Vehicle(name='Hyundai Creta', description='India\'s most popular SUV, balancing size, features, and performance.',
                    image_file='creta.jpg',  # <-- LOCAL FILENAME
                    price_per_day=4000, category='SUV', passenger_capacity=5, fuel_type='Diesel'),
            Vehicle(name='Mahindra XUV700', description='A technologically advanced and spacious SUV for the whole family.',
                    image_file='xuv700.jpg',  # <-- LOCAL FILENAME
                    price_per_day=5500, category='SUV', passenger_capacity=7, fuel_type='Petrol'),
            Vehicle(name='Kia Seltos', description='A stylish and modern SUV packed with premium features.',
                    image_file='seltos.jpg',  # <-- LOCAL FILENAME
                    price_per_day=4200, category='SUV', passenger_capacity=5, fuel_type='Petrol'),
            
            # MUVs
            Vehicle(name='Toyota Innova Crysta', description='The undisputed king of MUVs, known for reliability and comfort.',
                    image_file='innova.jpg',  # <-- LOCAL FILENAME
                    price_per_day=6000, category='MUV', passenger_capacity=7, fuel_type='Diesel'),
            Vehicle(name='Maruti Suzuki Ertiga', description='A practical and economical 7-seater MUV for families.',
                    image_file='ertiga.jpg',  # <-- LOCAL FILENAME
                    price_per_day=3800, category='MUV', passenger_capacity=7, fuel_type='Petrol')
        ]
        
        try:
            print(f"Adding {len(vehicles)} new vehicle records...")
            db.session.add_all(vehicles)
            db.session.commit() # Commit additions
            print("Successfully added new vehicles.")
        except Exception as e:
            db.session.rollback() # Rollback if add fails
            print(f"Error adding vehicles: {e}")

    print("Database setup script finished.")

if __name__ == '__main__':
    add_vehicles()
