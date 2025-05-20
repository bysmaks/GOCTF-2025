from Crypto.Util.number import *
from tqdm import tqdm
from sage.all import *
from typing import List, Tuple, Optional, Any


class GoldwasserMicaliSolver:
    def __init__(self, n: int, x: int, enc: List[int]) -> None:
        self.n: Integer = Integer(n)
        self.x: Integer = Integer(x)
        self.enc: List[Integer] = [Integer(c) for c in enc]
        self.k: Optional[Integer] = None
        self.y: Optional[Integer] = None
        
    def resultant(self, f1: Any, f2: Any, var: Any) -> Any:
        return Matrix(f1.sylvester_matrix(f2, var)).determinant()
    
    def pgcd(self, g1: Any, g2: Any) -> Any:
        return g1.monic() if not g2 else self.pgcd(g2, g1 % g2)
    
    def find_k(self) -> Integer:
        P = PolynomialRing(Zmod(self.n), ['y', 'k'])
        y, k = P.gens()
        
        p1 = self.x * y^2 - self.enc[0]
        p2 = (y + k)^2 - self.enc[1]
        p3 = self.resultant(p1, p2, y)
        
        p3_uni = p3.univariate_polynomial()
        roots = p3_uni.monic().small_roots()
        if not roots:
            raise ValueError("No small roots found for k")
        return roots[0]
    
    def find_y(self) -> Integer:
        P = PolynomialRing(Zmod(self.n), ['y'])
        y = P.gen()
        
        p1 = self.x * y^2 - self.enc[0]
        p2 = (y + self.k)^2 - self.enc[1]
        p4 = self.pgcd(p1, p2)
        
        if not p4.coefficients():
            raise ValueError("No coefficients found in GCD")
        return self.n - p4.coefficients()[0]
    
    def decrypt(self) -> bytes:
        self.k = self.find_k()
        self.y = self.find_y()
        
        flag: int = 0
        P = PolynomialRing(Zmod(self.n), ['k'])
        k = P.gen()
        
        for c in tqdm(self.enc[::-1]):
            flag <<= 1
            poly = self.x * (self.y + k)^2 - c
            roots = poly.monic().small_roots()
            if roots:
                flag += 1
                
        return long_to_bytes(flag)


def load_data() -> Tuple[int, int, List[int]]:
    with open('data', 'r') as f:
        data = f.read()
    
    namespace: dict = {}
    exec(data, namespace)
    
    n: Optional[int] = namespace.get('n')
    x: Optional[int] = namespace.get('x')
    enc: Optional[List[int]] = namespace.get('enc')
    
    if not all(var is not None for var in [n, x, enc]):
        raise ValueError("Required variables n, x, and enc not found in data file")
    
    return n, x, enc


def main() -> None:
    n, x, enc = load_data()
    solver = GoldwasserMicaliSolver(n, x, enc)
    flag = solver.decrypt()
    print(f"Decrypted flag: {flag}")
    return


if __name__ == "__main__":
    main()
