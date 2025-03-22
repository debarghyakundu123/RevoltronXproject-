import requests
import webbrowser
import streamlit as st
from groq import Groq

# Initialize Groq API
client = Groq(api_key="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")

# Function to generate startup insights (excluding UI/UX design)
def generate_insights(idea, industry, audience):
    prompt = f"""
    Generate a detailed startup plan for:
    - Idea: {idea}
    - Industry: {industry}
    - Target Audience: {audience}
    
    Include the following:
    📌 Overview of the idea
    🎨 Color Palette Suggestions (based on industry)
    🔍 Target Audience Analysis
    📊 Competitor Research
    💡 Pain Points & Required Features
    💰 Funding Sources & Contacts
    🔥 Industry Trends
    🛠 DBMS Schema for backend
    🏦 Investor Details (Leave space for it)
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        stream=False,
    )
    return response.choices[0].message.content

# Function to generate image (UI/UX Design)
def generate_image(description):
    url = "https://chatgpt-vision1.p.rapidapi.com/texttoimage3"
    payload = {
        "text": description,
        "width": 512,
        "height": 512,
        "steps": 1
    }

    headers = {
        "x-rapidapi-key": "24d3c839bemsh93106af2d6d217ep1aa8dejsn9840d252c80b",
        "x-rapidapi-host": "chatgpt-vision1.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    try:
        data = response.json()
        
        if "generated_image" in data:
            image_url = data["generated_image"]
            print(f"Generated Image URL: {image_url}")
            
            # Open Image in Browser Automatically
            webbrowser.open(image_url)
            return image_url
        else:
            print("Image generation failed. Response:", data)
            return None
    except requests.exceptions.JSONDecodeError:
        print("Invalid JSON response. Raw response:", response.text)
        return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

# Streamlit App
def main():
    st.title("Startup Idea Insights Generator")

    # Input fields for user to fill out
    idea = st.text_input("Startup Idea")
    industry = st.text_input("Industry")
    audience = st.text_input("Target Audience")

    if st.button("Generate Insights"):
        if idea and industry and audience:
            # Generate startup insights
            insights = generate_insights(idea, industry, audience)
            st.subheader("Startup Insights:")
            st.write(insights)

            # Create a description based on user inputs for UI/UX design
            ui_description = f"A startup app for {idea} in the {industry} industry, targeting {audience}. A user interface design concept."

            # Call the function to generate the UI/UX design image based on the description
            image_url = generate_image(ui_description)

            # Display the generated image
            if image_url:
                st.image(image_url, caption="Generated UI/UX Design", use_column_width=True)
        else:
            st.error("Please fill in all fields before submitting.")

if __name__ == "__main__":
    main()
