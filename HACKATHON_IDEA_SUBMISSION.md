# Hackathon Idea Submission: MSI-VPE (Screenplay Emotion-to-Visual Mapper)

## 💡 Project Title
**MSI-VPE: Emotion-Driven Cinematography Assistant**

## 🚀 Tagline
*Bridging the gap between script and screen: An AI co-pilot that translates screenplay emotions into visual cinematography directives.*

## 😤 The Problem
Indie filmmakers and students often struggle to translate the emotional subtext of a screenplay into concrete visual choices (lighting, color, camera angles). Professional tools are expensive and complex, while manual breakdown is tedious and requires years of theory knowledge. There is no accessible tool that acts as a "digital cinematographer" to visualize the emotional arc of a script before a single frame is shot.

## 🛠 The Solution
**MSI-VPE** is an automated "pre-visualization" engine. It uses Natural Language Processing (NLP) to analyze screenplay text, detect nuanced emotional shifts scene-by-scene, and scientifically map those emotions to cinematographic parameters.

**How it works:**
1.  **Analyze:** Users upload a `.fountain` screenplay. Our system parses the text to identify dialogue, action, and scene headers.
2.  **Detect:** An ensemble of open-source Transformers (RoBERTa) detects 27+ distinct emotions (Joy, Dread, Nostalgia, Tension, etc.) in every beat of the script.
3.  **Map:** A rule-based engine, grounded in film theory, translates emotional data into visual specs:
    *   **Lighting:** Hard vs. soft, warm vs. cool, high vs. low contrast.
    *   **Color:** Generates emotionally congruent color palettes (e.g., desaturated blues for isolation, high-contrast reds for danger).
    *   **Camera:** Recommends angles (Dutch angle for confusion) and movement (handheld for anxiety).
4.  **Visualize:** The web interface presents an interactive timeline of the script's emotional arc alongside specific visual recipes for each scene.

## 💻 Tech Stack
*   **Frontend:** React, Tailwind CSS, Chart.js (for emotional arc visualization)
*   **Backend:** Python, FastAPI
*   **AI/ML:** Hugging Face Transformers (`SamLowe/roberta-base-go_emotions`), PyTorch
*   **Data:** Custom mappings based on standard cinematography textbooks

## 💥 Impact & Value
*   **Democratizes Filmmaking:** Gives novice creators access to expert-level visual theory.
*   **Saves Time:** Automates the "script breakdown" process, allowing directors to focus on creative decisions.
*   **Visualizes Story:** Helps writers and directors "see" the emotional rhythm of their story instantly.

## 🔮 What's Next?
*   **Style Transfer:** "Make this scene look like a Wes Anderson movie."
*   **Image Generation:** Integrating Stable Diffusion to generate storyboard reference images based on our lighting/camera prompts.
*   **Real-Time feedback:** A plugin for screenwriting software (like Final Draft) that gives visual feedback as you type.

## 🔗 Links
*   **Demo:** [Link to Demo]
*   **Repository:** [Link to GitHub]
