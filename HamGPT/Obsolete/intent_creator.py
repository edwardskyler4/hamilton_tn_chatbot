import json

# Create a basic structure for intents including departments as tags
departments = [
    "Accounting", "UT/TSU Extension - Hamilton County", "Alternative Sentencing", "Assessor of Property",
    "Building Inspection Department", "Chester Frost Park", "Chancery Court", "CHCRPA",
    "Chief of Staff", "Circuit Court Clerk", "Circuit Court Judges", "Clerk And Master",
    "Community and Economic Development Department", "County Attorney", "County Auditor's Office",
    "County Clerk", "County Commission", "County Mayor", "Criminal Court Clerk",
    "Criminal Court Clerk Expungement Center", "Criminal Court Clerk Payment Center",
    "Criminal Court Judges", "Development Department", "Development Services", "District Attorney General",
    "Drug Recovery Court", "Education Department", "Election Commission", "Emergency Management and Homeland Security",
    "Emergency Medical Services (EMS)", "Engineering Department", "Enterprise South Nature Park",
    "Equal Employment Opportunity (EEO)", "Facilities Maintenance Department", "Finance Division",
    "Financial Management", "General Services Division", "General Sessions Criminal Clerk",
    "Geospatial Technology", "Ground Water", "Health Department", "Highway Department",
    "Human Resources Division", "Information Technology Department (IT)", "Judicial Commission Magistrates",
    "Juvenile Court", "Juvenile Court Clerk", "Child Support Division", "Local Emergency Planning Committee (LEPC)",
    "Magistrates - Judicial Commission", "Mayor", "Medical Examiner", "Mental Health Court",
    "Parks And Recreation", "Procurement And Fleet Management Department", "Public Defender",
    "Public Works Division", "Read 20 Program", "Real Property Office", "Records Management",
    "Recycling Department", "Register of Deeds", "Risk Management Office", "Sessions Civil Court",
    "Sessions Court Judges Office", "Sheriff", "Soil and Water Conservation District",
    "Support Services", "Telecommunication Department", "Title VI Department", "Tennessee Riverpark",
    "Trustee", "Veteran Services Office", "Water Quality Department", "Water And Wastewater Treatment Authority (WWTA)"
]

intents = []

for dept in departments:
    intents.append({
        "tag": dept.lower().replace(" ", "_"),
        "example_inputs": [f"How do I contact {dept}?", f"What does the {dept} do?", f"{dept} hours"],
        "possible_responses": [f"You can contact {dept} at...", f"The {dept} is responsible for...", f"Here are the office hours for {dept}..."]
    })

# Save to a JSON file
file_path = "/mnt/data/county_chatbot_intents.json"
with open(file_path, "w") as file:
    json.dump(intents, file, indent=4)

file_path