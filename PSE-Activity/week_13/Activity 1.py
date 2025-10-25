import os
from openai import OpenAI


def instructor_chatbot():
    client = OpenAI(api_key="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")

    """Command-line AI Itinerary Chatbot."""
    print("Welcome to AI Itinerary recommender! Answer a few questions to get personalized itenary advice.\n")
    
    days = input("How many (days): ")
    location = input("Where is the destination (city name): ")
    age = input("Enter your age: ")
    # fitness_goal = input("What is your fitness goal? (e.g., lose weight, build muscle, endurance, etc.): ")
    
    # Construct prompt
    prompt = f"""
    You are a professional trouist recommender. Provide an itinerary recommendation based on user data.
    
    User Details:
    - days: {days} days
    - destination: {location} city
    - Age: {age} years
    
    Based on your personal information, 
    Then, give a structured itinerary with a name of the place, address and short description for each day seperatly in order with maximom three activities in a day.
    """
    
    try:
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a professional itinerary recommender."},
                      {"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.8,
        stream=True
        )

        print("\n My Name is Chris as AI Itinerary expert:")
        for token in response:
            if hasattr(token, 'choices'):
                print(token.choices[0].delta.content, end='', flush=True)
        
    except Exception as e:
        print("Error communicating with Meta Llama API:", e)

if __name__ == "__main__":
    instructor_chatbot()