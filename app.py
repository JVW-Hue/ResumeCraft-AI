from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)

# AI Resume Templates and Data
JOB_KEYWORDS = {
    'software': ['JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'Git', 'AWS', 'Docker'],
    'marketing': ['SEO', 'Google Analytics', 'Social Media', 'Content Marketing', 'PPC', 'Email Marketing'],
    'sales': ['CRM', 'Lead Generation', 'Negotiation', 'Customer Relations', 'Pipeline Management'],
    'design': ['Photoshop', 'Figma', 'UI/UX', 'Adobe Creative Suite', 'Prototyping', 'User Research'],
    'finance': ['Excel', 'Financial Analysis', 'Budgeting', 'Risk Management', 'QuickBooks', 'SAP'],
    'project': ['Agile', 'Scrum', 'JIRA', 'Risk Management', 'Stakeholder Management', 'PMP']
}

ACHIEVEMENT_TEMPLATES = {
    'entry': [
        'Completed {} training program with distinction',
        'Contributed to {} project that improved efficiency by {}%',
        'Collaborated with team of {} to deliver {} on schedule',
        'Gained hands-on experience in {} through internship program'
    ],
    'mid': [
        'Led {} initiative that increased revenue by {}%',
        'Managed team of {} professionals across {} projects',
        'Implemented {} solution reducing costs by ${}K annually',
        'Improved {} process efficiency by {}% through optimization'
    ],
    'senior': [
        'Spearheaded {} transformation saving ${}M annually',
        'Built and led high-performing team of {} professionals',
        'Delivered {} projects worth ${}M+ under budget and on time',
        'Established {} best practices adopted company-wide'
    ],
    'executive': [
        'Orchestrated {} strategy resulting in {}% market share growth',
        'Led organizational transformation of {} employees across {} locations',
        'Secured ${}M+ in funding through strategic partnerships',
        'Drove {}% revenue growth over {} years through innovation'
    ]
}

def generate_ai_summary(job_title, experience_level, skills):
    """Generate dynamic AI-powered professional summary"""
    job_lower = job_title.lower() if job_title else 'professional'
    
    # Determine industry based on job title
    industry_keywords = []
    for industry, keywords in JOB_KEYWORDS.items():
        if industry in job_lower:
            industry_keywords = keywords[:4]
            break
    
    if not industry_keywords and skills:
        skill_list = [s.strip() for s in skills.split(',')[:4]]
        industry_keywords = skill_list
    
    summaries = {
        'entry': f"Motivated {job_title or 'professional'} with strong foundation in {', '.join(industry_keywords[:3]) if industry_keywords else 'relevant technologies'}. Recent graduate eager to apply academic knowledge and contribute to innovative projects. Quick learner with excellent problem-solving abilities and passion for continuous improvement.",
        
        'mid': f"Results-driven {job_title or 'professional'} with 4+ years of experience in {', '.join(industry_keywords[:3]) if industry_keywords else 'key technologies'}. Proven track record of delivering high-quality solutions and collaborating effectively with cross-functional teams. Seeking to leverage expertise in {industry_keywords[0] if industry_keywords else 'technology'} to drive innovation and business growth.",
        
        'senior': f"Accomplished {job_title or 'professional'} with 8+ years of experience leading teams and driving strategic initiatives. Deep expertise in {', '.join(industry_keywords[:4]) if industry_keywords else 'enterprise solutions'} with proven ability to mentor junior staff and deliver complex projects. Strong track record of improving efficiency and driving measurable business results.",
        
        'executive': f"Visionary {job_title or 'executive'} with 15+ years of experience in strategic leadership and organizational transformation. Expert in {', '.join(industry_keywords[:3]) if industry_keywords else 'business strategy'} with proven ability to scale teams, drive innovation, and deliver exceptional results in competitive markets."
    }
    
    return summaries.get(experience_level, summaries['mid'])

def generate_ai_achievements(experience_level, job_title):
    """Generate realistic achievements based on experience level"""
    templates = ACHIEVEMENT_TEMPLATES.get(experience_level, ACHIEVEMENT_TEMPLATES['mid'])
    achievements = []
    
    for template in templates[:3]:
        if '{}' in template:
            if experience_level == 'entry':
                achievement = template.format(
                    random.choice(['intensive', '6-month', 'comprehensive']),
                    random.choice([15, 20, 25]),
                    random.choice([5, 8, 12]),
                    random.choice(['key', 'critical', 'innovative'])
                )
            elif experience_level == 'mid':
                achievement = template.format(
                    random.choice(['digital transformation', 'process improvement', 'team optimization']),
                    random.choice([15, 25, 35]),
                    random.choice([8, 12, 15]),
                    random.choice([3, 5, 8]),
                    random.choice([150, 200, 300]),
                    random.choice([30, 40, 50])
                )
            elif experience_level == 'senior':
                achievement = template.format(
                    random.choice(['digital', 'operational', 'strategic']),
                    random.choice([2, 3, 5]),
                    random.choice([20, 30, 50]),
                    random.choice([10, 15, 25]),
                    random.choice([5, 8, 12]),
                    random.choice(['development', 'security', 'quality'])
                )
            else:  # executive
                achievement = template.format(
                    random.choice(['growth', 'expansion', 'innovation']),
                    random.choice([25, 35, 50]),
                    random.choice([200, 500, 1000]),
                    random.choice([5, 8, 12]),
                    random.choice([50, 75, 100]),
                    random.choice([3, 5, 7])
                )
            achievements.append(achievement)
        else:
            achievements.append(template)
    
    return achievements

def suggest_skills(job_title):
    """Suggest relevant skills based on job title"""
    job_lower = job_title.lower() if job_title else ''
    
    for industry, skills in JOB_KEYWORDS.items():
        if industry in job_lower:
            return skills
    
    return ['Communication', 'Problem Solving', 'Leadership', 'Time Management', 'Teamwork', 'Critical Thinking']

def generate_resume_theme(job_title, experience_level):
    """Generate colorful theme based on job and experience"""
    themes = {
        'software': {'primary': '#10b981', 'secondary': '#34d399', 'accent': '#6ee7b7', 'bg': 'linear-gradient(135deg, #ecfdf5, #d1fae5, #a7f3d0)', 'style': 'Modern, tech-focused'},
        'marketing': {'primary': '#f59e0b', 'secondary': '#fbbf24', 'accent': '#fcd34d', 'bg': 'linear-gradient(135deg, #fffbeb, #fef3c7, #fed7aa)', 'style': 'Creative, energetic'},
        'design': {'primary': '#8b5cf6', 'secondary': '#a78bfa', 'accent': '#c4b5fd', 'bg': 'linear-gradient(135deg, #f5f3ff, #ede9fe, #ddd6fe)', 'style': 'Artistic, sophisticated'},
        'finance': {'primary': '#3b82f6', 'secondary': '#60a5fa', 'accent': '#93c5fd', 'bg': 'linear-gradient(135deg, #eff6ff, #dbeafe, #bfdbfe)', 'style': 'Professional, trustworthy'},
        'sales': {'primary': '#ef4444', 'secondary': '#f87171', 'accent': '#fca5a5', 'bg': 'linear-gradient(135deg, #fef2f2, #fecaca, #fca5a5)', 'style': 'Bold, dynamic'},
        'project': {'primary': '#6366f1', 'secondary': '#818cf8', 'accent': '#a5b4fc', 'bg': 'linear-gradient(135deg, #eef2ff, #e0e7ff, #c7d2fe)', 'style': 'Organized, leadership-focused'},
        'tech': {'primary': '#10b981', 'secondary': '#34d399', 'accent': '#6ee7b7', 'bg': 'linear-gradient(135deg, #ecfdf5, #d1fae5, #a7f3d0)', 'style': 'Modern, tech-focused'},
        'engineer': {'primary': '#10b981', 'secondary': '#34d399', 'accent': '#6ee7b7', 'bg': 'linear-gradient(135deg, #ecfdf5, #d1fae5, #a7f3d0)', 'style': 'Modern, tech-focused'},
        'developer': {'primary': '#10b981', 'secondary': '#34d399', 'accent': '#6ee7b7', 'bg': 'linear-gradient(135deg, #ecfdf5, #d1fae5, #a7f3d0)', 'style': 'Modern, tech-focused'}
    }
    
    job_lower = job_title.lower() if job_title else ''
    
    # Enhanced job detection
    for industry in themes.keys():
        if industry in job_lower:
            return themes[industry]
    
    # Additional keyword matching
    if any(word in job_lower for word in ['code', 'program', 'web', 'app', 'tech', 'it']):
        return themes['software']
    elif any(word in job_lower for word in ['market', 'brand', 'social', 'content', 'digital']):
        return themes['marketing']
    elif any(word in job_lower for word in ['design', 'ui', 'ux', 'graphic', 'creative']):
        return themes['design']
    elif any(word in job_lower for word in ['finance', 'account', 'bank', 'invest', 'money']):
        return themes['finance']
    elif any(word in job_lower for word in ['sales', 'sell', 'business', 'client', 'customer']):
        return themes['sales']
    elif any(word in job_lower for word in ['project', 'manage', 'lead', 'coordinator', 'scrum']):
        return themes['project']
    
    # Default rainbow theme
    return {'primary': '#6366f1', 'secondary': '#8b5cf6', 'accent': '#ec4899', 'bg': 'linear-gradient(135deg, #fdf2f8, #f3e8ff, #ede9fe)', 'style': 'Colorful, unique'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/templates')
def templates():
    return render_template('templates.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    job_title = data.get('jobTitle', '')
    experience_level = data.get('experienceLevel', 'mid')
    skills = data.get('skills', '')
    
    # Generate AI-powered content
    summary = generate_ai_summary(job_title, experience_level, skills)
    achievements = generate_ai_achievements(experience_level, job_title)
    
    # Process skills or suggest based on job title
    if skills:
        skill_list = [s.strip() for s in skills.split(',') if s.strip()]
    else:
        skill_list = suggest_skills(job_title)
    
    # Generate colorful theme
    theme = generate_resume_theme(job_title, experience_level)
    
    return jsonify({
        'fullName': data.get('fullName', 'John Doe'),
        'summary': summary,
        'jobTitle': job_title,
        'skills': skill_list,
        'achievements': achievements,
        'workExperience': data.get('workExperience', ''),
        'education': data.get('education', ''),
        'certifications': data.get('certifications', '').split(',') if data.get('certifications') else [],
        'theme': theme
    })

@app.route('/templates')
def get_templates():
    templates = [
        {'id': 1, 'name': 'Classic Blue', 'description': 'Traditional design with a modern twist', 'category': 'Professional'},
        {'id': 2, 'name': 'Modern Purple', 'description': 'Clean and contemporary design', 'category': 'Modern'},
        {'id': 3, 'name': 'Green Executive', 'description': 'Professional design for finance and business', 'category': 'Executive'},
        {'id': 4, 'name': 'Creative Pink', 'description': 'Designed for creatives and designers', 'category': 'Creative'},
        {'id': 5, 'name': 'Minimalist', 'description': 'Clean and minimal design with focus on content', 'category': 'Minimal'},
        {'id': 6, 'name': 'Warm Amber', 'description': 'Warm and inviting design for technical roles', 'category': 'Technical'},
        {'id': 7, 'name': 'Sky Blue', 'description': 'Calm and professional design for HR roles', 'category': 'HR'},
        {'id': 8, 'name': 'Deep Purple', 'description': 'Elegant design for product and management roles', 'category': 'Management'},
        {'id': 9, 'name': 'Vibrant Magenta', 'description': 'Creative design for marketing professionals', 'category': 'Marketing'},
        {'id': 10, 'name': 'Bold Coral', 'description': 'Strong design for sales and leadership roles', 'category': 'Sales'}
    ]
    return jsonify(templates)

@app.route('/examples')
def get_examples():
    examples = [
        {
            'title': 'Software Engineer',
            'experience': 'senior',
            'summary': 'Full-stack developer with 8+ years building scalable applications',
            'skills': ['JavaScript', 'React', 'Node.js', 'AWS', 'Python', 'Docker']
        },
        {
            'title': 'Marketing Manager', 
            'experience': 'mid',
            'summary': 'Digital marketing professional with proven campaign success',
            'skills': ['SEO', 'Google Analytics', 'Social Media', 'Content Marketing']
        },
        {
            'title': 'Project Manager',
            'experience': 'senior', 
            'summary': 'Certified PMP with enterprise project delivery experience',
            'skills': ['Agile', 'Scrum', 'Risk Management', 'Stakeholder Management']
        }
    ]
    return jsonify(examples)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)