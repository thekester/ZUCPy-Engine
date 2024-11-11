# ZUC Algorithm Implementation in Python

This script provides a detailed, step-by-step implementation of the ZUC stream cipher in Python. It loads the encryption key and initialization vector (IV) from a `.env` file for security reasons, and implements the ZUC cipher as used in mobile communication security.

## Dependencies Installation
To run the script, install the required packages by running:

```sh
pip install python-dotenv matplotlib numpy
```

Environment File Setup

Create a .env file in the same directory as your script, and include the following variables:

```txt
KEY=1F,3C,5A,7E,9D,BB,DF,F1,23,45,67,89,AB,CD,EF,01
IV=FE,DC,BA,98,76,54,32,10,0F,1E,2D,3C,4B,5A,69,78
```

# ZUC Algorithm Implementation in Python (Continued)

## Key Components of the ZUC Algorithm

The ZUC algorithm is composed of several key components that work together to generate a secure keystream for encryption purposes. Below, we provide an overview of the main components:

### 1. Linear Feedback Shift Register (LFSR)
The LFSR is the core of the ZUC algorithm. It consists of 16 registers, each containing 31 bits. The LFSR uses a series of feedback taps and modulo operations to generate pseudo-random output bits. These registers are initialized using the key and IV, and they play a significant role in maintaining the internal state of the cipher.

- The LFSR is responsible for updating its state with each round of the algorithm.
- It generates new pseudo-random bits based on the current state and feedback functions.

### 2. Bit Reorganization
The bit reorganization step takes specific bits from the LFSR registers and combines them to produce four 32-bit words. These words are used as input for the F function and help to ensure that the internal state of the algorithm is mixed in a non-linear manner.

### 3. Non-linear F Function
The F function introduces non-linearity into the ZUC algorithm, making it more resistant to attacks such as linear cryptanalysis. The F function uses two internal registers (R1 and R2), which are updated at each round.

- **S-Boxes**: The F function utilizes two S-boxes (S0 and S1), which perform byte substitution operations to enhance the complexity of the output.
- **Linear Transformation**: The F function also applies linear transformations to ensure the output is a complex function of the input bits.

### 4. Keystream Generation
After the initialization phase, the ZUC algorithm enters the keystream generation phase. In this phase, the algorithm generates 32-bit words, which are used as the keystream for encryption or decryption.

- The keystream is XORed with the plaintext to produce ciphertext during encryption.
- During decryption, the same keystream is XORed with the ciphertext to retrieve the original plaintext.

## Running the Script
To run the ZUC algorithm script, follow these steps:

1. **Prepare the Environment**: Ensure that the `.env` file is properly set up with the key and IV values as described earlier.
2. **Run the Python Script**: Execute the script in your Python environment. The script will initialize the ZUC algorithm, generate a keystream, and optionally visualize the internal states using `matplotlib`.

```sh
python zuc-crypto.py
```

## Visualize the States (Optional)
The script includes an option to visualize the evolution of the LFSR and F function registers. This is helpful for understanding how the internal state changes over time and for educational purposes.

## Important Considerations
- **Security**: The key and IV should be kept secure at all times. Avoid hardcoding these values directly in the script.
- **Performance**: The ZUC algorithm is designed to be efficient for hardware and software implementations, making it suitable for mobile communication standards such as LTE.

## Additional Resources
- For more in-depth information on the ZUC algorithm, you can refer to my tutorial  [ZUC Algorithm Overview](https://pnsrt.tavenel.fr/matieres/crypto/zuc.html).
- For a practical understanding, consider experimenting with different keys and IVs to see how the keystream changes.