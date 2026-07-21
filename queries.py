"""
Example queries and reporting functions.
"""
from sqlalchemy import text
from database import get_engine


def get_top_regions_by_arrivals(limit: int = 10):
    """
    Fetches the top regions based on total arrivals.
    
    Args:
        limit: The number of regions to return.
    """
    engine = get_engine()
    
    query = text(f"""
        SELECT geo_label, SUM(arrivals) AS arrivals
        FROM tourism_data
        GROUP BY geo_label
        ORDER BY arrivals DESC
        LIMIT :limit
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"limit": limit})
            
            print(f"\n--- Top {limit} Regions by Arrivals ---")
            for row in result:
                # row is a tuple-like object (geo_label, arrivals)
                print(f"{row[0]}: {row[1]:.0f}")
            print("---------------------------------------\n")
            
    except Exception as e:
        print(f"Error executing query: {e}")

if __name__ == "__main__":
    get_top_regions_by_arrivals()