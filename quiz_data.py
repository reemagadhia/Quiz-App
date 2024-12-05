def get_quiz_data():
    quiz_data = {
        "Maths": [
            {
                "question": "If there are 23 boys and 21 girls in Class A, Class B has 21 boys and 22 girls. How many girls and boys are there in Class A and B combined?",
                "choices": ["73 boys and 70 girls", "40 boys and 42 girls", "44 boys and 43 girls", "35 boys and 37 girls"],
                "answer": "44 boys and 43 girls"
            },
            {
                "question": "If you multiply 45.5 by 2, what will be the answer?",
                "choices": ["90.5", "91", "92", "91.5"],
                "answer": "91"
            },
        ],
        "Science": [
            {
                "question": "What is the boiling point of water at sea level in Celsius?",
                "choices": ["90°C", "100°C", "110°C", "120°C"],
                "answer": "100°C"
            },
        ],
        "General Knowledge": [
            {
                "question": "Who was the first president of the United States?",
                "choices": ["Abraham Lincoln", "George Washington", "John Adams", "Thomas Jefferson"],
                "answer": "George Washington"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "choices": ["Earth", "Mars", "Venus", "Jupiter"],
                "answer": "Mars"
            },
            {
                "question": "What is the capital of France?",
                "choices": ["Berlin", "Madrid", "Paris", "Rome"],
                "answer": "Paris"
            }
        ]
    }
    return quiz_data
