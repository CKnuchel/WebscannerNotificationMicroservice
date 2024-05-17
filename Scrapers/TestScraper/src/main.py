from database import Base, engine

Base.metadata.create_all(bind=engine) # This creates the tables in the database