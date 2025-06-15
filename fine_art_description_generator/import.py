import numpy as np

# Example array (replace this with your real data)
your_array = np.array([1, 2, np.nan, np.inf])

print(np.isnan(your_array).any())  # True if NaNs present
print(np.isinf(your_array).any())  # True if infs present
