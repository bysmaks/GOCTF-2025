from dataclasses import dataclass
from Crypto.Util.number import *
from typing import List, Tuple
from gmpy2 import legendre
import os


@dataclass
class EncryptionParameters:
    modulus_n: int
    public_key_x: int
    encrypted_values: List[int]


class GMInJeans:
    def __init__(self, key_size: int = 2048):
        """
        Args:
            key_size (int): Size of prime numbers in bits
        """
        self.key_size = key_size
        self.prime_p = None
        self.prime_q = None
        self.modulus_n = None
        self.public_key_x = None

    def generate_key_pair(self) -> Tuple[int, int]:
        """
        Returns:
            tuple: (modulus n, public key x)
        """
        self.prime_p, self.prime_q = getPrime(self.key_size), getPrime(self.key_size)
        self.modulus_n = self.prime_p * self.prime_q

        self.public_key_x = getRandomRange(0, self.modulus_n)
        while legendre(self.public_key_x, self.prime_p) != -1 or legendre(self.public_key_x, self.prime_q) != -1:
            self.public_key_x = getRandomRange(0, self.modulus_n)

        return self.modulus_n, self.public_key_x

    def encrypt(self, message: int) -> List[int]:
        """
        Args:
            message (int): Message to encrypt
        
        Returns:
            list: List of encrypted values
        """
        if not self.modulus_n or not self.public_key_x:
            raise ValueError("Keys not generated. Call generate_key_pair() first.")

        random_y = getRandomRange(0, self.modulus_n)
        encrypted_values = []
        
        while message:
            current_bit = message & 1
            message >>= 1
            encrypted_bit = (pow(random_y, 2) * pow(self.public_key_x, current_bit)) % self.modulus_n
            encrypted_values.append(encrypted_bit)
            random_y += getRandomRange(1, 2**48)
        
        return encrypted_values

    def get_encryption_parameters(self) -> EncryptionParameters:
        """
        Returns:
            EncryptionParameters: Current encryption parameters
        """
        if not self.modulus_n or not self.public_key_x:
            raise ValueError("Keys not generated. Call generate_key_pair() first.")
            
        return EncryptionParameters(
            modulus_n=self.modulus_n,
            public_key_x=self.public_key_x,
            encrypted_values=[]
        )


class EncryptionDataWriter:
    def __init__(self, output_file: str):
        """
        Args:
            output_file (str): Path to output file
        """
        self.output_file = output_file

    def save_encryption_data(self, params: EncryptionParameters, encrypted_flag: List[int]):
        """
        Args:
            params (EncryptionParameters): Encryption parameters
            encrypted_flag (list): Encrypted flag values
        """
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        with open(self.output_file, 'w') as output_file:
            output_file.write(f"n = {params.modulus_n}\n")
            output_file.write(f"x = {params.public_key_x}\n")
            output_file.write(f"enc = {encrypted_flag}\n")


def main() -> None:
    FLAG = bytes_to_long(b'goctf{REDACTED}')
    OUTPUT_FILE = './data'

    forbidden_jeans = GMInJeans()
    
    forbidden_jeans.generate_key_pair()
    
    encrypted_flag = forbidden_jeans.encrypt(FLAG)
    
    params = forbidden_jeans.get_encryption_parameters()
    
    writer = EncryptionDataWriter(OUTPUT_FILE)
    writer.save_encryption_data(params, encrypted_flag)

    print(f"Encryption data saved to {OUTPUT_FILE}")
    print(f"Flag: {FLAG}")
    print(f"Encrypted flag: {encrypted_flag}")
    print(f"Encryption parameters: {params}")
    return


if __name__ == "__main__":
    main()
