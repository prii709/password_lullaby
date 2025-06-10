# model/utils.py

import yaml
import numpy as np

def load_config(config_path="model/model_config.yaml"):
    """
    Loads a model or training configuration from a YAML file.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        print(f"Warning: Config file {config_path} not found. Using default config.")
        return None
    except Exception as e:
        print(f"Error loading config from {config_path}: {e}")
        return None

def preprocess_input_text(text, max_length=100, embedding_dim=64):
    """
    Placeholder for preprocessing input text into a numerical format for the model.
    This might involve tokenization, padding, and embedding.
    """
    print(f"Preprocessing text: '{text}' (placeholder)")
    # Simple character-level embedding (example)
    # In a real scenario, use pre-trained embeddings or a learned embedding layer.
    vectors = []
    for char_code in [ord(c) for c in text[:max_length]]:
        # Create a simple vector based on char_code (highly naive)
        vec = np.random.rand(embedding_dim) # Replace with actual embedding lookup
        vec[0] = char_code / 255.0 # Just an example to make it somewhat dependent on char_code
        vectors.append(vec)

    # Pad sequences to max_length
    while len(vectors) < max_length:
        vectors.append(np.zeros(embedding_dim)) # Padding with zeros

    if not vectors: # Handle empty text case
        return np.zeros((1, max_length, embedding_dim))

    # Stacking and ensuring correct dimensions for a batch of 1
    processed_input = np.array(vectors).reshape(1, max_length, embedding_dim)
    print(f"Processed input shape: {processed_input.shape}")
    return processed_input


def load_training_data(data_path):
    """
    Placeholder for loading training data for the model.
    This would depend heavily on the nature of the data (e.g., audio files, MIDI, text).
    """
    print(f"Loading training data from {data_path} (placeholder)...")
    # Example:
    # X_train, y_train = [], []
    # Load your data here
    # For now, return dummy data
    num_samples = 100
    input_features = 128 # Should match model's expected input
    output_features = 256 # Should match model's expected output (if supervised)

    # Dummy input data (e.g., noise for a GAN generator)
    X_train = np.random.rand(num_samples, input_features)

    # Dummy output data (e.g., "real" audio features for a GAN discriminator)
    # Or, if it's for training the generator part of a GAN, this might not be directly used in this format.
    y_train = np.random.rand(num_samples, output_features)

    print(f"Dummy training data generated: X_train shape {X_train.shape}, y_train shape {y_train.shape}")
    return X_train, y_train


print("model.utils module loaded")
