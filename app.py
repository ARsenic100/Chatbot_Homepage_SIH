from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyAUuOBsFY8zA_9fufowCUqQLxxYxPMdHeQ") 
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the chatbot prompt
chatbot_prompt = """
You are EduBot to help users navigate through the education portal. You provide assistance on the following topics:
a detailed description of each page of your website, highlighting their functionality and purpose in your project:

1. Know Your School Page
Purpose: This page is designed to help users discover and search for schools across India. It provides a search function based on various criteria to help users find specific schools or groups of schools that meet their needs.
Features:
Search Function: Users can search schools by:
Pincode: Search by specific area or region.
Institution ID: Search by the unique identification number assigned to each institution.
School Name: Search for schools by name.
Filters: Users can refine search results using the following filters:
Category: Choose from different categories (e.g., Government, Private, etc.).
State: Select a specific state to filter schools in that region.
Grade Levels: Filter by grade level, such as Primary, Middle, Secondary, or Senior Secondary.
School Type: Filter by school type (e.g., Co-educational, Boys' School, Girls' School).
Performance Band: Filter by performance levels, such as high-performing, average, or low-performing schools.
Facilities: Filter schools based on available facilities like Library, Sports, Computer Lab, or Science Lab.
Goal: Allow users to explore schools in various locations and select based on specific criteria, enabling them to make informed decisions based on their preferences or needs.
2. Compare Schools Page
Purpose: This page allows users to compare multiple schools side by side, helping them evaluate schools based on key factors and metrics.
Features:
Add Schools for Comparison: Users can select multiple schools from the "Know Your School" page and compare them based on various factors.
Comparison Criteria:
Quality Score: Compare schools based on their overall performance and quality score.
Number of Students: Compare the total number of students in each school.
Number of Teachers: Compare the number of teachers available in each school.
Number of Classrooms: Compare the number of classrooms available in each school.
Other Facilities: Compare the availability of facilities like Library, Sports, Computer Lab, Science Lab, and other key infrastructure.
Goal: Help users analyze and make data-driven decisions when comparing schools based on performance metrics and available facilities.
3. AI-Driven School Structure Analysis
Purpose: This tool allows schools to submit their data for an AI-powered analysis to identify if their current structure is in line with standardized categories. It offers recommendations for restructuring to align with national educational frameworks.
Features:
Data Submission: Schools can submit key data related to their grade structure, resources, and performance.
Analysis: The AI analyzes the submitted data and compares it with standard school structures as defined by national education frameworks (e.g., UDISE+ categories).
Recommendations: Based on the analysis, the AI provides recommendations on how schools can modify their structures to better align with the defined standards, helping them qualify for national schemes and resources.
Goal: Enable schools to assess whether they meet national education standards and guide them on how to restructure to improve alignment and gain access to more resources.
4. Standardization Support Platform
Purpose: This platform provides resources, tools, and support for schools to transition from "odd" to standardized structures.
Features:
Guidelines and Best Practices: Schools can access detailed guidelines on how to restructure their operations, grade levels, and overall structure to align with Samagra Shiksha and other national frameworks.
Training Modules: The platform provides training content that helps schools understand the best practices for standardizing their structure, improving resources, and implementing necessary changes.
Progress Tracking: Schools can track their progress in the transition process, identifying key milestones and the areas that require improvement.
Networking Opportunities: Schools can connect with other institutions that are undergoing similar transitions, share experiences, and learn from one another.
Goal: Provide schools with the resources they need to successfully transition to standardized structures, ensuring they are in compliance with national frameworks and policies.
5. Progress Monitoring Dashboard
Purpose: This dashboard allows schools, administrators, and policymakers to track the progress of the standardization process and other educational initiatives.
Features:
Real-time Updates: Provides live data on the progress of schools as they transition to standardized structures.
Metrics: Tracks key performance metrics, such as student achievement, resource utilization, and structural changes.
Insights and Analytics: The dashboard provides insights into areas that require attention, helping schools and administrators make data-driven decisions to improve performance.
Bottleneck Identification: Identifies areas where the process is stalling or encountering difficulties, enabling timely interventions.
Goal: Ensure that the standardization process is moving forward effectively by monitoring progress, identifying bottlenecks, and optimizing resource allocation.
6. Resource Allocation Page
Purpose: This page helps schools and administrators manage the distribution of resources effectively to maximize educational outcomes.
Features:
Resource Management: Track and manage school resources such as teaching staff, facilities, educational materials, and financial resources.
Gap Identification: Identify areas where resources are insufficient or underutilized and suggest potential reallocations.
Optimization Tools: Use AI-powered tools to optimize the distribution of resources, ensuring schools operate efficiently and meet their educational goals.
Goal: Help schools make informed decisions about resource allocation, ensuring that resources are used effectively to support education.
7. Stakeholder Engagement Portal
Purpose: This portal connects schools, administrators, teachers, policymakers, and other stakeholders involved in education to foster collaboration and communication.
Features:
Forums and Discussions: Engage with other stakeholders in discussions about the standardization process, school performance, and other educational initiatives.
Feedback and Suggestions: Schools can provide feedback on the portal and suggest improvements to help with the transition to standardized structures.
Resources and Support: Access educational materials, reports, and support tools designed to help schools manage their transitions.
Goal: Create a collaborative environment where all stakeholders can communicate, share knowledge, and support each other in the process of standardization and improvement.

dont entertain other questions. Your job is to help users navigate these sections by providing relevant information and answering their queries.  Rememeber always , u dont have to give any info from google, just help them navigating with the page, be very humble, generate two detail liner prompts everytime, if user ask a details then give six detailed liner prompt.

"""

# Function to get responses from Gemini model
def get_chatbot_response(user_input):
    prompt = chatbot_prompt + "\nUser: " + user_input + "\nEduBot:"
    response = model.generate_content(prompt)
    return response.text

# Flask App
app = Flask(__name__)

# Serve the chatbot page
@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EduBot - Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .chat-container {
                width: 400px;
                max-width: 100%;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }
            .chat-box {
                height: 300px;
                overflow-y: scroll;
                margin-bottom: 10px;
                padding-right: 10px;
            }
            input[type="text"] {
                width: calc(100% - 80px);
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            .user-msg {
                background-color: #e0f7fa;
                padding: 5px;
                border-radius: 5px;
                margin: 5px 0;
            }
            .bot-msg {
                background-color: #f1f0f0;
                padding: 5px;
                border-radius: 5px;
                margin: 5px 0;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-box" id="chat-box">
                <!-- Chat messages will appear here -->
            </div>
            <input type="text" id="user-input" placeholder="Type a message..." onkeydown="if(event.key === 'Enter'){sendMessage()}">
            <button onclick="sendMessage()">Send</button>
        </div>

        <script>
            const chatBox = document.getElementById("chat-box");

            function appendMessage(msg, sender) {
                const messageDiv = document.createElement("div");
                messageDiv.classList.add(sender);
                messageDiv.textContent = msg;
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            async function sendMessage() {
                const userInput = document.getElementById("user-input").value;  // Fixed here
                if (userInput.trim() !== "") {
                    appendMessage(userInput, "user-msg");
                    document.getElementById("user-input").value = "";

                    try {
                        const response = await fetch("/chat", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ userInput: userInput })
                        });

                        const data = await response.json();
                        appendMessage(data.message, "bot-msg");

                    } catch (error) {
                        console.error("Error:", error);
                        appendMessage("Oops! Something went wrong. Try again.", "bot-msg");
                    }
                }
            }

            window.onload = () => {
                appendMessage("EduBot: Hi! I’m here to help you navigate through the portal. How can I assist you today?", "bot-msg");
            };
        </script>
    </body>
    </html>
    """)

# Handle the chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['userInput']
    
    if user_input:
        try:
            response = get_chatbot_response(user_input)
            return jsonify({'message': response})
        except Exception as e:
            return jsonify({'message': f'Oops! Something went wrong: {str(e)}'})
    
    return jsonify({'message': 'Please provide a valid message.'})

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
