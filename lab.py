import random
import pandas

pandas.set_option('display.max_columns', None)


def inv(a, m):  # Обратный к a по модулю m
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Нет обратного')
    else:
        return x % m


def simplify(matrix):
    for row in range(len(matrix)):
        invelem = inv(matrix[row][row], p)
        for col in range(row, len(matrix[row])):
            matrix[row][col] = (matrix[row][col] * invelem) % p
        for other_row in range(row + 1, len(matrix)):
            anchor = matrix[other_row][row]
            for col in range(row, len(matrix[row])):
                matrix[other_row][col] = (anchor * matrix[row][col] * (-1) + matrix[other_row][col]) % p
    return matrix


p = 67  # 56389247275368499
print("p =", p)
m = random.randint(1, p - 1)
print("m =", m)

print("Количество участников: ")  # n
n = int(input())
print("Группа доступа: ")  # k
k = int(input())

Q = [m]
for i in range(k - 1):
    Q.append(random.randint(1, p - 1))
print("Q =", Q)
print()

### Фаза раздачи
D = []
for i in range(n):
    temp = []
    for j in range(k):
        temp.append(random.randint(1, p - 1))
    b = 0
    for j in range(k):
        b += Q[j] * temp[j]
    temp.append(b % p)
    D.append(temp)

col = []  # Заполнение таблицы долей участников
for i in range(k):
    col.append("a" + str(i + 1))
col.append("b")
D1 = pandas.DataFrame(data=D, columns=col, index=[i + 1 for i in range(n)])
print(D1)
print()

### Фаза восстановления
print("Номера участников для восстановления:")
nums = input().split()
members = [int(item) for item in nums]

M = []
for i in members:
    M.append(D[i - 1])
# print(M)

M = simplify(M)  # Приведение к ступенчатому виду
for row in range(len(M)):  # Транспонирование
    middle = (len(M[row]) - 1) // 2
    for col in range(middle):
        t = M[row][col]
        M[row][col] = M[row][len(M[row]) - col - 2]
        M[row][len(M[row]) - col - 2] = t
for row in range(len(M) // 2):
    t = M[row]
    M[row] = M[len(M) - row - 1]
    M[len(M) - row - 1] = t
M = simplify(M)  # И снова приведение к ступенчатому виду
# Получаем систему уравнений, решённую по методу жордана-гаусса по модулю

print(M)
print("Секрет = ", M[-1][-1])

