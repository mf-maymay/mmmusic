def take_x_at_a_time(items, x):
    sequence = list(items)
    quotient, remainder = divmod(len(sequence), x)
    for i in range(quotient + bool(remainder)):
        yield sequence[i * x : (i + 1) * x]
