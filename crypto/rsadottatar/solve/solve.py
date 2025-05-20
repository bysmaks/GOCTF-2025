from Crypto.Util.number import *
from typing import Tuple, List


class RabinSolver:
    """
    A class to solve Rabin cryptosystem challenges.
    The Rabin cryptosystem is an asymmetric cryptographic technique based on the difficulty
    of finding square roots modulo a composite number.
    """
    
    def __init__(self, c: int, p: int, q: int):
        """
        Initialize the Rabin solver with the given parameters.
        
        Args:
            c (int): Encrypted message
            p (int): First prime factor (must be congruent to 3 mod 4)
            q (int): Second prime factor (must be congruent to 3 mod 4)
        """
        self.c = c
        self.p = p
        self.q = q
        self.n = p * q
        
    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean Algorithm implementation.
        
        Args:
            a (int): First number
            b (int): Second number
            
        Returns:
            Tuple[int, int, int]: GCD and Bezout coefficients
        """
        if a == 0:
            return (b, 0, 1)
        g, y, x = RabinSolver.extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

    def solve_rabin(self) -> List[bytes]:
        """
        Solve the Rabin cryptosystem challenge using Chinese Remainder Theorem.
        For Rabin, we need to find square roots modulo p and q, then combine them.
        
        Returns:
            List[bytes]: List of possible decrypted messages
        """
        # Calculate CRT components
        g, yp, yq = self.extended_gcd(self.p, self.q)
        
        # Calculate square roots modulo p and q
        # For Rabin, we use ((p+1)/4) and ((q+1)/4) as exponents
        # This works because p and q are both ≡ 3 (mod 4)
        # 10 is the number of times to raise the exp to the power of 10 because e=2^10
        mp = pow(self.c, ((self.p + 1) // 4) ** 10, self.p)
        mq = pow(self.c, ((self.q + 1) // 4) ** 10, self.q)
        
        # Calculate all four possible solutions using CRT
        r = (yp * self.p * mq + yq * self.q * mp) % self.n
        mr = self.n - r
        s = (yp * self.p * mq - yq * self.q * mp) % self.n
        ms = self.n - s
        
        # Convert all possible solutions to bytes
        return [long_to_bytes(num) for num in [r, mr, s, ms]]

def main():
    # Rabin parameters
    c = 2163983051571600180887664142073165011661701734356076308381978740348051087726166829962880363784974133366413692462650897736482699069984141582012933511766737235773594789687018235731162803454027658521584467943414507497920761773422445338043694802866434441335378775655817366048615054040814410576051215405199816659641622780109903556184874596928631200181998450796139229660746729077464857949153740674488064133834094954385941604080256530165071916197667525458878853968816783990455451847855696190863381135057254268013393478065873502843880457772893548145290919829927325695063817891940417513397407701653262384095441708372173788385
    p = 110802163407718558547289645847194196648240351561019504600522273900318614715081581618809334088733792051742762747671854183709511444724801399385984067020256747509792881327833573422929988567467250643869483680333148450034614093004122945277059385922777328778702048272718895705532702635399255398344640277812175763923
    q = 116114469856211228102888596552510365775195615275659911240392034017703877153126490675186710201637327688278865179850832492881008310190972426083755857670836100201210728680837138739001567995201936855404157580184979868108556335034685758905443392982750834587801692587494909689049362627292813543937249455110292053011

    # Create solver instance and solve
    solver = RabinSolver(c, p, q)
    solutions = solver.solve_rabin()
    
    # Print all possible solutions
    for i, solution in enumerate(solutions, 1):
        print(f"Solution {i}: {solution}")

if __name__ == "__main__":
    main()
