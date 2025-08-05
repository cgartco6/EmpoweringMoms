import os
import json
import datetime
from utils import get_config, generate_ai_content, save_to_database

def generate_new_course():
    """Generate a new course every two weeks"""
    config = get_config()
    existing_courses = config['courses']
    
    # Analyze popular topics
    prompt = "Based on current trends, suggest a new online course topic for South African moms wanting financial freedom"
    topic = generate_ai_content(prompt, max_tokens=100)
    
    # Generate course content
    prompt = f"Create comprehensive course content for: {topic}. Include modules, lessons, and learning objectives"
    content = generate_ai_content(prompt, max_tokens=2000)
    
    # Set pricing based on complexity
    word_count = len(content.split())
    price = min(2000, max(200, int(word_count * 0.05)))
    
    # Create course structure
    course = {
        "id": f"course-{datetime.datetime.now().strftime('%Y%m%d')}",
        "title": topic,
        "description": content[:500] + "...",
        "price": price,
        "modules": json.loads(generate_ai_content(f"Create 5 module titles for course: {topic}")),
        "created_at": datetime.datetime.now().isoformat()
    }
    
    # Save to database and config
    save_to_database("courses", course)
    existing_courses[course['id']] = course
    update_config({"courses": existing_courses})
    
    print(f"Created new course: {topic} (R{price})")
    return course

if __name__ == "__main__":
    generate_new_course()
