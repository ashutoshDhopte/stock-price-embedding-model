import numpy as np
from keras import layers, Model #tensorflow.keras is now the standard import
import data

# --- 1. DEFINE THE MODEL ---
# Define the size of your input pattern and desired vector
# Let's say a pattern is 30 data points (e.g., 30 minutes of close prices)
input_size = 30
embedding_size = 128 # The size of your final vector

# Define the Input Layer
input_layer = layers.Input(shape=(input_size,))

# Build the Encoder part (compresses the data)
encoded = layers.Dense(embedding_size, activation='relu')(input_layer)

# Build the Decoder part (tries to reconstruct the data)
decoded = layers.Dense(input_size, activation='sigmoid')(input_layer)

# Create the full Autoencoder Model
autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer='adam', loss='mean_squared_error')


def preprocess_data(data):
    patterns = []
    # Extract only the 'close' price from each tuple
    close_prices = [row[4] for row in data]  # row[4] is 'close'
    for i in range(len(close_prices) - input_size + 1):
        sequence = close_prices[i : i + input_size]
        sequence = np.array(sequence, dtype=np.float32)
        normalized_sequence = sequence - sequence[0]
        patterns.append(normalized_sequence)

    print(f"✅ Preprocessed {len(patterns)} patterns from the data.")
    return np.array(patterns)

def train_data(data):
    print("Starting model training (this might take a while)...")
    autoencoder.fit(
        data,
        data, # The model learns to reconstruct its own input
        epochs=50,
        batch_size=256,
        shuffle=True,
        verbose=1 # Shows progress
    )
    print("✅ Model training complete.")


    # --- 3. EXTRACT AND SAVE THE ENCODER ---
    # This is the final, most important step of this script.
    # You create a new model that only contains the encoder part.
    encoder = Model(input_layer, encoded)

    # Save the encoder to a file. This file is your final product.
    encoder.save('encoder_model.keras')  # Use .keras extension for Keras models
    print("✅ Encoder has been saved to 'encoder_model.keras'.")
    print("You can now use this file in your main application.")


def main():
    """Main function to run the ETL process."""
    conn = None
    ohlcv_data = None
    try:
        conn = data.connect_to_postgres()
        if conn:
            ticker_symbol = 'GOOGL'
            ohlcv_data = data.fetch_ohlcv_data(conn, ticker_symbol)
            process_data = preprocess_data(ohlcv_data)
            train_data(process_data)
    finally:
        if conn:
            conn.close()
            print("PostgreSQL connection closed.")

if __name__ == "__main__":
    main()