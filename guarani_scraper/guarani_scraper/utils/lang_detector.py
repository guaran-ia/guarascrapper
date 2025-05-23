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
        # Load the pretrained model
        # self.fasttext_model = fasttext.load_model("lang_model/lid.176.bin")
        
    def is_guarani(self, text):
        votes = 0
        
        # FastText vote
        try:
            lang, _ = self.fasttext_model.predict(text)
            if lang[0] == '__label__gn':
                votes += 1
        except:
            pass

        # Polyglot vote
        try:
            if Detector(text).language.code == 'gn':
                votes += 1
        except:
            pass
        
        # TODO: Add one more language detector
        
        return votes == 2