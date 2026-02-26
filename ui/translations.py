"""Translation system for multi-language support."""

# Translation dictionaries for UI text
TRANSLATIONS = {
    "english": {
        # Navigation
        "home": "Home",
        "upload_code": "Upload Code",
        "explanations": "Explanations",
        "learning_paths": "Learning Paths",
        "quizzes": "Quizzes",
        "flashcards": "Flashcards",
        "progress": "Progress",
        
        # Home page
        "welcome_title": "Welcome to CodeGuru India",
        "welcome_subtitle": "Learn Code Faster with AI-Powered Explanations",
        "feature_analysis": "Smart Code Analysis",
        "feature_analysis_desc": "Upload files or GitHub repos",
        "feature_voice": "Voice Queries",
        "feature_voice_desc": "Ask questions in English, Hindi, or Telugu",
        "feature_learning": "Interactive Learning",
        "feature_learning_desc": "Flashcards, quizzes, and learning paths",
        "feature_progress": "Progress Tracking",
        "feature_progress_desc": "Monitor your growth over time",
        "feature_analogies": "Simple Analogies",
        "feature_analogies_desc": "Complex concepts explained simply",
        
        # Code upload
        "upload_title": "Upload Code for Analysis",
        "file_upload": "File Upload",
        "github_repo": "GitHub Repository",
        "voice_query": "Voice Query",
        "upload_file": "Upload a Code File",
        "supported_formats": "Supported formats",
        "max_file_size": "Max file size",
        "choose_file": "Choose a code file",
        "analyze_repo": "Analyze GitHub Repository",
        "max_repo_size": "Max repository size",
        "repo_url_placeholder": "https://github.com/username/repository",
        "valid_url": "Valid GitHub URL",
        "invalid_url": "Please enter a valid GitHub URL",
        "voice_questions": "Ask Questions with Voice",
        "speak_languages": "Speak in English, Hindi, or Telugu",
        "start_recording": "Start Recording",
        "type_question": "Or type your question here",
        "question_placeholder": "What does this function do?",
        "analysis_options": "Analysis Options",
        "enable_debugging": "Enable Debugging Analysis",
        "generate_diagrams": "Generate Diagrams",
        "explanation_difficulty": "Explanation Difficulty",
        "generate_flashcards": "Generate Flashcards",
        "analyze_code": "Analyze Code",
        "analyzing": "Analyzing your code...",
        "analysis_complete": "Analysis complete!",
        "generated_flashcards": "Generated {count} flashcards.",
        
        # Explanations
        "code_explanations": "Code Explanations",
        "summary": "Summary",
        "details": "Details",
        "diagrams": "Diagrams",
        "issues": "Issues",
        "code_summary": "Code Summary",
        "code_structure": "Code Structure",
        "functions": "Functions",
        "classes": "Classes",
        "complexity": "Complexity",
        "patterns_detected": "Patterns Detected",
        "key_concepts": "Key Concepts",
        "simple_analogies": "Simple Analogies",
        
        # Learning paths
        "learning_paths_title": "Learning Paths",
        "choose_journey": "Choose Your Learning Journey",
        "select_path": "Select a Learning Path",
        "topics": "Topics",
        "est_hours": "Est. Hours",
        "progress_label": "Progress",
        "complete": "Complete",
        "learning_roadmap": "Learning Roadmap",
        "prerequisites": "Prerequisites",
        "start": "Start",
        "review": "Review",
        "locked": "Locked",
        "milestone_achievements": "Milestone Achievements",
        
        # Quizzes
        "interactive_quizzes": "Interactive Quizzes",
        "select_topic": "Select Topic",
        "difficulty": "Difficulty",
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "start_quiz": "Start Quiz",
        "question": "Question",
        "of": "of",
        "submit_answer": "Submit Answer",
        "next_question": "Next Question",
        "previous": "Previous",
        "quiz_complete": "Quiz Complete!",
        "your_score": "Your Score",
        "time_taken": "Time Taken",
        "correct_answers": "Correct Answers",
        
        # Flashcards
        "interactive_flashcards": "Interactive Flashcards",
        "topic": "Topic",
        "all_topics": "All Topics",
        "all_levels": "All Levels",
        "card": "Card",
        "flip_to_back": "Flip to Back",
        "flip_to_front": "Flip to Front",
        "rate_card": "Rate this card:",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "mark_reviewed": "Mark Reviewed",
        "mark_mastered": "Mark as Mastered",
        "no_flashcards": "No flashcards available. Generate flashcards from code analysis!",
        
        # Progress
        "progress_dashboard": "Progress Dashboard",
        "topics_completed": "Topics Completed",
        "avg_quiz_score": "Avg Quiz Score",
        "learning_streak": "Learning Streak",
        "days": "days",
        "time_spent": "Time Spent",
        "hours": "hours",
        "progress_over_time": "Progress Over Time",
        "skill_levels": "Skill Levels",
        "weekly_summary": "Weekly Summary",
        "activities_completed": "Activities Completed",
        "topics_learned": "Topics Learned",
        "achievement_badges": "Achievement Badges",
        
        # Common
        "loading": "Loading...",
        "error": "Error",
        "success": "Success",
        "warning": "Warning",
        "info": "Info",
        "close": "Close",
        "save": "Save",
        "cancel": "Cancel",
        "delete": "Delete",
        "edit": "Edit",
        "view": "View",
        "download": "Download",
    },
    
    "hindi": {
        # Navigation
        "home": "होम",
        "upload_code": "कोड अपलोड करें",
        "explanations": "व्याख्या",
        "learning_paths": "सीखने के रास्ते",
        "quizzes": "क्विज़",
        "flashcards": "फ्लैशकार्ड",
        "progress": "प्रगति",
        
        # Home page
        "welcome_title": "CodeGuru India में आपका स्वागत है",
        "welcome_subtitle": "AI-संचालित व्याख्याओं के साथ तेज़ी से कोड सीखें",
        "feature_analysis": "स्मार्ट कोड विश्लेषण",
        "feature_analysis_desc": "फ़ाइलें या GitHub रेपो अपलोड करें",
        "feature_voice": "वॉयस क्वेरी",
        "feature_voice_desc": "अंग्रेजी, हिंदी या तेलुगु में प्रश्न पूछें",
        "feature_learning": "इंटरैक्टिव लर्निंग",
        "feature_learning_desc": "फ्लैशकार्ड, क्विज़ और सीखने के रास्ते",
        "feature_progress": "प्रगति ट्रैकिंग",
        "feature_progress_desc": "समय के साथ अपनी वृद्धि की निगरानी करें",
        "feature_analogies": "सरल उपमाएं",
        "feature_analogies_desc": "जटिल अवधारणाओं को सरलता से समझाया गया",
        
        # Code upload
        "upload_title": "विश्लेषण के लिए कोड अपलोड करें",
        "file_upload": "फ़ाइल अपलोड",
        "github_repo": "GitHub रिपॉजिटरी",
        "voice_query": "वॉयस क्वेरी",
        "upload_file": "एक कोड फ़ाइल अपलोड करें",
        "supported_formats": "समर्थित प्रारूप",
        "max_file_size": "अधिकतम फ़ाइल आकार",
        "choose_file": "एक कोड फ़ाइल चुनें",
        "analyze_repo": "GitHub रिपॉजिटरी का विश्लेषण करें",
        "max_repo_size": "अधिकतम रिपॉजिटरी आकार",
        "repo_url_placeholder": "https://github.com/username/repository",
        "valid_url": "मान्य GitHub URL",
        "invalid_url": "कृपया एक मान्य GitHub URL दर्ज करें",
        "voice_questions": "वॉयस के साथ प्रश्न पूछें",
        "speak_languages": "अंग्रेजी, हिंदी या तेलुगु में बोलें",
        "start_recording": "रिकॉर्डिंग शुरू करें",
        "type_question": "या यहां अपना प्रश्न टाइप करें",
        "question_placeholder": "यह फ़ंक्शन क्या करता है?",
        "analysis_options": "विश्लेषण विकल्प",
        "enable_debugging": "डिबगिंग विश्लेषण सक्षम करें",
        "generate_diagrams": "आरेख उत्पन्न करें",
        "explanation_difficulty": "व्याख्या कठिनाई",
        "generate_flashcards": "फ्लैशकार्ड उत्पन्न करें",
        "analyze_code": "कोड का विश्लेषण करें",
        "analyzing": "आपके कोड का विश्लेषण किया जा रहा है...",
        "analysis_complete": "विश्लेषण पूर्ण!",
        "generated_flashcards": "{count} फ्लैशकार्ड उत्पन्न किए गए।",
        
        # Explanations
        "code_explanations": "कोड व्याख्या",
        "summary": "सारांश",
        "details": "विवरण",
        "diagrams": "आरेख",
        "issues": "समस्याएं",
        "code_summary": "कोड सारांश",
        "code_structure": "कोड संरचना",
        "functions": "फ़ंक्शन",
        "classes": "क्लासेस",
        "complexity": "जटिलता",
        "patterns_detected": "पैटर्न का पता चला",
        "key_concepts": "मुख्य अवधारणाएं",
        "simple_analogies": "सरल उपमाएं",
        
        # Learning paths
        "learning_paths_title": "सीखने के रास्ते",
        "choose_journey": "अपनी सीखने की यात्रा चुनें",
        "select_path": "एक सीखने का रास्ता चुनें",
        "topics": "विषय",
        "est_hours": "अनुमानित घंटे",
        "progress_label": "प्रगति",
        "complete": "पूर्ण",
        "learning_roadmap": "सीखने का रोडमैप",
        "prerequisites": "पूर्वापेक्षाएँ",
        "start": "शुरू करें",
        "review": "समीक्षा करें",
        "locked": "लॉक",
        "milestone_achievements": "मील का पत्थर उपलब्धियां",
        
        # Quizzes
        "interactive_quizzes": "इंटरैक्टिव क्विज़",
        "select_topic": "विषय चुनें",
        "difficulty": "कठिनाई",
        "beginner": "शुरुआती",
        "intermediate": "मध्यवर्ती",
        "advanced": "उन्नत",
        "start_quiz": "क्विज़ शुरू करें",
        "question": "प्रश्न",
        "of": "का",
        "submit_answer": "उत्तर जमा करें",
        "next_question": "अगला प्रश्न",
        "previous": "पिछला",
        "quiz_complete": "क्विज़ पूर्ण!",
        "your_score": "आपका स्कोर",
        "time_taken": "लिया गया समय",
        "correct_answers": "सही उत्तर",
        
        # Flashcards
        "interactive_flashcards": "इंटरैक्टिव फ्लैशकार्ड",
        "topic": "विषय",
        "all_topics": "सभी विषय",
        "all_levels": "सभी स्तर",
        "card": "कार्ड",
        "flip_to_back": "पीछे की ओर पलटें",
        "flip_to_front": "सामने की ओर पलटें",
        "rate_card": "इस कार्ड को रेट करें:",
        "easy": "आसान",
        "medium": "मध्यम",
        "hard": "कठिन",
        "mark_reviewed": "समीक्षित के रूप में चिह्नित करें",
        "mark_mastered": "महारत हासिल के रूप में चिह्नित करें",
        "no_flashcards": "कोई फ्लैशकार्ड उपलब्ध नहीं। कोड विश्लेषण से फ्लैशकार्ड उत्पन्न करें!",
        
        # Progress
        "progress_dashboard": "प्रगति डैशबोर्ड",
        "topics_completed": "पूर्ण किए गए विषय",
        "avg_quiz_score": "औसत क्विज़ स्कोर",
        "learning_streak": "सीखने की लकीर",
        "days": "दिन",
        "time_spent": "बिताया गया समय",
        "hours": "घंटे",
        "progress_over_time": "समय के साथ प्रगति",
        "skill_levels": "कौशल स्तर",
        "weekly_summary": "साप्ताहिक सारांश",
        "activities_completed": "पूर्ण की गई गतिविधियां",
        "topics_learned": "सीखे गए विषय",
        "achievement_badges": "उपलब्धि बैज",
        
        # Common
        "loading": "लोड हो रहा है...",
        "error": "त्रुटि",
        "success": "सफलता",
        "warning": "चेतावनी",
        "info": "जानकारी",
        "close": "बंद करें",
        "save": "सहेजें",
        "cancel": "रद्द करें",
        "delete": "हटाएं",
        "edit": "संपादित करें",
        "view": "देखें",
        "download": "डाउनलोड करें",
    },
    
    "telugu": {
        # Navigation
        "home": "హోమ్",
        "upload_code": "కోడ్ అప్‌లోడ్ చేయండి",
        "explanations": "వివరణలు",
        "learning_paths": "నేర్చుకునే మార్గాలు",
        "quizzes": "క్విజ్‌లు",
        "flashcards": "ఫ్లాష్‌కార్డ్‌లు",
        "progress": "పురోగతి",
        
        # Home page
        "welcome_title": "CodeGuru India కు స్వాగతం",
        "welcome_subtitle": "AI-శక్తితో కూడిన వివరణలతో వేగంగా కోడ్ నేర్చుకోండి",
        "feature_analysis": "స్మార్ట్ కోడ్ విశ్లేషణ",
        "feature_analysis_desc": "ఫైల్స్ లేదా GitHub రెపోలను అప్‌లోడ్ చేయండి",
        "feature_voice": "వాయిస్ ప్రశ్నలు",
        "feature_voice_desc": "ఇంగ్లీష్, హిందీ లేదా తెలుగులో ప్రశ్నలు అడగండి",
        "feature_learning": "ఇంటరాక్టివ్ లెర్నింగ్",
        "feature_learning_desc": "ఫ్లాష్‌కార్డ్‌లు, క్విజ్‌లు మరియు నేర్చుకునే మార్గాలు",
        "feature_progress": "పురోగతి ట్రాకింగ్",
        "feature_progress_desc": "కాలక్రమేణా మీ పెరుగుదలను పర్యవేక్షించండి",
        "feature_analogies": "సరళమైన ఉపమానాలు",
        "feature_analogies_desc": "సంక్లిష్ట భావనలు సరళంగా వివరించబడ్డాయి",
        
        # Code upload
        "upload_title": "విశ్లేషణ కోసం కోడ్ అప్‌లోడ్ చేయండి",
        "file_upload": "ఫైల్ అప్‌లోడ్",
        "github_repo": "GitHub రిపోజిటరీ",
        "voice_query": "వాయిస్ క్వెరీ",
        "upload_file": "కోడ్ ఫైల్ అప్‌లోడ్ చేయండి",
        "supported_formats": "మద్దతు ఉన్న ఫార్మాట్‌లు",
        "max_file_size": "గరిష్ట ఫైల్ పరిమాణం",
        "choose_file": "కోడ్ ఫైల్ ఎంచుకోండి",
        "analyze_repo": "GitHub రిపోజిటరీని విశ్లేషించండి",
        "max_repo_size": "గరిష్ట రిపోజిటరీ పరిమాణం",
        "repo_url_placeholder": "https://github.com/username/repository",
        "valid_url": "చెల్లుబాటు అయ్యే GitHub URL",
        "invalid_url": "దయచేసి చెల్లుబాటు అయ్యే GitHub URL ను నమోదు చేయండి",
        "voice_questions": "వాయిస్‌తో ప్రశ్నలు అడగండి",
        "speak_languages": "ఇంగ్లీష్, హిందీ లేదా తెలుగులో మాట్లాడండి",
        "start_recording": "రికార్డింగ్ ప్రారంభించండి",
        "type_question": "లేదా మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి",
        "question_placeholder": "ఈ ఫంక్షన్ ఏమి చేస్తుంది?",
        "analysis_options": "విశ్లేషణ ఎంపికలు",
        "enable_debugging": "డీబగ్గింగ్ విశ్లేషణను ప్రారంభించండి",
        "generate_diagrams": "రేఖాచిత్రాలను రూపొందించండి",
        "explanation_difficulty": "వివరణ కష్టం",
        "generate_flashcards": "ఫ్లాష్‌కార్డ్‌లను రూపొందించండి",
        "analyze_code": "కోడ్‌ను విశ్లేషించండి",
        "analyzing": "మీ కోడ్‌ను విశ్లేషిస్తోంది...",
        "analysis_complete": "విశ్లేషణ పూర్తయింది!",
        "generated_flashcards": "{count} ఫ్లాష్‌కార్డ్‌లు రూపొందించబడ్డాయి.",
        
        # Explanations
        "code_explanations": "కోడ్ వివరణలు",
        "summary": "సారాంశం",
        "details": "వివరాలు",
        "diagrams": "రేఖాచిత్రాలు",
        "issues": "సమస్యలు",
        "code_summary": "కోడ్ సారాంశం",
        "code_structure": "కోడ్ నిర్మాణం",
        "functions": "ఫంక్షన్లు",
        "classes": "క్లాసులు",
        "complexity": "సంక్లిష్టత",
        "patterns_detected": "నమూనాలు గుర్తించబడ్డాయి",
        "key_concepts": "ముఖ్య భావనలు",
        "simple_analogies": "సరళమైన ఉపమానాలు",
        
        # Learning paths
        "learning_paths_title": "నేర్చుకునే మార్గాలు",
        "choose_journey": "మీ నేర్చుకునే ప్రయాణాన్ని ఎంచుకోండి",
        "select_path": "నేర్చుకునే మార్గాన్ని ఎంచుకోండి",
        "topics": "అంశాలు",
        "est_hours": "అంచనా గంటలు",
        "progress_label": "పురోగతి",
        "complete": "పూర్తి",
        "learning_roadmap": "నేర్చుకునే రోడ్‌మ్యాప్",
        "prerequisites": "ముందస్తు అవసరాలు",
        "start": "ప్రారంభించండి",
        "review": "సమీక్షించండి",
        "locked": "లాక్ చేయబడింది",
        "milestone_achievements": "మైలురాయి విజయాలు",
        
        # Quizzes
        "interactive_quizzes": "ఇంటరాక్టివ్ క్విజ్‌లు",
        "select_topic": "అంశాన్ని ఎంచుకోండి",
        "difficulty": "కష్టం",
        "beginner": "ప్రారంభకుడు",
        "intermediate": "మధ్యస్థ",
        "advanced": "అధునాతన",
        "start_quiz": "క్విజ్ ప్రారంభించండి",
        "question": "ప్రశ్న",
        "of": "యొక్క",
        "submit_answer": "సమాధానాన్ని సమర్పించండి",
        "next_question": "తదుపరి ప్రశ్న",
        "previous": "మునుపటి",
        "quiz_complete": "క్విజ్ పూర్తయింది!",
        "your_score": "మీ స్కోర్",
        "time_taken": "తీసుకున్న సమయం",
        "correct_answers": "సరైన సమాధానాలు",
        
        # Flashcards
        "interactive_flashcards": "ఇంటరాక్టివ్ ఫ్లాష్‌కార్డ్‌లు",
        "topic": "అంశం",
        "all_topics": "అన్ని అంశాలు",
        "all_levels": "అన్ని స్థాయిలు",
        "card": "కార్డ్",
        "flip_to_back": "వెనుకకు తిప్పండి",
        "flip_to_front": "ముందుకు తిప్పండి",
        "rate_card": "ఈ కార్డ్‌ను రేట్ చేయండి:",
        "easy": "సులభం",
        "medium": "మధ్యస్థ",
        "hard": "కష్టం",
        "mark_reviewed": "సమీక్షించినట్లు గుర్తించండి",
        "mark_mastered": "నైపుణ్యం సాధించినట్లు గుర్తించండి",
        "no_flashcards": "ఫ్లాష్‌కార్డ్‌లు అందుబాటులో లేవు। కోడ్ విశ్లేషణ నుండి ఫ్లాష్‌కార్డ్‌లను రూపొందించండి!",
        
        # Progress
        "progress_dashboard": "పురోగతి డాష్‌బోర్డ్",
        "topics_completed": "పూర్తయిన అంశాలు",
        "avg_quiz_score": "సగటు క్విజ్ స్కోర్",
        "learning_streak": "నేర్చుకునే పరంపర",
        "days": "రోజులు",
        "time_spent": "గడిపిన సమయం",
        "hours": "గంటలు",
        "progress_over_time": "కాలక్రమేణా పురోగతి",
        "skill_levels": "నైపుణ్య స్థాయిలు",
        "weekly_summary": "వారపు సారాంశం",
        "activities_completed": "పూర్తయిన కార్యకలాపాలు",
        "topics_learned": "నేర్చుకున్న అంశాలు",
        "achievement_badges": "విజయ బ్యాడ్జ్‌లు",
        
        # Common
        "loading": "లోడ్ అవుతోంది...",
        "error": "లోపం",
        "success": "విజయం",
        "warning": "హెచ్చరిక",
        "info": "సమాచారం",
        "close": "మూసివేయండి",
        "save": "సేవ్ చేయండి",
        "cancel": "రద్దు చేయండి",
        "delete": "తొలగించండి",
        "edit": "సవరించండి",
        "view": "చూడండి",
        "download": "డౌన్‌లోడ్ చేయండి",
    }
}


def get_text(key: str, language: str = "english") -> str:
    """
    Get translated text for a key.
    
    Args:
        key: Translation key
        language: Language code (english, hindi, telugu)
        
    Returns:
        Translated text or key if not found
    """
    lang_dict = TRANSLATIONS.get(language, TRANSLATIONS["english"])
    return lang_dict.get(key, key)


def format_text(key: str, language: str = "english", **kwargs) -> str:
    """
    Get translated text with formatting.
    
    Args:
        key: Translation key
        language: Language code
        **kwargs: Format arguments
        
    Returns:
        Formatted translated text
    """
    text = get_text(key, language)
    try:
        return text.format(**kwargs)
    except KeyError:
        return text
