import itertools
from tqdm import tqdm


def isPrime(n):
    if not n & 1 and n != 2:
        return (False, 2)
    end = int((n**0.5) + 1)
    for i in range(3, end, 2):
        if n % i == 0:
            return (False, i)
    return True


digits = "1234567890"
count = sum(1 for _ in itertools.permutations(digits))
pbar = tqdm(
    itertools.permutations(digits),
    ncols=100,
    total=int(count),
    # unit_scale=True,
    bar_format="{percentage:3.0f}%| {desc} | {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]{postfix}",
)
divisor = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
for i in pbar:
    k = int("".join(i))
    pbar.set_description_str(f"{k}")
    b, d = isPrime(k)
    if b:
        pbar.write(f"{k}")
        # break
    else:
        divisor[d] += 1

print(divisor)
