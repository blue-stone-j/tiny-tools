
'''
Read the values from file, skip zero values if necessary, normalize the data, and then calculate and plot the 
normal distribution parameters.
'''

import numpy as np # for normal distribution fit
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from scipy import stats # for estimating normal distribution fit
from scipy.stats import anderson

def normalize_value(value):
    if value=="-0.000":
        return "0.000"
    else:
        return value

def plot_histogram(values):
    # Plot histogram and normal distribution
    count, bins, ignored = plt.hist(values, bins=30, density=True, alpha=0.6, color='blue')
    # Plot the normal distribution curve
    x = np.linspace(min(values), max(values), 1000)
    plt.plot(x, (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2), color='red')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.title('Histogram and Normal Distribution Fit')
    plt.show()

def plot_QQ(values):
    plt.figure(figsize=(6, 6))
    stats.probplot(values, dist="norm", plot=plt)
    plt.title("Q-Q Plot")
    plt.show()

def plot_frequency(values):
    # Count the occurrences of each unique value
    value_counts = Counter(values)

    x_values = list(value_counts.keys())
    y_counts = list(value_counts.values())

    x = pd.to_numeric(x_values)
    y = pd.to_numeric(y_counts)/len(values)

    # Plot the data
    plt.plot(x, y,label=f'File: {filename}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Frequency of Values')

    x_range=(-0.1,0.1)
    plt.xlim(x_range)

    # Show the plot
    plt.legend()
    plt.grid(True)
    plt.show()

# Read values from a file, skipping the normalized zero value
filename = '../data/1d_data.csv'  # Replace with your actual file name
with open(filename, 'r') as file:
    # Read values, convert to floats, and filter out zero values
    # values = [float(line.strip()) for line in file if float(line.strip()) != 0]
    # Read values, convert to floats
    values = [float(normalize_value(line.strip())) for line in file]

# Calculate mean and standard deviation
mean = np.mean(values)
std_dev = np.std(values)
print(f"Mean (μ): {mean}")
print(f"Standard Deviation (σ): {std_dev}")
print("")

# Calculate skewness and kurtosis
'''
skewness measures the asymmetry of the data distribution. Positive skewness means a longer tail on the right, while 
negative skewness means a longer tail on the left.
'''
skewness = stats.skew(values)
'''
Kurtosis measures the "tailedness" of the data. Normal distribution kurtosis is 3 (or 0 if using excess kurtosis).
Higher kurtosis suggests heavy tails (more extreme outliers), and lower kurtosis indicates light tails.
'''
kurtosis = stats.kurtosis(values)  # Excess kurtosis (normal distribution kurtosis = 0)
print(f"Skewness: {skewness}")
print(f"Kurtosis (Excess): {kurtosis}")
print("")

# Perform Kolmogorov-Smirnov (K-S) test
'''
a nonparametric statistical test used to compare two probability distributions. It is commonly used for two main 
purposes: 1. test whether the distribution of a sample matches a known theoretical distribution, such as a normal or 
exponential distribution. 2. evaluates whether two independent samples are drawn from the same underlying probability 
distribution.
'''
ks_stat, p_value = stats.kstest(values, 'norm', args=(mean, std_dev))
print(f"K-S Test Statistic: {ks_stat}")
print(f"K-S Test p-value: {p_value}")
print("")

# Perform Shapiro-Wilk test
'''
a statistical test used to assess the normality of a data sample. It calculates a W-statistic based on the correlation 
between the observed data and the values expected under normality. 
1. Ranges of W-statistic from 0 to 1, where values close to 1 suggest the data is likely from a normal distribution. 
2. P-value Determines the significance of the test result. A low p-value (commonly < 0.05) indicates that the data 
   significantly deviates from normality, allowing the null hypothesis of normality to be rejected.
key points:
1. Most effective for sample sizes between 3 and 50. 
2. Sensitive to even slight deviations from normality, so it might detect non-normality in large samples even if 
   deviations are minimal.
'''
shapiro_stat, shapiro_p = stats.shapiro(values)
print(f"Shapiro-Wilk Test Statistic: {shapiro_stat}")
print(f"Shapiro-Wilk Test p-value: {shapiro_p}")
print("")

# Perform the Anderson-Darling test for normality
result = anderson(values)
# Display the test statistic
print("Anderson-Darling Statistic:", result.statistic)
# Display critical values and significance levels
for significance_level, critical_value in zip(result.significance_level, result.critical_values):
    if result.statistic > critical_value:
        print(f"At significance level {significance_level}%, reject the null hypothesis: data is not normal")
    else:
        print(f"At significance level {significance_level}%, fail to reject the null hypothesis: data is normal")

# plot histogram
plot_histogram(values)
# Plot Q-Q plot (Quantile-Quantile Plot)
plot_QQ(values)
# plot original frequency
plot_frequency(values)
