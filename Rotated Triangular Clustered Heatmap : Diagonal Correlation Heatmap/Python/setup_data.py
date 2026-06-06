import numpy as np
import pandas as pd
import os

# Set seed for reproducibility
np.random.seed(42)

# Generate data like in MATLAB
X = np.random.randn(20, 20)

# Linspace arrays
l1 = np.linspace(-1, 2.5, 20).reshape(-1, 1)
l2 = np.linspace(0.5, -0.7, 20).reshape(-1, 1)
l3 = np.linspace(0.9, -0.2, 20).reshape(-1, 1)

# Concatenate arrays
part1 = np.tile(l1, (1, 8))
part2 = np.tile(l2, (1, 5))
part3 = np.tile(l3, (1, 7))

X_add = np.hstack([part1, part2, part3])
X = X + X_add

# Compute correlation matrix
Data = np.corrcoef(X.T)

# Alternatively, in MATLAB `corr(X)` computes correlation of columns,
# meaning it treats rows as observations and columns as variables.
# Wait! MATLAB `corr(X)` correlates the columns of X.
# np.corrcoef(X.T) computes correlation of the columns of X.
# Let's verify MATLAB corr(X) behavior: yes, it returns 20x20.

columns = [f"Sl-{i+1}" for i in range(20)]
df = pd.DataFrame(Data, columns=columns, index=columns)

# Save to csv
df.to_csv('data.csv')
