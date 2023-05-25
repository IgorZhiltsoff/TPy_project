from sys import getsizeof

spam = ['eggs' for i in range(10**6)]

same = True
for i in range(1, len(spam)):
    same &= spam[i - 1] is spam[i]

print(same)
print(getsizeof(spam))
