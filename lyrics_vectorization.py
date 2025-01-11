from transformers import DistilBertTokenizer, DistilBertModel
import torch
import pandas as pd

class BERTFeatureExtractor():
    """Class to extract token features, using the DistilBERT Tokenizer."""

    def __init__(self, data_path):
        # Data paths
        self.data_dir = data_path
 
        # Load DistilBERT
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = DistilBertModel.from_pretrained('distilbert-base-uncased')

    def load_lyrics(self, data_file : str):
        """Returns a list of responses for the given data path to the txt file.
        
        Parameters:
            data_file : str
                The path to the txt file containing the responses.
        """
        data_f = pd.read_csv(data_file)
        titles = data_f.get('title')
        lyrics = data_f.get('lyrics')
        return titles, lyrics

    def extract_features(self, data_file : str, batch_size : int =8):
        """Returns the extracted features for the specified text file using DistilBERT.
        
        Parameters:
            data_file : str
                The path to the txt file containing to extract its features
            batch_size : str, default 8
                The size of the batch to process the tokens. 
        """
        # Load responses to prompts
        _, lyrics = self.load_lyrics(data_file)

        features = []
        self.model.eval()
        with torch.no_grad():
            for i in range(0, len(lyrics.tolist()), batch_size):
                batch_lyrics = lyrics.tolist()[i:i+batch_size]
                inputs = self.tokenizer(batch_lyrics, padding=True, return_tensors='pt', truncation=True)
                outputs = self.model(**inputs)

                cls_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
                features.extend(cls_embeddings)
            return features
    
    def save_to_csv(self):
        """Saves the extracted features for the learner (0) and native (1) classes into a single csv file
        in the data folder.
        """
        # Extract features
        lyrics_features = self.extract_features(self.data_dir)

        # Combine data and song info
        lyrics_df = pd.DataFrame(lyrics_features)

        lyrics_df.to_csv("vectorized-lyrics.csv", index=False)  # Save to csv

if __name__ == "__main__":
    # Define data path
    DATA_PATH = "full-dataset-with-preprocessing.csv"

    # Create feature extractor
    extractor = BERTFeatureExtractor(DATA_PATH)
    extractor.save_to_csv()
