"""
Script to generate Tableau-ready CSV datasets from the Trip Planner database.
This script extracts and flattens the hierarchical JSON data into multiple CSV files
suitable for data visualization in Tableau.
"""

import json
import csv
import os
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'processed', 'database.json')
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_database():
    """Load the main database JSON file."""
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_places_csv(data):
    """Generate places dimension table."""
    output_file = os.path.join(OUTPUT_DIR, 'places.csv')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['place_id', 'place_name', 'state', 'description', 'num_attractions', 'num_travel_options'])
        
        for place in data:
            num_attractions = len(place.get('attractions', []))
            num_travel = len(place.get('travel_options', []))
            writer.writerow([
                place.get('place_id', ''),
                place.get('place_name', ''),
                place.get('state', ''),
                place.get('description', ''),
                num_attractions,
                num_travel
            ])
    
    print(f"✅ Generated: {output_file}")
    return output_file

def generate_attractions_csv(data):
    """Generate tourist spots/attractions fact table."""
    output_file = os.path.join(OUTPUT_DIR, 'attractions.csv')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'spot_id', 'place_id', 'place_name', 'state', 'spot_name', 
            'description', 'num_dining_options', 'num_stay_options',
            'avg_dining_price', 'avg_stay_price', 'min_dining_price', 'max_dining_price',
            'min_stay_price', 'max_stay_price'
        ])
        
        for place in data:
            for spot in place.get('attractions', []):
                dining = spot.get('dining', [])
                stays = spot.get('accommodation', [])
                
                # Calculate dining stats
                dining_prices = [int(d.get('price_per_person', 0)) for d in dining if d.get('price_per_person')]
                avg_dining = sum(dining_prices) / len(dining_prices) if dining_prices else 0
                min_dining = min(dining_prices) if dining_prices else 0
                max_dining = max(dining_prices) if dining_prices else 0
                
                # Calculate stay stats
                stay_prices = [int(s.get('price_per_night', 0)) for s in stays if s.get('price_per_night')]
                avg_stay = sum(stay_prices) / len(stay_prices) if stay_prices else 0
                min_stay = min(stay_prices) if stay_prices else 0
                max_stay = max(stay_prices) if stay_prices else 0
                
                writer.writerow([
                    spot.get('spot_id', ''),
                    place.get('place_id', ''),
                    place.get('place_name', ''),
                    place.get('state', ''),
                    spot.get('spot_name', ''),
                    spot.get('description', ''),
                    len(dining),
                    len(stays),
                    round(avg_dining, 2),
                    round(avg_stay, 2),
                    min_dining,
                    max_dining,
                    min_stay,
                    max_stay
                ])
    
    print(f"✅ Generated: {output_file}")
    return output_file

def generate_dining_csv(data):
    """Generate dining options fact table with detailed pricing."""
    output_file = os.path.join(OUTPUT_DIR, 'dining_options.csv')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'food_id', 'spot_id', 'place_id', 'place_name', 'spot_name',
            'food_place_name', 'price_per_person', 'budget_range'
        ])
        
        for place in data:
            for spot in place.get('attractions', []):
                for dining in spot.get('dining', []):
                    writer.writerow([
                        dining.get('food_id', ''),
                        spot.get('spot_id', ''),
                        place.get('place_id', ''),
                        place.get('place_name', ''),
                        spot.get('spot_name', ''),
                        dining.get('food_place_name', ''),
                        dining.get('price_per_person', ''),
                        dining.get('budget_range', '')
                    ])
    
    print(f"✅ Generated: {output_file}")
    return output_file

def generate_accommodation_csv(data):
    """Generate accommodation options fact table."""
    output_file = os.path.join(OUTPUT_DIR, 'accommodation_options.csv')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'stay_id', 'spot_id', 'place_id', 'place_name', 'spot_name',
            'stay_name', 'price_per_night', 'budget_range'
        ])
        
        for place in data:
            for spot in place.get('attractions', []):
                for stay in spot.get('accommodation', []):
                    writer.writerow([
                        stay.get('stay_id', ''),
                        spot.get('spot_id', ''),
                        place.get('place_id', ''),
                        place.get('place_name', ''),
                        spot.get('spot_name', ''),
                        stay.get('stay_name', ''),
                        stay.get('price_per_night', ''),
                        stay.get('budget_range', '')
                    ])
    
    print(f"✅ Generated: {output_file}")
    return output_file

def generate_travel_options_csv(data):
    """Generate travel options fact table with cost and duration analysis."""
    output_file = os.path.join(OUTPUT_DIR, 'travel_options.csv')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'travel_id', 'place_id', 'place_name', 'source_city',
            'travel_mode', 'approx_cost', 'approx_duration_hours',
            'cost_per_hour', 'cost_category'
        ])
        
        for place in data:
            for travel in place.get('travel_options', []):
                cost = float(travel.get('approx_cost', 0))
                duration = float(travel.get('approx_duration_hours', 1))
                cost_per_hour = round(cost / duration, 2) if duration > 0 else 0
                
                # Categorize cost
                if cost < 1000:
                    cost_category = 'Budget'
                elif cost < 3000:
                    cost_category = 'Economy'
                elif cost < 5000:
                    cost_category = 'Standard'
                else:
                    cost_category = 'Premium'
                
                writer.writerow([
                    travel.get('travel_id', ''),
                    place.get('place_id', ''),
                    place.get('place_name', ''),
                    travel.get('source_city', ''),
                    travel.get('travel_mode', ''),
                    travel.get('approx_cost', ''),
                    travel.get('approx_duration_hours', ''),
                    cost_per_hour,
                    cost_category
                ])
    
    print(f"✅ Generated: {output_file}")
    return output_file

def generate_summary_stats_csv(data):
    """Generate aggregated summary statistics for dashboard KPIs."""
    output_file = os.path.join(OUTPUT_DIR, 'summary_statistics.csv')
    
    # Calculate stats
    total_places = len(data)
    total_attractions = sum(len(p.get('attractions', [])) for p in data)
    total_dining = sum(
        len(s.get('dining', []))
        for p in data
        for s in p.get('attractions', [])
    )
    total_stays = sum(
        len(s.get('accommodation', []))
        for p in data
        for s in p.get('attractions', [])
    )
    total_travel = sum(len(p.get('travel_options', [])) for p in data)
    
    # Source cities
    source_cities = set()
    travel_modes = set()
    travel_costs = []
    travel_durations = []
    
    for place in data:
        for travel in place.get('travel_options', []):
            source_cities.add(travel.get('source_city', ''))
            travel_modes.add(travel.get('travel_mode', ''))
            travel_costs.append(float(travel.get('approx_cost', 0)))
            travel_durations.append(float(travel.get('approx_duration_hours', 0)))
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['metric', 'value'])
        writer.writerow(['total_places', total_places])
        writer.writerow(['total_attractions', total_attractions])
        writer.writerow(['total_dining_options', total_dining])
        writer.writerow(['total_accommodation_options', total_stays])
        writer.writerow(['total_travel_routes', total_travel])
        writer.writerow(['unique_source_cities', len(source_cities)])
        writer.writerow(['unique_travel_modes', len(travel_modes)])
        writer.writerow(['avg_travel_cost', round(sum(travel_costs) / len(travel_costs), 2) if travel_costs else 0])
        writer.writerow(['min_travel_cost', min(travel_costs) if travel_costs else 0])
        writer.writerow(['max_travel_cost', max(travel_costs) if travel_costs else 0])
        writer.writerow(['avg_travel_duration_hours', round(sum(travel_durations) / len(travel_durations), 2) if travel_durations else 0])
        writer.writerow(['data_generated_on', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    
    print(f"✅ Generated: {output_file}")
    return output_file

def generate_travel_mode_analysis_csv(data):
    """Generate travel mode comparison analysis."""
    output_file = os.path.join(OUTPUT_DIR, 'travel_mode_analysis.csv')
    
    mode_stats = {}
    
    for place in data:
        for travel in place.get('travel_options', []):
            mode = travel.get('travel_mode', 'Unknown')
            cost = float(travel.get('approx_cost', 0))
            duration = float(travel.get('approx_duration_hours', 0))
            
            if mode not in mode_stats:
                mode_stats[mode] = {'costs': [], 'durations': [], 'count': 0}
            
            mode_stats[mode]['costs'].append(cost)
            mode_stats[mode]['durations'].append(duration)
            mode_stats[mode]['count'] += 1
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'travel_mode', 'total_routes', 'avg_cost', 'min_cost', 'max_cost',
            'avg_duration_hours', 'min_duration_hours', 'max_duration_hours'
        ])
        
        for mode, stats in mode_stats.items():
            writer.writerow([
                mode,
                stats['count'],
                round(sum(stats['costs']) / len(stats['costs']), 2),
                min(stats['costs']),
                max(stats['costs']),
                round(sum(stats['durations']) / len(stats['durations']), 2),
                min(stats['durations']),
                max(stats['durations'])
            ])
    
    print(f"✅ Generated: {output_file}")
    return output_file

def generate_source_city_analysis_csv(data):
    """Generate source city connectivity and cost analysis."""
    output_file = os.path.join(OUTPUT_DIR, 'source_city_analysis.csv')
    
    city_stats = {}
    
    for place in data:
        for travel in place.get('travel_options', []):
            city = travel.get('source_city', 'Unknown')
            cost = float(travel.get('approx_cost', 0))
            destination = place.get('place_name', '')
            
            if city not in city_stats:
                city_stats[city] = {
                    'destinations': set(),
                    'costs': [],
                    'count': 0
                }
            
            city_stats[city]['destinations'].add(destination)
            city_stats[city]['costs'].append(cost)
            city_stats[city]['count'] += 1
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'source_city', 'connected_destinations', 'total_routes',
            'avg_cost', 'min_cost', 'max_cost'
        ])
        
        for city, stats in city_stats.items():
            writer.writerow([
                city,
                len(stats['destinations']),
                stats['count'],
                round(sum(stats['costs']) / len(stats['costs']), 2),
                min(stats['costs']),
                max(stats['costs'])
            ])
    
    print(f"✅ Generated: {output_file}")
    return output_file

def generate_budget_distribution_csv(data):
    """Generate budget distribution analysis for dining and accommodation."""
    output_file = os.path.join(OUTPUT_DIR, 'budget_distribution.csv')
    
    results = []
    
    # Dining budget distribution
    dining_budgets = {'low': 0, 'mid': 0, 'high': 0}
    for place in data:
        for spot in place.get('attractions', []):
            for dining in spot.get('dining', []):
                budget_raw = dining.get('budget_range', '')
                budget = budget_raw.lower() if budget_raw else ''
                if budget in dining_budgets:
                    dining_budgets[budget] += 1
    
    for budget, count in dining_budgets.items():
        results.append(['Dining', budget.title(), count])
    
    # Accommodation budget distribution
    stay_budgets = {'low': 0, 'mid': 0, 'high': 0}
    for place in data:
        for spot in place.get('attractions', []):
            for stay in spot.get('accommodation', []):
                budget_raw = stay.get('budget_range', '')
                budget = budget_raw.lower() if budget_raw else ''
                if budget in stay_budgets:
                    stay_budgets[budget] += 1
    
    for budget, count in stay_budgets.items():
        results.append(['Accommodation', budget.title(), count])
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['category', 'budget_range', 'count'])
        writer.writerows(results)
    
    print(f"✅ Generated: {output_file}")
    return output_file

def main():
    """Main function to generate all Tableau datasets."""
    print("=" * 60)
    print("🚀 TripSync Tableau Data Export Tool")
    print("=" * 60)
    
    # Load data
    print("\n📂 Loading database...")
    data = load_database()
    print(f"   Loaded {len(data)} places\n")
    
    # Generate CSVs
    print("📊 Generating CSV files for Tableau...\n")
    
    files = []
    files.append(generate_places_csv(data))
    files.append(generate_attractions_csv(data))
    files.append(generate_dining_csv(data))
    files.append(generate_accommodation_csv(data))
    files.append(generate_travel_options_csv(data))
    files.append(generate_summary_stats_csv(data))
    files.append(generate_travel_mode_analysis_csv(data))
    files.append(generate_source_city_analysis_csv(data))
    files.append(generate_budget_distribution_csv(data))
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully generated {len(files)} CSV files!")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    print("\n📈 Tableau Visualization Suggestions:")
    print("   • Places map with attractions count")
    print("   • Travel cost comparison by mode (Bar/Line chart)")
    print("   • Budget distribution (Pie chart)")
    print("   • Source city connectivity (Network graph)")
    print("   • Price distribution (Histogram)")
    print("   • Travel duration vs cost scatter plot")
    print("=" * 60)

if __name__ == "__main__":
    main()
