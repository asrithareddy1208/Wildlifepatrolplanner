import streamlit as st
import folium
from streamlit_folium import st_folium

from graph import graph
from algorithm import patrol_planner, remove_blocked_trail

if "route" not in st.session_state:
    st.session_state["route"] = None

if "distance" not in st.session_state:
    st.session_state["distance"] = None

if "original_distance" not in st.session_state:
    st.session_state["original_distance"] = None

if "blocked_trail" not in st.session_state:
    st.session_state["blocked_trail"] = "None"


# Wildlife locations
location_coords = {
    "Srisailam": (16.0750, 78.8726),
    "Srisailam Dam": (16.08653, 78.89702),
    "Mallela Theertham": (16.0, 78.65),
    "Akka Mahadevi Caves": (16.08, 78.95),
    "Farahabad": (16.35, 78.70)
}


# Title
st.title("🐅 Wildlife Monitoring Patrol Planner")

st.write(
    "Plan an efficient patrol route between wildlife monitoring locations."
)


# Get locations
locations = list(graph.keys())

st.sidebar.header("🚓 Patrol Controls")

start = st.sidebar.selectbox(
    "Starting Location",
    locations
)

required = st.sidebar.multiselect(
    "Monitoring Locations",
    [x for x in locations if x != start]
)

# Blocked trail selection
trails = []

for node in graph:
    for neighbor, distance in graph[node]:
        if (neighbor, node) not in trails:
            trails.append((node, neighbor))


blocked_trail = st.sidebar.selectbox(
    "🚧 Blocked Trail",
    ["None"] + [
        f"{a} → {b}"
        for a, b in trails
    ]
)

# Show all wildlife locations initially
m = folium.Map(
    location=location_coords["Srisailam"],
    zoom_start=13
)

for name, coordinates in location_coords.items():

    folium.Marker(
        coordinates,
        popup=name,
        tooltip=name
    ).add_to(m)

st_folium(
    m,
    width=1000,
    height=500
)



# Plan route
if st.sidebar.button("🚓 Plan Patrol Route"):

    if len(required) == 0:
        st.warning("Please select at least one monitoring location.")

    else:
        # Calculate normal route
        original_route, original_distance = patrol_planner(
            graph, start, required
        )

        # Remove blocked trail
        blocked_graph = remove_blocked_trail(
            graph, blocked_trail
        )

        # Calculate new route
        route, distance = patrol_planner(
            blocked_graph, start, required
        )

        st.session_state["route"] = route
        st.session_state["distance"] = distance
        st.session_state["original_distance"] = original_distance
        st.session_state["blocked_trail"] = blocked_trail


# Reset route (separate button)
if st.sidebar.button("🔄 Reset Route"):
    st.session_state["route"] = None
    st.session_state["distance"] = None
    st.session_state["original_distance"] = None
    st.session_state["blocked_trail"] = "None"
    st.rerun()

# Display route
if st.session_state["route"] is not None:

    route = st.session_state["route"]
    distance = st.session_state["distance"]
    original_distance = st.session_state["original_distance"]
    blocked_trail = st.session_state["blocked_trail"]

    if blocked_trail != "None":

        st.warning(
            f"🚧 Blocked Trail: {blocked_trail}"
        )

        st.info(
            f"🔄 Route recalculated because the trail is blocked."
        )

        extra_distance = distance - original_distance

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🛣️ Original Distance",
                f"{original_distance} km"
            )

        with col2:
            st.metric(
                "🔄 New Distance",
                f"{distance} km"
            )

        with col3:
            st.metric(
                "📈 Extra Distance",
                f"{extra_distance} km"
            )

    st.success("Patrol route generated!")

    if blocked_trail == "None":
        st.success("🟢 All trails are available.")
    else:
        st.warning(
            f"🟠 Patrol route adapted around {blocked_trail}"
        )

    # Route
    st.write("### 🛣️ Patrol Route")

    st.write("### 📋 Patrol Sequence")

    for i, location in enumerate(route, 1):
        st.write(f"**{i}.** 📍 {location}")

    st.write("### 🛣️ Route Segments")

    current_graph = remove_blocked_trail(
        graph,
        blocked_trail
    )

    for i in range(len(route) - 1):

        a = route[i]
        b = route[i + 1]

        for neighbor, weight in current_graph[a]:

            if neighbor == b:

                st.write(
                    f"📍 {a} → {b} : **{weight} km**"
                )

                break

    # Distance
    st.write("### 📏 Total Distance")

    st.write(
        f"{distance} km"
    )

    # Dashboard
    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "📏 Total Distance",
            f"{distance} km"
        )


    with col2:

        st.metric(
            "📍 Locations Visited",
            len(route) - 1
        )


    with col3:

        st.metric(
            "🚓 Starting Point",
            start
        )


    # Create map
    m = folium.Map(
        location=location_coords[start],
        zoom_start=13
    )


    # Add markers
    for location in route:

        folium.Marker(
            location_coords[location],
            popup=location,
            tooltip=location
        ).add_to(m)


    # Draw patrol route
    route_points = [
        location_coords[location]
        for location in route
    ]


    folium.PolyLine(
        route_points,
        weight=5
    ).add_to(m)

    if blocked_trail != "None":

        a, b = blocked_trail.split(" → ")

        folium.PolyLine(
            [
                location_coords[a],
                location_coords[b]
            ],
            weight=6,
            color="red",
            dash_array="10"
        ).add_to(m)

    st.write("### 🗺️ Map Legend")
    st.write("🟦 Solid line = Patrol Route")
    st.write("🟥 Dashed line = Blocked Trail")
   
    # Display map
    st_folium(
        m,
        width=1000,
        height=600
    )

st.divider()

st.header("🧠 Algorithm Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📍 Locations",
        len(graph)
    )

with col2:
    edges = sum(len(x) for x in graph.values()) // 2

    st.metric(
        "🛣️ Trails",
        edges
    )

with col3:
    st.metric(
        "⚡ Algorithm",
        "Dijkstra"
    )


st.subheader("🔹 Dijkstra's Algorithm")

st.write(
    "Finds the shortest path between monitoring locations "
    "using trail distance as the edge weight."
)

st.write("**Time Complexity:** O((V + E) log V)")
st.write("**Space Complexity:** O(V + E)")


st.subheader("🔹 Greedy Patrol Selection")

st.write(
    "Selects the nearest unvisited monitoring location "
    "to determine the next patrol destination."
)

st.write(
    "**Dynamic Rerouting:** Supported 🚧"
)
