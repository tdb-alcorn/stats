def sample(label_to_probability_map, sample_size):
    m = label_to_probability_map
    keys = list(label_to_probability_map.keys())
    probabilities = [m[k] for k in keys]
    samples = sample_multinomial(probabilities, sample_size)
    return [keys[i] for i in samples]


def sample_multinomial(probabilities_array, sample_size):
    p = probabilities_array
    n = sample_size
    total = sum(p)
    p = [prob/total for prob in p]
    p_idx = sorted(range(len(p)), key=lambda i: p[i])
    p_sorted = [p[i] for i in p_idx]
    p_sum = [sum(p_sorted[:(i+1)]) for i in range(len(p_sorted))]
    def label(s):
        idx = binary_search(p_sum, s)
        return p_idx[idx]
    raw_samples = numpy.random.uniform(low=0, high=p_sum[-1], size=n)
    samples = [label(s) for s in raw_samples]
    return samples


def count(array):
    counts = dict()
    for x in array:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


def binary_search(array, value):
    l = len(array)
    if l == 0:
        return 0
    middle = int(l)//2
    left_sub_array = array[:middle]
    right_sub_array = array[middle+1:]
    if value == array[middle]:
        return middle
    elif value > array[middle]:
        return binary_search(right_sub_array, value) + middle + 1
    else:  # value < array[middle]
        return binary_search(left_sub_array, value)


def dict_sub(dict1, dict2):
    '''
    Returns {key: dict1[key]-dict2[key]} for each key where default value
    is dict_i[key] = 0 if a dict does not contain key.
    '''
    result = dict()
    keys = set(dict1.keys()).union(set(dict2.keys()))
    for k in keys:
        value1 = dict1[k] if k in dict1 else 0
        value2 = dict2[k] if k in dict2 else 0
        result[k] = value1 - value2
    return result


def dict_divide(dictionary, divisor):
    d = dictionary
    c = divisor
    result = dict([(k, d[k]/c) for k in d])
    return result


# test sample
ltp = {'cat': 0.1, 'dog': 0.5, 'herp': 0.3, 'derp': 0.1}
print('Testing #sample()...')
print('Result should be very close to ' + str(ltp))
print(count(sample(ltp, 10000)))

# test sample_multinomial
print('Testing #sample()...')
n = 10000
x = sample_multinomial([0.1, 0.2, 0.4, 0.3], n)
counts = count(x)
for key in counts:
    counts[key] /= n
print('Result should be very close to ' + str({0: 0.1, 1: 0.2, 2: 0.4, 3: 0.3}))
print(counts)

# test binary_search
print('Testing #binary_search()...')
print(binary_search([1,2,3,5], 4) == 3)
print(binary_search([0.1, 0.2, 0.4, 0.9, 1], 0.3) == 2)
for i in range(10):
    print(binary_search(range(10), i+0.5) == i + 1)

# test count
import random
print('Testing #count()...')
arr = [1,2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,6,6]
random.shuffle(arr)

# test dict_sub
print('Testing #dict_sub()...')
d1 = {'cat': 0.1, 'dog': 0.5, 'herp': 0.2, 'derp': 0.1}
d2 = {'dog': 0.2, 'herp': 0.1, 'burp': 0.2}
print(dict_sub(d1, d2) == {'dog': 0.3, 'cat': 0.1, 'herp': 0.1, 'derp': 0.1, 'burp': -0.2})

# test dict_divide
print('Testing #dict_divide()...')
d3 = {'a': 10, 'b': 5, 'c': 3242.4}
print(dict_divide(d3, 2))
print(count(arr) == {i: i for i in range(1,7)})
