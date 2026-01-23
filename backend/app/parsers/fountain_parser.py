"""
Fountain Screenplay Parser

Parses Fountain format screenplay files into structured scene data.
Fountain spec: https://fountain.io/syntax
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class ElementType(Enum):
    """Types of screenplay elements"""
    SCENE_HEADING = "scene_heading"
    ACTION = "action"
    CHARACTER = "character"
    DIALOGUE = "dialogue"
    PARENTHETICAL = "parenthetical"
    TRANSITION = "transition"
    CENTERED = "centered"
    PAGE_BREAK = "page_break"
    SECTION = "section"
    SYNOPSIS = "synopsis"
    NOTE = "note"
    TITLE_PAGE = "title_page"


@dataclass
class SceneElement:
    """Individual screenplay element"""
    element_type: ElementType
    content: str
    line_number: int
    metadata: Optional[Dict] = None


@dataclass
class Scene:
    """Parsed screenplay scene"""
    scene_number: Optional[int]
    heading: str
    location: str
    time_of_day: str
    interior_exterior: str
    elements: List[SceneElement]
    start_line: int
    end_line: int
    
    def get_dialogue(self) -> List[Dict[str, str]]:
        """Extract all dialogue from scene"""
        dialogue = []
        current_character = None
        
        for element in self.elements:
            if element.element_type == ElementType.CHARACTER:
                current_character = element.content
            elif element.element_type == ElementType.DIALOGUE and current_character:
                dialogue.append({
                    "character": current_character,
                    "text": element.content
                })
        
        return dialogue
    
    def get_action_lines(self) -> List[str]:
        """Extract all action/description lines"""
        return [
            elem.content for elem in self.elements 
            if elem.element_type == ElementType.ACTION
        ]


class FountainParser:
    """Parse Fountain format screenplay files"""
    
    # Regex patterns based on Fountain spec
    SCENE_HEADING_PATTERN = r'^(INT|EXT|EST|INT\.\/EXT|I\/E)[\.\s](.+?)(\s*-\s*(.+))?$'
    CHARACTER_PATTERN = r'^([A-Z][A-Z\s\.\(\)]+?)(\s*\^)?$'
    TRANSITION_PATTERN = r'^([A-Z\s]+TO:)$'
    CENTERED_PATTERN = r'^>\s*(.+?)\s*<$'
    SECTION_PATTERN = r'^(#{1,6})\s+(.+)$'
    SYNOPSIS_PATTERN = r'^=\s+(.+)$'
    NOTE_PATTERN = r'\[\[(.+?)\]\]'
    TITLE_PAGE_PATTERN = r'^([A-Za-z\s]+):\s*(.+)$'
    PAGE_BREAK_PATTERN = r'^={3,}$'
    
    def __init__(self):
        self.lines: List[str] = []
        self.current_line: int = 0
        self.title_page: Dict[str, str] = {}
        self.scenes: List[Scene] = []
    
    def parse_file(self, file_path: str) -> List[Scene]:
        """Parse a Fountain file and return list of scenes"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse_string(content)
    
    def parse_string(self, content: str) -> List[Scene]:
        """Parse Fountain content string"""
        self.lines = content.split('\n')
        self.current_line = 0
        self.title_page = {}
        self.scenes = []
        
        # Parse title page (if exists)
        self._parse_title_page()
        
        # Parse body (scenes)
        while self.current_line < len(self.lines):
            scene = self._parse_scene()
            if scene:
                self.scenes.append(scene)
        
        return self.scenes
    
    def _parse_title_page(self):
        """Parse title page metadata"""
        while self.current_line < len(self.lines):
            line = self.lines[self.current_line].strip()
            
            # Title page ends at first blank line
            if not line:
                self.current_line += 1
                break
            
            match = re.match(self.TITLE_PAGE_PATTERN, line)
            if match:
                key = match.group(1).strip().lower()
                value = match.group(2).strip()
                self.title_page[key] = value
                self.current_line += 1
            else:
                # Not title page format, start parsing scenes
                break
    
    def _parse_scene(self) -> Optional[Scene]:
        """Parse a single scene"""
        # Find scene heading
        scene_heading_line = self._find_next_scene_heading()
        if scene_heading_line is None:
            return None
        
        self.current_line = scene_heading_line
        heading_line = self.lines[self.current_line].strip()
        
        # Parse scene heading
        match = re.match(self.SCENE_HEADING_PATTERN, heading_line, re.IGNORECASE)
        if not match:
            self.current_line += 1
            return None
        
        int_ext = match.group(1).upper()
        location = match.group(2).strip()
        time_of_day = match.group(4).strip() if match.group(4) else "UNKNOWN"
        
        scene_start = self.current_line
        self.current_line += 1
        
        # Parse scene elements until next scene or end
        elements = []
        while self.current_line < len(self.lines):
            line = self.lines[self.current_line]
            
            # Check if next scene
            if re.match(self.SCENE_HEADING_PATTERN, line.strip(), re.IGNORECASE):
                break
            
            element = self._parse_element(line)
            if element:
                elements.append(element)
            
            self.current_line += 1
        
        scene = Scene(
            scene_number=len(self.scenes) + 1,
            heading=heading_line,
            location=location,
            time_of_day=time_of_day,
            interior_exterior=int_ext,
            elements=elements,
            start_line=scene_start,
            end_line=self.current_line - 1
        )
        
        return scene
    
    def _find_next_scene_heading(self) -> Optional[int]:
        """Find the next scene heading line number"""
        while self.current_line < len(self.lines):
            line = self.lines[self.current_line].strip()
            if re.match(self.SCENE_HEADING_PATTERN, line, re.IGNORECASE):
                return self.current_line
            self.current_line += 1
        return None
    
    def _parse_element(self, line: str) -> Optional[SceneElement]:
        """Parse a single screenplay element"""
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            return None
        
        # Check element types in order
        
        # Centered text
        if re.match(self.CENTERED_PATTERN, stripped):
            match = re.match(self.CENTERED_PATTERN, stripped)
            return SceneElement(
                element_type=ElementType.CENTERED,
                content=match.group(1),
                line_number=self.current_line
            )
        
        # Transition
        if re.match(self.TRANSITION_PATTERN, stripped):
            return SceneElement(
                element_type=ElementType.TRANSITION,
                content=stripped,
                line_number=self.current_line
            )
        
        # Character (must be all caps, must check BEFORE parenthetical!)
        # Character rule: All caps, next line is dialogue or parenthetical
        if re.match(self.CHARACTER_PATTERN, stripped):
            # Look ahead to see if next line is dialogue or parenthetical
            if self.current_line + 1 < len(self.lines):
                next_line = self.lines[self.current_line + 1].strip()
                # If next line is parenthetical or non-character, this is a character name
                if next_line and (next_line.startswith('(') or not re.match(self.CHARACTER_PATTERN, next_line)):
                    return SceneElement(
                        element_type=ElementType.CHARACTER,
                        content=stripped.rstrip('^').strip(),
                        line_number=self.current_line
                    )
        
        # Parenthetical (dialogue direction) - AFTER character check
        if stripped.startswith('(') and stripped.endswith(')'):
            return SceneElement(
                element_type=ElementType.PARENTHETICAL,
                content=stripped,
                line_number=self.current_line
            )
        
        # Section heading
        if re.match(self.SECTION_PATTERN, stripped):
            match = re.match(self.SECTION_PATTERN, stripped)
            return SceneElement(
                element_type=ElementType.SECTION,
                content=match.group(2),
                line_number=self.current_line,
                metadata={"level": len(match.group(1))}
            )
        
        # Synopsis
        if re.match(self.SYNOPSIS_PATTERN, stripped):
            match = re.match(self.SYNOPSIS_PATTERN, stripped)
            return SceneElement(
                element_type=ElementType.SYNOPSIS,
                content=match.group(1),
                line_number=self.current_line
            )
        
        # Page break
        if re.match(self.PAGE_BREAK_PATTERN, stripped):
            return SceneElement(
                element_type=ElementType.PAGE_BREAK,
                content="",
                line_number=self.current_line
            )
        
        # Check if previous element was a character (dialogue)
        # This is a heuristic - if previous non-empty non-parenthetical line was CHARACTER, this is DIALOGUE
        for i in range(self.current_line - 1, -1, -1):
            prev_line = self.lines[i].strip()
            if not prev_line:
                continue
            # Skip parentheticals when looking back
            if prev_line.startswith('(') and prev_line.endswith(')'):
                continue
            if re.match(self.CHARACTER_PATTERN, prev_line):
                return SceneElement(
                    element_type=ElementType.DIALOGUE,
                    content=stripped,
                    line_number=self.current_line
                )
            break
        
        # Default to action
        return SceneElement(
            element_type=ElementType.ACTION,
            content=stripped,
            line_number=self.current_line
        )
    
    def get_all_dialogue_text(self) -> str:
        """Extract all dialogue from all scenes as single string"""
        all_dialogue = []
        for scene in self.scenes:
            for dialogue_item in scene.get_dialogue():
                all_dialogue.append(dialogue_item['text'])
        return " ".join(all_dialogue)
    
    def get_all_action_text(self) -> str:
        """Extract all action description from all scenes"""
        all_action = []
        for scene in self.scenes:
            all_action.extend(scene.get_action_lines())
        return " ".join(all_action)
