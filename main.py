"""
Main Entry Point for the Greek Tourism Project.
Provides a CLI to manage the database and ETL processes.
"""
import argparse
import sys
import subprocess
import logging

from create_tables import init_db
from loader import load
from queries import get_top_regions_by_arrivals

def run_dashboard():
    """Runs the Streamlit dashboard."""
    print("Starting Streamlit Dashboard...")
    try:
        subprocess.run(["streamlit", "run", "app/🏛️_Dashboard.py"])
    except KeyboardInterrupt:
        print("\nDashboard stopped.")

def main():
    parser = argparse.ArgumentParser(description="Greek Tourism Data Management CLI")
    
    parser.add_argument(
        "--init-db", 
        action="store_true", 
        help="Initialize the database schema (create tables)"
    )
    
    parser.add_argument(
        "--load-data", 
        action="store_true", 
        help="Fetch data from API and load it into the database"
    )
    
    parser.add_argument(
        "--query-top", 
        type=int,
        metavar="N",
        help="Query and print the top N regions by arrivals"
    )

    parser.add_argument(
        "--dashboard", 
        action="store_true", 
        help="Run the Streamlit Dashboard"
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, print help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("app.log")]
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting Greek Tourism CLI")
        
    if args.init_db:
        init_db()
        
    if args.load_data:
        load()
        
    if args.query_top:
        get_top_regions_by_arrivals(limit=args.query_top)

    if args.dashboard:
        run_dashboard()

if __name__ == "__main__":
    main()
