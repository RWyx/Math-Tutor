# Math Tutor — Socratic AI Tutor

A conversational AI tutor that guides students through math problems step by step, instead of dumping full solutions.

## Motivation

When I upload a problem to AI, it gives a wall of text I can't read. 
This project makes AI ask "where are you stuck?" and explain only that one step.

## How it works

- Student describes a math problem in natural language
- AI asks where they are stuck (Socratic method)
- AI explains one step at a time and checks understanding before continuing

## Tech Stack

- Python
- DeepSeek API (OpenAI-compatible)
- `python-dotenv` for API key management

## Setup

1. Clone the repo
2. Create `API_KEY.env` with your DeepSeek API key: DEEPSEEK_API_KEY=your_key_here
3. Install dependencies:
```bash
   pip install openai python-dotenv
```
4. Run:
```bash
   python test.py
```

## Next Steps

- [ ] Accept image/screenshot input
- [ ] Accept PDF input  
- [ ] Web interface with Streamlit