#!/usr/bin/env python3
"""
Comprehensive cross-role analysis script for DevPrompt system
Runs all personas, generates reviews, and provides overall system assessment

Usage:
  python3 analyze_system.py                           # Run all personas
  python3 analyze_system.py --personas role1,role2   # Run specific personas
  python3 analyze_system.py --beginners              # Run only beginner personas
  python3 analyze_system.py --advanced               # Run only advanced personas
  python3 analyze_system.py --list                   # List all available personas
"""
import os
import subprocess
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import time

# All available personas (software development focused)
ALL_PERSONAS = [
    'senior_fullstack', 'junior_frontend', 'computer_science_student', 
    'curious_beginner', 'emergency_manager', 'devops_engineer', 'mobile_developer', 
    'freelance_consultant', 'security_engineer', 'startup_cto', 'data_scientist'
]

# Predefined persona groups
PERSONA_GROUPS = {
    "beginners": ["computer_science_student", "junior_frontend", "curious_beginner"],
    "necessity": ["emergency_manager"],  # Pure necessity-driven users
    "intermediate": ["devops_engineer", "mobile_developer", "freelance_consultant", "data_scientist"],
    "advanced": ["senior_fullstack", "security_engineer", "startup_cto"],
    "technical": ["senior_fullstack", "devops_engineer", "security_engineer", "data_scientist"],
    "frontend": ["junior_frontend", "senior_fullstack", "freelance_consultant"],
    "motivation_test": ["curious_beginner", "emergency_manager"],  # Test both motivation types
    "quick": ["senior_fullstack", "curious_beginner", "emergency_manager"]  # For faster testing
}

def run_persona_test(persona: str) -> Tuple[str, float, str]:
    """Run test for a single persona and return review, score, and timing"""
    print(f"  🧪 Testing {persona}...")
    
    start_time = time.time()
    
    try:
        # Run the test and capture output
        result = subprocess.run(
            ['python3', 'test_devprompt.py', '-r', persona],
            capture_output=True,
            text=True,
            timeout=120,  # 2 minutes per persona
            env={**os.environ, 'OPENAI_API_KEY': open('key.txt').read().strip()}
        )
        
        if result.returncode != 0:
            return f"ERROR: {result.stderr}", 0.0, time.time() - start_time
            
        review = result.stdout.strip()
        
        # Extract score
        score_match = re.search(r'SCORE:\s*(\d+)/10', review)
        score = float(score_match.group(1)) if score_match else 0.0
        
        return review, score, time.time() - start_time
        
    except subprocess.TimeoutExpired:
        return "ERROR: Test timed out", 0.0, time.time() - start_time
    except Exception as e:
        return f"ERROR: {str(e)}", 0.0, time.time() - start_time

def analyze_scores(results: Dict[str, Tuple[str, float, float]], selected_personas: List[str]) -> Dict:
    """Analyze scoring patterns across personas"""
    scores = [(persona, score) for persona, (_, score, _) in results.items() if score > 0]
    
    if not scores:
        return {"error": "No valid scores found"}
    
    score_values = [score for _, score in scores]
    
    analysis = {
        "total_personas": len(selected_personas),
        "successful_tests": len(scores),
        "failed_tests": len(selected_personas) - len(scores),
        "average_score": sum(score_values) / len(score_values),
        "min_score": min(score_values),
        "max_score": max(score_values),
        "score_distribution": {
            "excellent (9-10)": len([s for s in score_values if s >= 9]),
            "good (7-8)": len([s for s in score_values if 7 <= s < 9]),
            "fair (5-6)": len([s for s in score_values if 5 <= s < 7]),
            "poor (1-4)": len([s for s in score_values if s < 5])
        },
        "by_persona": {persona: score for persona, score in scores}
    }
    
    return analysis

def categorize_personas_by_experience(results: Dict[str, Tuple[str, float, float]]) -> Dict:
    """Categorize personas by experience level and analyze patterns"""
    
    categories = {
        "beginners": ["computer_science_student", "junior_frontend", "hobbyist_parent"],
        "intermediate": ["data_scientist", "devops_engineer", "mobile_developer"],
        "advanced": ["senior_fullstack", "freelance_consultant", "security_engineer", "startup_cto"]
    }
    
    analysis = {}
    
    for category, persona_list in categories.items():
        scores = []
        for persona in persona_list:
            if persona in results and results[persona][1] > 0:
                scores.append(results[persona][1])
        
        if scores:
            analysis[category] = {
                "count": len(scores),
                "average_score": sum(scores) / len(scores),
                "scores": scores,
                "personas": persona_list
            }
    
    return analysis

def extract_common_feedback_themes(results: Dict[str, Tuple[str, float, float]]) -> Dict:
    """Extract common themes from feedback across personas"""
    
    all_reviews = []
    for persona, (review, score, _) in results.items():
        if score > 0:  # Only successful reviews
            all_reviews.append((persona, review, score))
    
    # Common weakness patterns
    weakness_patterns = {
        "overwhelming": ["overwhelming", "complex", "too much", "advanced", "intimidating"],
        "beginner_support": ["beginner", "learning", "patient", "simple", "educational"],
        "flexibility": ["flexible", "rigid", "adaptable", "context", "situation"],
        "experience_mismatch": ["experience", "level", "appropriate", "suitable", "relevant"]
    }
    
    theme_analysis = {}
    
    for theme, keywords in weakness_patterns.items():
        mentions = 0
        personas_affected = []
        
        for persona, review, score in all_reviews:
            review_lower = review.lower()
            if any(keyword in review_lower for keyword in keywords):
                mentions += 1
                personas_affected.append((persona, score))
        
        theme_analysis[theme] = {
            "mentions": mentions,
            "percentage": (mentions / len(all_reviews)) * 100,
            "affected_personas": personas_affected
        }
    
    return theme_analysis

def generate_system_recommendations(score_analysis: Dict, experience_analysis: Dict, theme_analysis: Dict) -> List[str]:
    """Generate specific recommendations for system improvement"""
    
    recommendations = []
    
    # Score-based recommendations
    if score_analysis["average_score"] < 7:
        recommendations.append("🔴 CRITICAL: Overall system performance is below acceptable threshold (avg: {:.1f}/10)".format(score_analysis["average_score"]))
    
    # Experience-level recommendations
    if "beginners" in experience_analysis:
        beginner_avg = experience_analysis["beginners"]["average_score"]
        if beginner_avg < 6:
            recommendations.append(f"🟡 PRIORITY: Beginner experience needs improvement (avg: {beginner_avg:.1f}/10)")
            recommendations.append("   → Implement simpler question flow for beginners")
            recommendations.append("   → Add educational context and explanations")
            recommendations.append("   → Reduce prompt complexity for learning-focused users")
    
    # Theme-based recommendations
    if theme_analysis["overwhelming"]["percentage"] > 30:
        recommendations.append("🟠 ISSUE: System frequently overwhelms users")
        recommendations.append("   → Implement adaptive question stopping based on experience")
        recommendations.append("   → Simplify generated prompts for junior developers")
    
    if theme_analysis["beginner_support"]["percentage"] > 25:
        recommendations.append("🟡 IMPROVEMENT: Beginner support frequently mentioned")
        recommendations.append("   → Add learning-focused prompt templates")
        recommendations.append("   → Include educational resources in generated prompts")
    
    # Success pattern recommendations
    if score_analysis["score_distribution"]["excellent (9-10)"] >= 5:
        recommendations.append("✅ STRENGTH: System performs excellently for experienced developers")
        recommendations.append("   → Leverage advanced questioning patterns for senior users")
    
    return recommendations

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="DevPrompt System Analysis")
    
    # Mutually exclusive group for persona selection
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--personas', type=str, help='Comma-separated list of specific personas to test')
    group.add_argument('--beginners', action='store_true', help='Test only beginner personas')
    group.add_argument('--intermediate', action='store_true', help='Test only intermediate personas') 
    group.add_argument('--advanced', action='store_true', help='Test only advanced personas')
    group.add_argument('--technical', action='store_true', help='Test only technical personas')
    group.add_argument('--frontend', action='store_true', help='Test only frontend-focused personas')
    group.add_argument('--quick', action='store_true', help='Run quick test with 3 representative personas')
    group.add_argument('--list', action='store_true', help='List all available personas and groups')
    
    return parser.parse_args()

def select_personas(args) -> List[str]:
    """Select which personas to run based on arguments"""
    
    if args.list:
        print("📋 Available Personas:")
        print("=" * 30)
        for persona in ALL_PERSONAS:
            print(f"  • {persona}")
        print()
        print("📋 Available Groups:")
        print("=" * 30)
        for group_name, personas in PERSONA_GROUPS.items():
            print(f"  • {group_name}: {', '.join(personas)}")
        exit(0)
    
    if args.personas:
        requested = [p.strip() for p in args.personas.split(',')]
        invalid = [p for p in requested if p not in ALL_PERSONAS]
        if invalid:
            print(f"❌ Invalid personas: {', '.join(invalid)}")
            print(f"Available personas: {', '.join(ALL_PERSONAS)}")
            exit(1)
        return requested
    
    # Check group flags
    for group_name in PERSONA_GROUPS.keys():
        if getattr(args, group_name, False):
            return PERSONA_GROUPS[group_name]
    
    # Default: run all personas
    return ALL_PERSONAS

def main():
    args = parse_args()
    selected_personas = select_personas(args)
    
    print("🚀 DevPrompt System Analysis")
    print("=" * 50)
    print(f"Testing {len(selected_personas)} developer personas...")
    if len(selected_personas) < len(ALL_PERSONAS):
        print(f"Selected personas: {', '.join(selected_personas)}")
    print()
    
    # Ensure reviews directory exists
    os.makedirs("reviews", exist_ok=True)
    
    # Run selected persona tests
    results = {}
    total_start_time = time.time()
    
    for persona in selected_personas:
        review, score, duration = run_persona_test(persona)
        results[persona] = (review, score, duration)
        
        # Save review to file
        with open(f"reviews/{persona}_review.txt", "w") as f:
            f.write(review)
        
        print(f"    ✅ {persona}: {score}/10 ({duration:.1f}s)")
    
    total_duration = time.time() - total_start_time
    
    print()
    print("📊 SYSTEM ANALYSIS RESULTS")
    print("=" * 50)
    
    # Overall scoring analysis
    score_analysis = analyze_scores(results, selected_personas)
    print(f"🎯 Overall Performance:")
    print(f"   Average Score: {score_analysis['average_score']:.1f}/10")
    print(f"   Range: {score_analysis['min_score']}/10 - {score_analysis['max_score']}/10")
    print(f"   Success Rate: {score_analysis['successful_tests']}/{score_analysis['total_personas']} ({score_analysis['successful_tests']/score_analysis['total_personas']*100:.1f}%)")
    print()
    
    # Score distribution
    print("📈 Score Distribution:")
    for category, count in score_analysis['score_distribution'].items():
        percentage = (count / score_analysis['successful_tests']) * 100
        print(f"   {category}: {count} personas ({percentage:.1f}%)")
    print()
    
    # Experience level analysis (only if we have relevant personas)
    experience_analysis = categorize_personas_by_experience(results)
    if experience_analysis:
        print("👥 Performance by Experience Level:")
        for level, data in experience_analysis.items():
            print(f"   {level.title()}: {data['average_score']:.1f}/10 avg ({data['count']} personas)")
            for persona in data['personas']:
                if persona in score_analysis['by_persona']:
                    score = score_analysis['by_persona'][persona]
                    print(f"     • {persona}: {score}/10")
        print()
    
    # Theme analysis
    theme_analysis = extract_common_feedback_themes(results)
    print("🔍 Common Feedback Themes:")
    for theme, data in theme_analysis.items():
        if data['mentions'] > 0:
            print(f"   {theme.replace('_', ' ').title()}: {data['mentions']} mentions ({data['percentage']:.1f}%)")
    print()
    
    # Generate recommendations
    recommendations = generate_system_recommendations(score_analysis, experience_analysis, theme_analysis)
    print("💡 SYSTEM RECOMMENDATIONS")
    print("=" * 50)
    for rec in recommendations:
        print(rec)
    
    if not recommendations:
        print("✅ System performing well across all metrics!")
    
    print()
    print("⏱️  PERFORMANCE METRICS")
    print("=" * 50)
    print(f"Total Analysis Time: {total_duration:.1f} seconds")
    print(f"Average Time per Persona: {total_duration/len(selected_personas):.1f} seconds")
    print(f"Reviews saved to: reviews/ directory")
    
    # Generate summary JSON for programmatic analysis
    summary = {
        "timestamp": time.time(),
        "total_duration": total_duration,
        "selected_personas": selected_personas,
        "score_analysis": score_analysis,
        "experience_analysis": experience_analysis,
        "theme_analysis": theme_analysis,
        "recommendations": recommendations
    }
    
    with open("system_analysis_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"📄 Detailed summary saved to: system_analysis_summary.json")

if __name__ == "__main__":
    main()