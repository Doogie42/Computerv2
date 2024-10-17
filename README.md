# Computorv2

Computor v2 is a simple bc like calulator that will solve simple arithmetic, polynomial, quadratic equations and matrix operations.
For the moment it only supports:
- addition, subtraction, multiplication and division of numbers.
- rational powers of rational and imaginary numbers with a right to left precedence(2 ^ 3 ^ 4 = 2 ^ (3 ^ 4)).
- parenthesis.
- variable assignement
## Usage
```
python main.py
```

## Examples
```
cv2> (8 * 3) + 2 / 4 - 1 
23.5
cv2> (5.2 * 6) * i / (2 * i - 2) * 15
117 -117 * i
cv2> 2 ^ 3 ^ 4
2.41785e+24
cv2> (2 ^ 3) ^ 4
4096
cv2> (2 +i) ^ 3 ^ 4
2.01274e+28 -2.91147e+27 * i

cv2> school = 21 + 21
42
cv2> age = 12i + 12i
24 * i
cv2> listvariable
school = 42
age = 24 * i
```

## Tests
```
python -m unittest
```