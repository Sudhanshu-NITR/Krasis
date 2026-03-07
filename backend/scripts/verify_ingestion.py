from app.scheduler.scheduler import run_ingestion_cycle

if __name__ == "__main__":
    print("Running verification...")
    run_ingestion_cycle()
    print("Verification complete.")
