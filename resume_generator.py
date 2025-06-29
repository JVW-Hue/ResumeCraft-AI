def generate_resume(job_title, experience_level, skills, education, work_experience="", certifications=""):
    """Generate a professional resume based on provided information."""
    
    # Professional summary based on experience level
    summary_templates = {
        "entry": f"Motivated {job_title.lower()} with strong foundational skills and eagerness to contribute to dynamic teams. Quick learner with excellent problem-solving abilities and commitment to professional growth.",
        "junior": f"Results-driven {job_title.lower()} with proven ability to deliver quality work and collaborate effectively. Strong technical foundation with hands-on experience in relevant technologies.",
        "mid": f"Experienced {job_title.lower()} with demonstrated expertise in delivering successful projects and leading technical initiatives. Proven track record of problem-solving and team collaboration.",
        "senior": f"Senior {job_title.lower()} with extensive experience leading complex projects and mentoring teams. Strategic thinker with deep technical expertise and strong business acumen.",
        "lead": f"Accomplished {job_title} with proven leadership experience and technical excellence. Expert in driving innovation, managing cross-functional teams, and delivering enterprise-level solutions."
    }
    
    summary = summary_templates.get(experience_level.lower(), summary_templates["mid"])
    
    # Format skills
    skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
    skills_formatted = ' • '.join(skills_list)
    
    # Generate resume
    resume = f"""JOHN DOE
{job_title.upper()}

PROFESSIONAL SUMMARY
{summary}

CORE SKILLS
{skills_formatted}

WORK EXPERIENCE
{work_experience if work_experience else f"Ready to begin career as {job_title} with strong academic foundation and practical project experience."}

EDUCATION
{education}"""
    
    if certifications:
        resume += f"\n\nCERTIFICATIONS\n{certifications}"
    
    return resume

# Example usage
if __name__ == "__main__":
    sample_resume = generate_resume(
        job_title="Software Developer",
        experience_level="junior",
        skills="Python, JavaScript, React, SQL, Git",
        education="Bachelor of Science in Computer Science, State University (2023)",
        work_experience="Software Developer Intern | Tech Solutions Inc. | June 2023 - August 2023\n• Developed web applications using React and Node.js\n• Collaborated with senior developers on database optimization\n• Participated in code reviews and agile development processes",
        certifications="AWS Cloud Practitioner (2023)"
    )
    print(sample_resume)