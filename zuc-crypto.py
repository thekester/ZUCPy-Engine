# ZUC Algorithm Implementation in Python
# This script provides a detailed, step-by-step implementation of the ZUC stream cipher.
# The key and IV are loaded from a .env file for security reasons, and their values are not printed.

import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# S-boxes S0 and S1 as per the ZUC specification
S0 = [
    0x3E,0x72,0x5B,0x47,0xCA,0xE0,0x00,0x33,0x04,0xD1,0x54,0x98,0x09,0xB9,0x6D,0xCB,
    0x7B,0x1B,0xF9,0x32,0xAF,0x9D,0x6A,0xA5,0xB8,0x2D,0xFC,0x1D,0x08,0x53,0x03,0x90,
    0x4D,0x4E,0x84,0x99,0xE4,0xCE,0xD9,0x91,0xDD,0xB6,0x85,0x48,0x8B,0x29,0x6E,0xAC,
    0xCD,0xC1,0xF8,0x1E,0x73,0x43,0x69,0xC6,0xB5,0xBD,0xFD,0x39,0x63,0x20,0xD4,0x38,
    0x76,0x7D,0xB2,0xA7,0xCF,0xED,0x57,0xC5,0xF3,0x2C,0xBB,0x14,0x21,0x06,0x55,0x9B,
    0xE3,0xEF,0x5E,0x31,0x4F,0x7F,0x5A,0xA4,0x0D,0x82,0x51,0x49,0x5F,0xBA,0x58,0x1C,
    0x4A,0x16,0xD5,0x17,0xA8,0x92,0x24,0x1F,0x8C,0xFF,0xD8,0xAE,0x2E,0x01,0xD3,0xAD,
    0x3B,0x4B,0xDA,0x46,0xEB,0xC9,0xDE,0x9A,0x8F,0x87,0xD7,0x3A,0x80,0x6F,0x2F,0xC8,
    0xB1,0xB4,0x37,0xF7,0x0A,0x22,0x13,0x28,0x7C,0xCC,0x3C,0x89,0xC7,0xC3,0x96,0x56,
    0x07,0xBF,0x7E,0xF0,0x0B,0x2B,0x97,0x52,0x35,0x41,0x79,0x61,0xA6,0x4C,0x10,0xFE,
    0xBC,0x26,0x95,0x88,0x8A,0xB0,0xA3,0xFB,0xC0,0x18,0x94,0xF2,0xE1,0xE5,0xE9,0x5D,
    0xD0,0xDC,0x11,0x66,0x64,0x5C,0xEC,0x59,0x42,0x75,0x12,0xF5,0x74,0x9C,0xAA,0x23,
    0x0E,0x86,0xAB,0xBE,0x2A,0x02,0xE7,0x67,0xE6,0x44,0xA2,0x6C,0xC2,0x93,0x9F,0xF1,
    0xF6,0xFA,0x36,0xD2,0x50,0x68,0x9E,0x62,0x71,0x15,0x3D,0xD6,0x40,0xC4,0xE2,0x0F,
    0x8E,0x83,0x77,0x6B,0x25,0x05,0x3F,0x0C,0x30,0xEA,0x70,0xB7,0xA1,0xE8,0xA9,0x65,
    0x8D,0x27,0x1A,0xDB,0x81,0xB3,0xA0,0xF4,0x45,0x7A,0x19,0xDF,0xEE,0x78,0x34,0x60
]

S1 = [
    0x55,0xC2,0x63,0x71,0x3B,0xC8,0x47,0x86,0x9F,0x3C,0xDA,0x5B,0x29,0xAA,0xFD,0x77,
    0x8C,0xC5,0x94,0x0C,0xA6,0x1A,0x13,0x00,0xE3,0xA8,0x16,0x72,0x40,0xF9,0xF8,0x42,
    0x44,0x26,0x68,0x96,0x81,0xD9,0x45,0x3E,0x10,0x76,0xC6,0xA7,0x8B,0x39,0x43,0xE1,
    0x3A,0xB5,0x56,0x2A,0xC0,0x6D,0xB3,0x05,0x22,0x66,0xBF,0xDC,0x0B,0xFA,0x62,0x48,
    0xDD,0x20,0x11,0x06,0x36,0xC9,0xC1,0xCF,0xF6,0x27,0x52,0xBB,0x69,0xF5,0xD4,0x87,
    0x7F,0x84,0x4C,0xD2,0x9C,0x57,0xA4,0xBC,0x4F,0x9A,0xDF,0xFE,0xD6,0x8D,0x7A,0xEB,
    0x2B,0x53,0xD8,0x5C,0xA1,0x14,0x17,0xFB,0x23,0xD5,0x7D,0x30,0x67,0x73,0x08,0x09,
    0xEE,0xB7,0x70,0x3F,0x61,0xB2,0x19,0x8E,0x4E,0xE5,0x4B,0x93,0x8F,0x5D,0xDB,0xA9,
    0xAD,0xF1,0xAE,0x2E,0xCB,0x0D,0xFC,0xF4,0x2D,0x46,0x6E,0x1D,0x97,0xE8,0xD1,0xE9,
    0x4D,0x37,0xA5,0x75,0x5E,0x83,0x9E,0xAB,0x82,0x9D,0xB9,0x1C,0xE0,0xCD,0x49,0x89,
    0x01,0xB6,0xBD,0x58,0x24,0xA2,0x5F,0x38,0x78,0x99,0x15,0x90,0x50,0xB8,0x95,0xE4,
    0xD0,0x91,0xC7,0xCE,0xED,0x0F,0xB4,0x6F,0xA0,0xCC,0xF0,0x02,0x4A,0x79,0xC3,0xDE,
    0xA3,0xEF,0xEA,0x51,0xE6,0x6B,0x18,0xEC,0x1B,0x2C,0x80,0xF7,0x74,0xE7,0xFF,0x21,
    0x5A,0x6A,0x54,0x1E,0x41,0x31,0x92,0x35,0xC4,0x33,0x07,0x0A,0xBA,0x7E,0x0E,0x34,
    0x88,0xB1,0x98,0x7C,0xF3,0x3D,0x60,0x6C,0x7B,0xCA,0xD3,0x1F,0x32,0x65,0x04,0x28,
    0x64,0xBE,0x85,0x9B,0x2F,0x59,0x8A,0xD7,0xB0,0x25,0xAC,0xAF,0x12,0x03,0xE2,0xF2
]

# The constants D (EK_d), used during key initialization
EK_d = [
    0x44D7,0x26BC,0x626B,0x135E,
    0x5789,0x35E2,0x7135,0x09AF,
    0x4D78,0x2F13,0x6BC4,0x1AF1,
    0x5E26,0x3C4D,0x789A,0x47AC
]

class ZUC:
    def __init__(self):
        # Initialize state variables
        
        # Linear Feedback Shift Register (LFSR) state (16 registers, each 31 bits)
        self.LFSR_S = [0] * 16  # LFSR_S[0] to LFSR_S[15]
        
        # F function registers (32 bits each)
        self.F_R1 = 0
        self.F_R2 = 0
        
        # Outputs of the Bit Reorganization process (32 bits each)
        self.BRC_X = [0] * 4  # BRC_X[0] to BRC_X[3]
        
        # S-boxes
        self.S0 = S0
        self.S1 = S1
        
        # Constants D
        self.EK_d = EK_d
        
        # Lists to store states for animation
        self.LFSR_states = []
        self.F_R1_states = []
        self.F_R2_states = []
        self.keystream_words = []
        self.rounds = 0

    # Addition modulo (2^31 - 1)
    def AddM(self, a, b):
        c = a + b
        # Handle carry if any
        result = ((c & 0x7FFFFFFF) + (c >> 31)) & 0x7FFFFFFF
        return result

    # Multiplication by 2^k modulo (2^31 - 1)
    def MulByPow2(self, x, k):
        # Cyclic shift to the left by k bits
        result = ((x << k) | (x >> (31 - k))) & 0x7FFFFFFF
        return result

    # Linear Feedback Shift Register (LFSR) with initialization mode
    def LFSRWithInitialisationMode(self, u):
        # Update the LFSR during initialization using input u
        f = self.LFSR_S[0]
        # Perform computations as per the specification
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[0], 8))
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[4], 20))
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[10], 21))
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[13], 17))
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[15], 15))
        f = self.AddM(f, u)
        # Shift the LFSR state
        for i in range(15):
            self.LFSR_S[i] = self.LFSR_S[i + 1]
        self.LFSR_S[15] = f
        # Ensure non-zero state
        if self.LFSR_S[15] == 0:
            self.LFSR_S[15] = 0x7FFFFFFF

    # LFSR with work mode (used during keystream generation)
    def LFSRWithWorkMode(self):
        # Update the LFSR during keystream generation without input u
        f = self.LFSR_S[0]
        # Perform computations as per the specification
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[0], 8))
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[4], 20))
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[10], 21))
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[13], 17))
        f = self.AddM(f, self.MulByPow2(self.LFSR_S[15], 15))
        # Shift the LFSR state
        for i in range(15):
            self.LFSR_S[i] = self.LFSR_S[i + 1]
        self.LFSR_S[15] = f
        # Ensure non-zero state
        if self.LFSR_S[15] == 0:
            self.LFSR_S[15] = 0x7FFFFFFF

    # Bit Reorganization
    def BitReorganization(self):
        # Rearrange bits from LFSR registers to form new words
        self.BRC_X[0] = (((self.LFSR_S[15] & 0x7FFF8000) << 1) & 0xFFFFFFFF) | (self.LFSR_S[14] & 0xFFFF)
        self.BRC_X[1] = (((self.LFSR_S[11] & 0xFFFF) << 16) & 0xFFFFFFFF) | ((self.LFSR_S[9] >> 15) & 0xFFFF)
        self.BRC_X[2] = (((self.LFSR_S[7] & 0xFFFF) << 16) & 0xFFFFFFFF) | ((self.LFSR_S[5] >> 15) & 0xFFFF)
        self.BRC_X[3] = (((self.LFSR_S[2] & 0xFFFF) << 16) & 0xFFFFFFFF) | ((self.LFSR_S[0] >> 15) & 0xFFFF)

    # Rotate left operation (circular left shift)
    def ROT(self, x, k):
        return ((x << k) | (x >> (32 - k))) & 0xFFFFFFFF

    # Linear transformation L1
    def L1(self, X):
        # Apply linear transformation to mix bits
        result = X ^ self.ROT(X, 2) ^ self.ROT(X, 10) ^ self.ROT(X, 18) ^ self.ROT(X, 24)
        return result

    # Linear transformation L2
    def L2(self, X):
        result = X ^ self.ROT(X, 8) ^ self.ROT(X, 14) ^ self.ROT(X, 22) ^ self.ROT(X, 30)
        return result

    # Combine bytes into a 32-bit word
    def MAKEU32(self, a, b, c, d):
        result = ((a << 24) | (b << 16) | (c << 8) | d) & 0xFFFFFFFF
        return result

    # Nonlinear function F
    def F(self):
        # Introduce nonlinearity to enhance security
        W = (self.BRC_X[0] ^ self.F_R1) + self.F_R2
        W = W & 0xFFFFFFFF  # Ensure 32-bit word
        W1 = (self.F_R1 + self.BRC_X[1]) & 0xFFFFFFFF
        W2 = self.F_R2 ^ self.BRC_X[2]
        # Apply linear transformations L1 and L2
        u = self.L1(((W1 << 16) & 0xFFFFFFFF) | ((W2 >> 16) & 0xFFFF))
        v = self.L2(((W2 << 16) & 0xFFFFFFFF) | ((W1 >> 16) & 0xFFFF))
        # S-box substitution
        u_bytes = [(u >> 24) & 0xFF, (u >> 16) & 0xFF, (u >> 8) & 0xFF, u & 0xFF]
        v_bytes = [(v >> 24) & 0xFF, (v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF]
        self.F_R1 = self.MAKEU32(
            self.S0[u_bytes[0]], self.S1[u_bytes[1]],
            self.S0[u_bytes[2]], self.S1[u_bytes[3]]
        )
        self.F_R2 = self.MAKEU32(
            self.S0[v_bytes[0]], self.S1[v_bytes[1]],
            self.S0[v_bytes[2]], self.S1[v_bytes[3]]
        )
        # Store states for animation
        self.F_R1_states.append(self.F_R1)
        self.F_R2_states.append(self.F_R2)
        return W

    # Combine bytes into a 31-bit word (used in key loading)
    def MAKEU31(self, a, b, c):
        result = ((a << 23) | (b << 8) | c) & 0x7FFFFFFF
        return result

    # Display the history of the ZUC algorithm
    def display_zuc_history(self):
        print("=== History of the ZUC Algorithm ===")
        print("ZUC is a stream cipher algorithm designed for mobile communications.")
        print("It was developed by the Data Assurance and Communication Security Research Center at the Chinese Academy of Sciences.")
        print("ZUC is used in the 3GPP LTE (Long Term Evolution) standards for 4G mobile communication.")
        print("It is valued for its simplicity, efficiency, and high level of security.\n")

    # Initialization with key and IV
    def Initialization(self, k, iv):
        print("=== Initialization of the ZUC Algorithm ===")
        print("The initialization phase sets up the internal state using the secret key and initialization vector (IV).")
        print("This ensures that the keystream generated is unique for this key and IV combination.\n")
        # Initialize the LFSR with the key and IV
        for i in range(16):
            # Use lower 15 bits of EK_d[i]
            d = self.EK_d[i] & 0x7FFF
            self.LFSR_S[i] = self.MAKEU31(k[i], d, iv[i])
            print(f"Initializing LFSR_S[{i}] with the key byte, constant D, and IV byte.")
        # Set F_R1 and F_R2 to zero
        self.F_R1 = 0
        self.F_R2 = 0
        print("\nF_R1 and F_R2 registers are initialized to zero.\n")
        # Run initialization steps
        for n in range(32):
            print(f"--- Initialization Round {n + 1} ---")
            print("1. Performing bit reorganization to prepare input for the nonlinear function.")
            self.BitReorganization()
            print("2. Applying the nonlinear function F to update the internal state.")
            w = self.F()
            u = (w >> 1) & 0x7FFFFFFF  # Remove the rightmost bit
            print("3. Updating the LFSR in initialization mode with the output of F.")
            self.LFSRWithInitialisationMode(u)
            # Store LFSR state for animation
            self.LFSR_states.append(self.LFSR_S.copy())
            print("\n")

    # Keystream generation
    def GenerateKeystream(self, KeystreamLen):
        print("=== Keystream Generation ===")
        print("The keystream is a sequence of bits used in stream ciphers to encrypt or decrypt data.")
        print("Each keystream word is generated based on the internal state, ensuring security.\n")
        keystream = []
        # Discard the first output
        print("Before generating the keystream, we perform a preparation step by discarding the first output.")
        self.BitReorganization()
        self.F()  # Discard the output
        self.LFSRWithWorkMode()
        print("Preparation completed. Starting keystream generation.\n")
        # Store LFSR state for animation
        self.LFSR_states.append(self.LFSR_S.copy())
        # Generate keystream words
        for i in range(KeystreamLen):
            print(f"--- Generating Keystream Word {i + 1} ---")
            print("1. Performing bit reorganization to prepare input for the nonlinear function.")
            self.BitReorganization()
            print("2. Applying the nonlinear function F to produce intermediate values.")
            z = (self.F() ^ self.BRC_X[3]) & 0xFFFFFFFF
            print(f"3. Combining the output of F with BRC_X[3] to produce the keystream word: {z:08X}")
            keystream.append(z)
            self.keystream_words.append(z)
            print("4. Updating the LFSR in work mode for the next iteration.\n")
            self.LFSRWithWorkMode()
            # Store LFSR state for animation
            self.LFSR_states.append(self.LFSR_S.copy())
        return keystream

    # Function to animate LFSR states
    def animate_lfsr(self):
        # Prepare data for animation
        fig, ax = plt.subplots()
        ax.set_title('LFSR State Over Time')
        ax.set_xlabel('Register Index')
        ax.set_ylabel('Value (Hex)')
        line, = ax.plot([], [], 'bo-')
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 0x7FFFFFFF)
        def init():
            line.set_data([], [])
            return line,
        def update(frame):
            x = list(range(16))
            y = self.LFSR_states[frame]
            line.set_data(x, y)
            ax.set_title(f'LFSR State at Round {frame}')
            return line,
        ani = animation.FuncAnimation(fig, update, frames=len(self.LFSR_states),
                                      init_func=init, blit=True, interval=500, repeat=False)
        plt.show()

    # Function to animate F_R1 and F_R2
    def animate_f_registers(self):
        # Prepare data for animation
        fig, ax = plt.subplots()
        ax.set_title('F Function Registers Over Time')
        ax.set_xlabel('Round')
        ax.set_ylabel('Value (Hex)')
        rounds = list(range(len(self.F_R1_states)))
        line1, = ax.plot([], [], 'r-', label='F_R1')
        line2, = ax.plot([], [], 'g-', label='F_R2')
        ax.set_xlim(0, len(self.F_R1_states))
        ax.set_ylim(0, 0xFFFFFFFF)
        ax.legend()
        def init():
            line1.set_data([], [])
            line2.set_data([], [])
            return line1, line2
        def update(frame):
            x = rounds[:frame]
            y1 = self.F_R1_states[:frame]
            y2 = self.F_R2_states[:frame]
            line1.set_data(x, y1)
            line2.set_data(x, y2)
            ax.set_title(f'F Function Registers at Round {frame}')
            return line1, line2
        ani = animation.FuncAnimation(fig, update, frames=len(rounds),
                                      init_func=init, blit=True, interval=500, repeat=False)
        plt.show()

def main():
    # Load the key and IV from the .env file
    key_str = os.getenv('KEY')
    iv_str = os.getenv('IV')

    if not key_str or not iv_str:
        print("Error: The KEY and IV variables are not defined in the .env file.")
        sys.exit(1)

    # Convert the strings into lists of integers
    key_bytes = [int(byte, 16) for byte in key_str.split(',')]
    iv_bytes = [int(byte, 16) for byte in iv_str.split(',')]

    if len(key_bytes) != 16 or len(iv_bytes) != 16:
        print("Error: The key and IV must each contain exactly 16 bytes.")
        sys.exit(1)

    print("The key and IV have been successfully loaded from the .env file.\n")

    print("Starting the ZUC algorithm...\n")

    # Initialize ZUC with the key and IV
    zuc = ZUC()
    zuc.display_zuc_history()
    zuc.Initialization(key_bytes, iv_bytes)

    # Generate keystream of desired length (number of 32-bit words)
    keystream_length = 5  # For example, generate 5 words for demonstration
    print(f"Generating a keystream of {keystream_length} words.\n")
    keystream = zuc.GenerateKeystream(keystream_length)

    # Print the keystream
    print("=== Final Keystream ===")
    for i, word in enumerate(keystream):
        print(f"Word {i + 1}: {word:08X}")

    print("\nZUC algorithm execution completed.")

    # Animate LFSR states
    print("\nAnimating LFSR internal states over time...")
    zuc.animate_lfsr()

    # Animate F function registers
    print("\nAnimating F function registers over time...")
    zuc.animate_f_registers()

if __name__ == "__main__":
    main()
