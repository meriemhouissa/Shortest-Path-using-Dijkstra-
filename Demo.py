import streamlit as st
import pandas as pd
import numpy as np
import heapq

# Set page configuration
st.set_page_config(
    page_title="Internship Pathfinder",
    
    layout="wide"
)

# Title
st.title(" Internship Pathfinder")
st.write("Find your optimal path to an internship based on your personality!")

# Sidebar
with st.sidebar:
    st.header("Personal Profile")
    personality = st.selectbox(
        "How would you describe your personality in social situations?",
        ["Shy", "Neutral", "Social"],
        index=1
    )
    
    st.subheader("Your Preferences")
    learning_pref = st.multiselect(
        "Preferred learning methods (optional):",
        ["Free Courses", "Workshops", "Hackathons", "Clubs/Organizations"]
    )
    
    network_pref = st.select_slider(
        "Comfort level with networking:",
        options=["Very Uncomfortable", "Uncomfortable", "Neutral", "Comfortable", "Very Comfortable"],
        value="Neutral"
    )
    
    time_constraint = st.slider("Time available (hours per week):", 1, 20, 10)
    
    analyze_button = st.button(" Find My Optimal Path", type="primary")

# Data loading function
def load_data():
    try:
        file_path = r"C:\Users\salma\Documents\network analysis project\Fillout New form ezuaT results (2).csv"
        df = pd.read_csv(file_path)
        df = df[df['What is your current academic level?'].notna()]
        return df
    except:
        st.warning("Using sample data - original file not found")
        return pd.DataFrame()

# Graph class
class InternshipGraph:
    def __init__(self):
        self.edges = {}
    
    def add_node(self, node):
        if node not in self.edges:
            self.edges[node] = {}
    
    def add_edge(self, from_node, to_node, weight):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node][to_node] = weight
    
    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.edges}
        distances[start] = 0
        previous = {}
        pq = [(0, start)]
        
        while pq:
            current_dist, current_node = heapq.heappop(pq)
            
            if current_node == end:
                break
                
            if current_dist > distances[current_node]:
                continue
                
            if current_node in self.edges:
                for neighbor, weight in self.edges[current_node].items():
                    distance = current_dist + weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous[neighbor] = current_node
                        heapq.heappush(pq, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = end
        while current != start:
            path.append(current)
            current = previous.get(current)
            if current is None:
                return [], float('inf')
        path.append(start)
        path.reverse()
        return path, distances[end]

# Sample weights (replace with your actual data loading)
def get_sample_weights(personality):
    if personality == "Shy":
        return {
            'Free_Courses': 0.8, 'Workshops': 1.2, 'Hackathons_Events': 1.5, 'Clubs_Orgs': 1.4,
            'LinkedIn_Optimized': 0.9, 'CV_Ready': 0.7, 'Career_Fair': 1.3,
            'Alumni_Network': 1.6, 'Professors': 1.4, 'Job_Platforms': 0.9,
            'Direct_Apply': 1.1, 'Company_Contact': 1.5, 'Interview': 1.0
        }
    elif personality == "Neutral":
        return {
            'Free_Courses': 1.0, 'Workshops': 1.0, 'Hackathons_Events': 1.2, 'Clubs_Orgs': 1.1,
            'LinkedIn_Optimized': 0.8, 'CV_Ready': 0.8, 'Career_Fair': 1.0,
            'Alumni_Network': 1.2, 'Professors': 1.1, 'Job_Platforms': 0.9,
            'Direct_Apply': 1.0, 'Company_Contact': 1.2, 'Interview': 0.9
        }
    else:  # Social
        return {
            'Free_Courses': 1.2, 'Workshops': 0.9, 'Hackathons_Events': 0.8, 'Clubs_Orgs': 0.7,
            'LinkedIn_Optimized': 0.7, 'CV_Ready': 0.8, 'Career_Fair': 0.9,
            'Alumni_Network': 0.8, 'Professors': 0.9, 'Job_Platforms': 1.0,
            'Direct_Apply': 1.1, 'Company_Contact': 0.8, 'Interview': 0.8
        }

def build_graph(weights):
    graph = InternshipGraph()
    
    # Student → Learning Activities
    graph.add_edge("Student", "Free_Courses", weights['Free_Courses'])
    graph.add_edge("Student", "Workshops", weights['Workshops'])
    graph.add_edge("Student", "Hackathons_Events", weights['Hackathons_Events'])
    graph.add_edge("Student", "Clubs_Orgs", weights['Clubs_Orgs'])
    
    # Learning Activities → Develop_Skills
    graph.add_edge("Free_Courses", "Develop_Skills", weights['Free_Courses'] * 0.5)
    graph.add_edge("Workshops", "Develop_Skills", weights['Workshops'] * 0.5)
    graph.add_edge("Hackathons_Events", "Develop_Skills", weights['Hackathons_Events'] * 0.5)
    graph.add_edge("Clubs_Orgs", "Develop_Skills", weights['Clubs_Orgs'] * 0.5)
    
    # Develop_Skills → Profile Building
    graph.add_edge("Develop_Skills", "LinkedIn_Optimized", weights['LinkedIn_Optimized'])
    graph.add_edge("Develop_Skills", "CV_Ready", weights['CV_Ready'])
    
    # Profile Building → Application Methods
    app_methods = ['Career_Fair', 'Alumni_Network', 'Professors', 'Job_Platforms', 'Direct_Apply', 'Company_Contact']
    for method in app_methods:
        graph.add_edge("LinkedIn_Optimized", method, weights[method])
        graph.add_edge("CV_Ready", method, weights[method])
    
    # Application Methods → Interview
    for method in app_methods:
        graph.add_edge(method, "Interview", weights['Interview'])
    
    # Interview → Internship_Offer
    graph.add_edge("Interview", "Internship_Offer", 0.1)
    
    return graph

# Main app logic
if analyze_button:
    # Get weights for selected personality
    weights = get_sample_weights(personality)
    
    # Build graph and find path
    graph = build_graph(weights)
    path, total_cost = graph.dijkstra("Student", "Internship_Offer")
    
    st.subheader(f" Your {personality} Personality Path")
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Personality", personality)
    with col2:
        st.metric("Path Steps", len(path))
    with col3:
        st.metric("Total Cost", f"{total_cost:.2f}")
    with col4:
        st.metric("Time Available", f"{time_constraint} hrs/week")
    
    
    st.subheader(" Optimal Path")
    path_text = " → ".join(path)
    st.success(path_text)
    
    # Step-by-step guide
    st.subheader(" Step-by-Step Guide")
    for i, step in enumerate(path):
        st.write(f"**Step {i+1}:** {step}")
    
    # Recommendations
    st.subheader(" Personalized Recommendations")
    
    with st.expander("Learning Method"):
        if path[1] == "Free_Courses":
            st.write(" **Free online courses** are perfect for self-paced learning")
        elif path[1] == "Workshops":
            st.write(" **Workshops** provide structured, hands-on experience")
        elif path[1] == "Hackathons_Events":
            st.write(" **Hackathons** help build practical skills quickly")
        else:
            st.write(" **Clubs/Organizations** offer networking and leadership opportunities")
    
    with st.expander("Application Strategy"):
        app_step = path[4] if len(path) > 4 else path[-2]
        st.write(f"✅ Your optimal application method is **{app_step.replace('_', ' ')}**")
        
        if "Uncomfortable" in network_pref and any(x in app_step for x in ['Alumni', 'Contact', 'Fair']):
            st.write(" **Tip:** Start with small networking goals to build confidence")
    
    # Activity analysis
    st.subheader(" Activity Difficulty Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Learning Methods:**")
        st.write(f"- Free Courses: {weights['Free_Courses']:.2f}")
        st.write(f"- Workshops: {weights['Workshops']:.2f}")
        st.write(f"- Hackathons: {weights['Hackathons_Events']:.2f}")
        st.write(f"- Clubs/Orgs: {weights['Clubs_Orgs']:.2f}")
    
    with col2:
        st.write("**Application Methods:**")
        st.write(f"- Job Platforms: {weights['Job_Platforms']:.2f}")
        st.write(f"- Career Fair: {weights['Career_Fair']:.2f}")
        st.write(f"- Alumni Network: {weights['Alumni_Network']:.2f}")
        st.write(f"- Direct Apply: {weights['Direct_Apply']:.2f}")

else:
    # Initial instructions
    st.subheader(" How to Use This Tool")
    st.write("1. **Select your personality type** from the sidebar")
    st.write("2. **Adjust your preferences** (optional)")
    st.write("3. **Click 'Find My Optimal Path'** to generate recommendations")
    
    st.write("---")
    
    st.subheader(" Sample Paths")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Shy Personality**")
        st.code("""Student → Free Courses → 
Develop Skills → CV Ready → 
Job Platforms → Interview → 
Internship Offer""")
    
    with col2:
        st.write("**Neutral Personality**")
        st.code("""Student → Workshops → 
Develop Skills → LinkedIn → 
Career Fair → Interview → 
Internship Offer""")
    
    with col3:
        st.write("**Social Personality**")
        st.code("""Student → Clubs/Orgs → 
Develop Skills → CV Ready → 
Alumni Network → Interview → 
Internship Offer""")


st.write("---")
st.caption("Internship Pathfinder • Powered by Dijkstra's Algorithm")