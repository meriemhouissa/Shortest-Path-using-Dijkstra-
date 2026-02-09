import pandas as pd
import numpy as np
import heapq

# -------------------------
# 1. Load CSV
# -------------------------
file_path = r"C:\Users\salma\Documents\network analysis project\Fillout New form ezuaT results (2).csv"
df = pd.read_csv(file_path)
df = df[df['What is your current academic level?'].notna()]

# -------------------------
# 2. Map activities to columns
# -------------------------
activities = {
    'Free_Courses': {'difficulty': 'How difficult is doing skill-building activities (courses, Youtube, certifications) for you personally?',
                     'value': 'How valuable do you think skill-building is for getting an internship?'},
    'Workshops': {'difficulty': 'How difficult is attending workshops for you personally?',
                  'value': 'How valuable do you think attending workshops is for getting an internship?'},
    'Hackathons_Events': {'difficulty': 'How difficult is participating in hackathons for you personally?',
                          'value': 'How valuable do you think hackathons are for getting an internship?'},
    'Clubs_Orgs': {'difficulty': 'How difficult is joining a student club / association for you personally?',
                   'value': 'How valuable do you think company visits are for getting an internship?'},  
    'LinkedIn_Optimized': {'difficulty': 'How difficult is improving your LinkedIn profile for you personally?',
                           'value': 'How valuable do you think optimizing LinkedIn is for getting an internship?'},
    'CV_Ready': {'difficulty': 'How difficult is updating your CV for you personally?',
                 'value': 'How valuable do you think updating your CV is for getting an internship?'},
    'Career_Fair': {'difficulty': 'How difficult is attending career fairs for you personally?',
                    'value': 'How valuable do you think career fairs are for getting an internship?'},
    'Alumni_Network': {'difficulty': 'How difficult is talking to alumni for you personally?',
                       'value': 'How valuable do you think talking to alumni is for getting an internship?'},
    'Professors': {'difficulty': 'How difficult is contacting a professor for you personally?',
                   'value': 'How valuable do you think contacting HR / networking is for getting an internship?'},  # proxy
    'Job_Platforms': {'difficulty': 'How difficult is searching in job platforms for you personally?',
                      'value': 'How valuable do you think searching in job platforms is for getting an internship?'},
    'Direct_Apply': {'difficulty': 'How difficult is sending spontaneous applications for you personally?',
                     'value': 'How valuable do you think spontaneous applications are for getting an internship?'},
    'Company_Contact': {'difficulty': 'How difficult is contacting HR or employees on LinkedIn for you personally?',
                        'value': 'How valuable do you think contacting HR / networking is for getting an internship?'},
    'Interview': {'difficulty': 'How difficult is preparing for internship interviews for you personally?',
                  'value': 6}  # fixed high value
}

# -------------------------
# 3. Personality types
# -------------------------
personalities = ['Shy', 'Neutral', 'Social']

# -------------------------
# 4. Compute simplified weights (difficulty / value)
# -------------------------
personality_weights = {}

for p in personalities:
    df_p = df[df['How would you describe your personality in social situations?'] == p]
    if df_p.empty: 
        continue
    weights = {}
    for act, cols in activities.items():
        # Difficulty
        if cols['difficulty'] in df_p.columns:
            diff = pd.to_numeric(df_p[cols['difficulty']], errors='coerce').dropna()
            avg_diff = diff.mean() if not diff.empty else 3.0
        else:
            avg_diff = 3.0
        # Value
        if isinstance(cols['value'], int):
            avg_val = cols['value']
        elif cols['value'] in df_p.columns:
            val = pd.to_numeric(df_p[cols['value']], errors='coerce').dropna()
            avg_val = val.mean() if not val.empty else 4.0
        else:
            avg_val = 4.0
        # Weight: lower is better
        weights[act] = avg_diff / avg_val
    personality_weights[p] = weights

print(f"Analyzed {len(df)} survey responses")

# -------------------------
# 5. DIJKSTRA ALGORITHM IMPLEMENTATION
# -------------------------
class InternshipGraph:
    def __init__(self):
        self.edges = {}
    
    def add_node(self, node):
        if node not in self.edges:
            self.edges[node] = {}
    
    def add_edge(self, from_node, to_node, weight):
        # ADD THIS: Ensure both nodes exist in the graph
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node][to_node] = weight
    
    def dijkstra(self, start, end):
        # Initialize distances
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

# -------------------------
# 6. BUILD GRAPH AND FIND OPTIMAL PATHS
# -------------------------
print("\n" + "="*80)
print("DIJKSTRA OPTIMAL PATHS FOR INTERNSHIP PREPARATION")
print("="*80)

for personality in personality_weights.keys():
    graph = InternshipGraph()
    weights = personality_weights[personality]
    
    # BUILD THE GRAPH ACCORDING TO YOUR STRUCTURE
    
    # Student → Learning Activities
    graph.add_edge("Student", "Free_Courses", weights['Free_Courses'])
    graph.add_edge("Student", "Workshops", weights['Workshops'])
    graph.add_edge("Student", "Hackathons_Events", weights['Hackathons_Events'])
    graph.add_edge("Student", "Clubs_Orgs", weights['Clubs_Orgs'])
    
    # Learning Activities → Develop_Skills
    graph.add_edge("Free_Courses", "Develop_Skills", weights['Free_Courses'] * 0.5)  # Reduced weight for progression
    graph.add_edge("Workshops", "Develop_Skills", weights['Workshops'] * 0.5)
    graph.add_edge("Hackathons_Events", "Develop_Skills", weights['Hackathons_Events'] * 0.5)
    graph.add_edge("Clubs_Orgs", "Develop_Skills", weights['Clubs_Orgs'] * 0.5)
    
    # Develop_Skills → Profile Building
    graph.add_edge("Develop_Skills", "LinkedIn_Optimized", weights['LinkedIn_Optimized'])
    graph.add_edge("Develop_Skills", "CV_Ready", weights['CV_Ready'])
    
    # Profile Building → Application Methods
    graph.add_edge("LinkedIn_Optimized", "Career_Fair", weights['Career_Fair'])
    graph.add_edge("LinkedIn_Optimized", "Alumni_Network", weights['Alumni_Network'])
    graph.add_edge("LinkedIn_Optimized", "Professors", weights['Professors'])
    graph.add_edge("LinkedIn_Optimized", "Job_Platforms", weights['Job_Platforms'])
    graph.add_edge("LinkedIn_Optimized", "Direct_Apply", weights['Direct_Apply'])
    graph.add_edge("LinkedIn_Optimized", "Company_Contact", weights['Company_Contact'])
    
    graph.add_edge("CV_Ready", "Career_Fair", weights['Career_Fair'])
    graph.add_edge("CV_Ready", "Alumni_Network", weights['Alumni_Network'])
    graph.add_edge("CV_Ready", "Professors", weights['Professors'])
    graph.add_edge("CV_Ready", "Job_Platforms", weights['Job_Platforms'])
    graph.add_edge("CV_Ready", "Direct_Apply", weights['Direct_Apply'])
    graph.add_edge("CV_Ready", "Company_Contact", weights['Company_Contact'])
    
    # Application Methods → Interview
    graph.add_edge("Career_Fair", "Interview", weights['Interview'])
    graph.add_edge("Alumni_Network", "Interview", weights['Interview'])
    graph.add_edge("Professors", "Interview", weights['Interview'])
    graph.add_edge("Job_Platforms", "Interview", weights['Interview'])
    graph.add_edge("Direct_Apply", "Interview", weights['Interview'])
    graph.add_edge("Company_Contact", "Interview", weights['Interview'])
    
    # Interview → Internship_Offer
    graph.add_edge("Interview", "Internship_Offer", 0.1)  # Very low weight for final step
    
    # FIND OPTIMAL PATH
    path, total_cost = graph.dijkstra("Student", "Internship_Offer")
    
    print(f" {personality.upper()} STUDENTS:")
    print(f"Optimal Path: {' → '.join(path)}")
    print(f"Total Cost: {total_cost:.3f}")
    
    # Show key decisions with weights
    if len(path) > 2:
        learning_choice = path[1]
        application_choice = path[5] if len(path) > 5 else path[-2]
        
        print(f"Key Decisions:")
        print(f"  Learning Method: {learning_choice} (weight: {weights.get(learning_choice, 'N/A'):.3f})")
        print(f"  Application Method: {application_choice} (weight: {weights.get(application_choice, 'N/A'):.3f})")

# -------------------------
# 7. SHOW ALL WEIGHTS FOR REFERENCE
# -------------------------
print("\n" + "="*80)
print("DETAILED WEIGHTS ANALYSIS (Difficulty / Value)")
print("="*80)

for personality, weights in personality_weights.items():
    print(f"\n{personality.upper()} PERSONALITY:")
    
    print("Learning Methods:")
    learning_methods = ['Free_Courses', 'Workshops', 'Hackathons_Events', 'Clubs_Orgs']
    for method in learning_methods:
        print(f"  {method:18} → {weights[method]:.3f}")
    
    print("\nApplication Methods:")
    app_methods = ['Career_Fair', 'Alumni_Network', 'Professors', 'Job_Platforms', 'Direct_Apply', 'Company_Contact']
    for method in app_methods:
        print(f"  {method:18} → {weights[method]:.3f}")
    
    print(f"\nProfile Building:")
    print(f"  LinkedIn_Optimized   → {weights['LinkedIn_Optimized']:.3f}")
    print(f"  CV_Ready            → {weights['CV_Ready']:.3f}")
    print(f"  Interview Prep      → {weights['Interview']:.3f}")

# -------------------------
# 8. QUICK SUMMARY
# -------------------------
print("\n" + "="*80)
print("QUICK RECOMMENDATIONS")
print("="*80)

for personality in personality_weights.keys():
    weights = personality_weights[personality]
    
    # Find best learning method (lowest weight)
    learning_methods = ['Free_Courses', 'Workshops', 'Hackathons_Events', 'Clubs_Orgs']
    best_learn = min(learning_methods, key=lambda x: weights[x])
    
    # Find best application method (lowest weight)
    app_methods = ['Career_Fair', 'Alumni_Network', 'Professors', 'Job_Platforms', 'Direct_Apply', 'Company_Contact']
    best_app = min(app_methods, key=lambda x: weights[x])
    
    print(f"\n{personality.upper()} Students:")
    print(f"  START WITH: {best_learn}")
    print(f"  APPLY VIA:  {best_app}")
    print(f"  STRATEGY:   Focus on what feels easiest and most valuable for you")