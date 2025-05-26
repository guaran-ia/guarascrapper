from polyglot.detect import Detector
import fasttext
import os


class GuaraniDetector:
    def __init__(self):
        # Get absolute path to the model file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "lang_model/lid.176.bin")

        # Load the pretrained model
        self.fasttext_model = fasttext.load_model(model_path)

    def is_guarani(self, text):
        """
        Determine if the input text is in the Guarani language.

        Uses a combination of FastText and Polyglot language detection models
        for more accurate identification.

        Both detection methods must agree on the language being Guarani
        for the function to return True, providing higher confidence
        in the language identification.

        Args:
            text (str): The text to analyze for Guarani language

        Returns:
            bool: True if both detection methods identify the text as Guarani,
                  False otherwise or if the text is too short to analyze
        """
        votes = 0

        # FastText vote
        try:
            # Create a sentence with repeated word for better detection
            text_to_check = (text + " ") * 5
            prediction = self.fasttext_model.predict(text_to_check)
            lang = prediction[0]
            if lang[0] == "__label__gn":
                votes += 1
        except Exception as e:
            print(f"FastText detection error: {e}")

        # Polyglot vote
        try:
            # Create a sentence with repeated word for better detection
            text_to_check = (text + " ") * 5
            detector = Detector(text_to_check)
            if detector.language.code == "gn":
                votes += 1
        except Exception as e:
            print(f"Polyglot detection error: {e}")

        # TODO: Add one more language detector

        return votes == 2
