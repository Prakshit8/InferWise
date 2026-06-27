from typing import Optional, List, Dict
import re


class TaskDetector:
    """Detect task category from prompt content."""
    
    TASK_PATTERNS = {
        "coding": [
            r"write\s+(?:a\s+)?(?:function|class|code|script|program)",
            r"implement\s+(?:a\s+)?(?:function|class|algorithm)",
            r"create\s+(?:a\s+)?(?:function|class|method)",
            r"debug\s+(?:this\s+)?code",
            r"fix\s+(?:this\s+)?(?:bug|error)",
            r"help\s+me\s+code",
            r"how\s+do\s+i\s+(?:write|implement|create)",
            r"refactor\s+(?:this\s+)?code",
            r"optimize\s+(?:this\s+)?code",
            r"convert\s+(?:this\s+)?code",
            r"translate\s+(?:this\s+)?code",
        ],
        "writing": [
            r"write\s+(?:a\s+)?(?:essay|article|story|blog|post|content)",
            r"create\s+(?:a\s+)?(?:essay|article|story|blog|post)",
            r"draft\s+(?:a\s+)?(?:document|email|letter)",
            r"summarize\s+(?:this\s+)?(?:text|content)",
            r"rewrite\s+(?:this\s+)?(?:text|content)",
            r"edit\s+(?:this\s+)?(?:text|content)",
            r"generate\s+(?:a\s+)?(?:summary|description)",
        ],
        "analysis": [
            r"analyze\s+(?:this\s+)?(?:data|text|code|content)",
            r"explain\s+(?:this\s+)?(?:code|concept|idea)",
            r"what\s+is\s+(?:the\s+)?(?:meaning|purpose|function)",
            r"how\s+does\s+(?:this\s+)?(?:work|function)",
            r"why\s+(?:does\s+)?(?:this\s+)?(?:work|happen)",
            r"compare\s+(?:and\s+contrast)",
            r"evaluate\s+(?:this\s+)?(?:approach|method)",
            r"assess\s+(?:this\s+)?(?:situation|scenario)",
        ],
        "math": [
            r"solve\s+(?:this\s+)?(?:equation|problem|calculation)",
            r"calculate\s+(?:this\s+)?(?:value|result)",
            r"what\s+is\s+\d+\s*[\+\-\*\/]\s*\d+",
            r"compute\s+(?:this\s+)?(?:value|result)",
            r"find\s+(?:the\s+)?(?:solution|answer)",
            r"how\s+much\s+is",
            r"add\s+\d+\s+and\s+\d+",
            r"multiply\s+\d+\s+by\s+\d+",
        ],
        "general": [
            r"tell\s+me\s+about",
            r"what\s+do\s+you\s+think",
            r"can\s+you\s+help\s+me",
            r"i\s+need\s+help",
            r"please\s+help",
        ],
    }
    
    def detect(self, text: str) -> str:
        """Detect task category from text.
        
        Args:
            text: The prompt text to analyze
            
        Returns:
            Detected task category
        """
        text_lower = text.lower()
        
        for task, patterns in self.TASK_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return task
        
        return "general"


class LanguageDetector:
    """Detect programming language from prompt content."""
    
    LANGUAGE_PATTERNS = {
        "python": [
            r"\bdef\s+\w+\s*\(",
            r"\bimport\s+\w+",
            r"\bfrom\s+\w+\s+import",
            r"\bclass\s+\w+.*:",
            r"print\s*\(",
            r"if\s+__name__\s*==\s*['\"]__main__['\"]",
            r"self\.",
            r"#.*",
        ],
        "javascript": [
            r"\bfunction\s+\w+\s*\(",
            r"\bconst\s+\w+\s*=",
            r"\blet\s+\w+\s*=",
            r"\bvar\s+\w+\s*=",
            r"console\.log\s*\(",
            r"=>\s*{",
            r"\.then\s*\(",
            r"async\s+function",
        ],
        "java": [
            r"\bpublic\s+(?:static\s+)?class\s+\w+",
            r"\bpublic\s+(?:static\s+)?void\s+\w+\s*\(",
            r"System\.out\.println",
            r"new\s+\w+\s*\(",
            r"import\s+java\.",
            r"@Override",
        ],
        "c": [
            r"#include\s*<",
            r"\bint\s+main\s*\(",
            r"printf\s*\(",
            r"scanf\s*\(",
            r"return\s+0;",
            r"\*\w+\s*=",
        ],
        "cpp": [
            r"#include\s*<",
            r"std::",
            r"cout\s*<<",
            r"cin\s*>>",
            r"vector<",
            r"using\s+namespace\s+std",
        ],
        "go": [
            r"package\s+main",
            r"func\s+\w+\s*\(",
            r"fmt\.Print",
            r"import\s+\(",
            r"defer\s+",
            r"go\s+func",
        ],
        "rust": [
            r"fn\s+\w+\s*\(",
            r"let\s+mut\s+",
            r"use\s+std::",
            r"println!\s*\(",
            r"impl\s+\w+",
            r"struct\s+\w+",
        ],
        "sql": [
            r"\bSELECT\s+",
            r"\bFROM\s+",
            r"\bWHERE\s+",
            r"\bINSERT\s+INTO",
            r"\bUPDATE\s+",
            r"\bDELETE\s+FROM",
            r"\bJOIN\s+",
            r"\bGROUP\s+BY",
        ],
        "html": [
            r"<html>",
            r"<div",
            r"<p>",
            r"<a\s+href",
            r"<script",
            r"<style",
            r"<!DOCTYPE",
        ],
        "css": [
            r"\.\w+\s*{",
            r"#\w+\s*{",
            r"background-color:",
            r"margin:",
            r"padding:",
            r"display:",
        ],
    }
    
    def detect(self, text: str) -> Optional[str]:
        """Detect programming language from text.
        
        Args:
            text: The prompt text to analyze
            
        Returns:
            Detected programming language or None
        """
        text_lower = text.lower()
        
        for language, patterns in self.LANGUAGE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return language
        
        # Check for language mentions
        language_keywords = {
            "python": ["python", "py"],
            "javascript": ["javascript", "js", "node", "nodejs"],
            "java": ["java"],
            "c": ["c language", "c programming"],
            "cpp": ["c++", "cpp"],
            "go": ["golang", "go"],
            "rust": ["rust"],
            "sql": ["sql", "database"],
            "html": ["html"],
            "css": ["css", "stylesheet"],
        }
        
        for language, keywords in language_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return language
        
        return None
