import streamlit as st

class QuizManager:
    def __init__(self, questions: list):
        """
        Initialize the QuizManager class with a list of quiz questions.
        """
        self.questions = questions
        self.total_questions = len(questions)

    def get_question_at_index(self, index: int):
        """
        Retrieves the quiz question object at the specified index. If the index is out of bounds,
        it restarts from the beginning index.

        :param index: The index of the question to retrieve.
        :return: The quiz question object at the specified index
        """
        # Ensure index is always within bounds using modulo arithmetic
        valid_index = index % self.total_questions
        return self.questions[valid_index]
    
    def next_question_index(self, direction=1):
        """
        Adjust the current quiz question index based on the specified direction.

        Parameters:
        - direction: An integer indicating the direction to move in the quiz questions list (1 for next, -1 for previous).
        """
        question_index = st.session_state["question_index"]
        # index wrapping
        new_index = (question_index + direction) % self.total_questions
        st.session_state["question_index"] = new_index