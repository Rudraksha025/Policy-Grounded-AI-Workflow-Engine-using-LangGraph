from src.database import engine, Base, ComplianceEvent, ComplianceRequest

print("Creating compliance database tables...")

Base.metadata.create_all(bind=engine)

print("All tables created successfully.")
