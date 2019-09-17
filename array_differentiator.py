arr = [2*(x / 10.0) for x in range(0, 10, 1)]

derivatives = []

for i, value in enumerate(arr[:-1]):
    derivatives.append(arr[i+1] - arr[i])
    print(str(arr[i+1]) + " - " + str(arr[i]) + " = " + str(derivatives[i]))

