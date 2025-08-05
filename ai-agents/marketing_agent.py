import os
import random
import requests
import schedule
import time
from utils import get_config, generate_ai_content, post_to_social_media

def create_social_content():
    """Generate marketing content for social media"""
    config = get_config()
    courses = config['courses']
    
    # Generate content based on current promotions
    content_types = [
        "motivational quote for moms",
        "course feature highlight",
        "student success story",
        "financial tip for South African mothers"
    ]
    
    topic = random.choice(content_types)
    prompt = f"Create engaging social media content about {topic} for South African moms"
    text = generate_ai_content(prompt, max_tokens=280)
    
    # Generate image prompt
    image_prompt = f"Professional image showing: {text[:100]}"
    image_url = generate_ai_content(image_prompt, content_type="image")
    
    return {
        "text": text,
        "image": image_url,
        "hashtags": "#EmpoweringMoms #SAmoms #FinancialFreedom"
    }

def run_social_campaign():
    """Run full social media marketing campaign"""
    content = create_social_content()
    
    # Post to all platforms
    platforms = ["facebook", "instagram", "tiktok", "whatsapp"]
    for platform in platforms:
        post_to_social_media(platform, content)
    
    print(f"Posted marketing content to {len(platforms)} platforms")

def schedule_marketing():
    """Schedule marketing posts throughout the day"""
    schedule.every().day.at("08:00").do(run_social_campaign)
    schedule.every().day.at("12:00").do(run_social_campaign)
    schedule.every().day.at("17:00").do(run_social_campaign)
    schedule.every().day.at("20:00").do(run_social_campaign)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_marketing()
