# Patrol Route Optimization App

## Overview
Streamlit app applying Dijkstra’s algorithm and greedy selection to design efficient patrol routes. 
Handles blocked trails with dynamic rerouting, tracks distances, and visualizes patrol paths for wildlife monitoring.

## Features
- Shortest path calculation using Dijkstra’s algorithm
- Greedy patrol selection for nearest location
- Dynamic rerouting when trails are blocked
- Distance tracking and route visualization

## Tech Stack
- Python
- Streamlit
- NetworkX (graph algorithms)

## Installation
1. Clone the repo:
   git clone https://github.com/USERNAME/Wildlifepatrolplanner.git
2. Install dependencies:
   pip install -r requirements.txt
3. Run the app:
   streamlit run app.py

## Example
Start: Srisailam → Dam → Akka Mahadevi Caves → Farahabad → Mallela Theertham  
Total Distance: 16 km (vs. 11 km originally due to reroute)

## Future Scope
- GPS integration
- Multi-agent patrols
- Advanced algorithms (A*, dynamic programming)
