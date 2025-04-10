import numpy as np
import matplotlib.pyplot as plt
import mplcursors  # Library for interactive annotations

# Constants for Shanghai (2023)
MIN_SALARY = 4000          # Minimum salary in Shanghai (CNY)2690
MIN_SOCIAL_INSURANCE_BASE = 6520    # Minimum social insurance base (CNY)
MAX_SOCIAL_INSURANCE_BASE = 34188   # Maximum social insurance base (CNY)

SHANGHAI_SOCIAL_INSURANCE_RATES = {
    'pension': 0.08,        # Employee contribution
    'medical': 0.02,       # Employee contribution
    'unemployment': 0.005, # Employee contribution
    'housing_fund': 0.07,  # Employee contribution (Shanghai housing fund)
}

EMPLOYER_SOCIAL_INSURANCE_RATES = {
    'pension': 0.16,       # Employer contribution
    'medical': 0.095,      # Employer contribution
    'unemployment': 0.005, # Employer contribution
    'work_injury': 0.0026, # Employer contribution
    'maternity': 0.01,     # Employer contribution
    'housing_fund': 0.07,  # Employer contribution (Shanghai housing fund)
}

# Individual Income Tax (IIT) brackets for China (2023)
IIT_BRACKETS = [
    (0, 3000, 0.03, 0),
    (3000, 12000, 0.10, 210),
    (12000, 25000, 0.20, 1410),
    (25000, 35000, 0.25, 2660),
    (35000, 55000, 0.30, 4410),
    (55000, 80000, 0.35, 7160),
    (80000, float('inf'), 0.45, 15160),
]

# Function to calculate individual income tax
def calculate_iit(salary):
    """
    Calculate individual income tax based on Chinese tax brackets.
    """
    for bracket in IIT_BRACKETS:
        lower, upper, rate, deduction = bracket
        if lower <= salary <= upper:
            return salary * rate - deduction
    return 0

# Function to calculate social insurance base
def get_social_insurance_base(salary):
    """
    Determine the social insurance base based on salary.
    """
    if salary < MIN_SOCIAL_INSURANCE_BASE:
        return MIN_SOCIAL_INSURANCE_BASE
    elif salary > MAX_SOCIAL_INSURANCE_BASE:
        return MAX_SOCIAL_INSURANCE_BASE
    else:
        return salary

# Function to calculate employee social insurance contributions
def calculate_employee_social_insurance(salary):
    """
    Calculate employee's social insurance contributions.
    """
    base = get_social_insurance_base(salary)
    total = 0
    for key, rate in SHANGHAI_SOCIAL_INSURANCE_RATES.items():
        total += base * rate
    return total

# Function to calculate employer's social insurance contributions
def calculate_employer_social_insurance(salary):
    """
    Calculate employer's social insurance contributions.
    """
    base = get_social_insurance_base(salary)
    total = 0
    for key, rate in EMPLOYER_SOCIAL_INSURANCE_RATES.items():
        total += base * rate
    return total

# Function to calculate taxed salary
def calculate_taxed_salary(salary):
    """
    Calculate taxed salary (net salary after deductions).
    """
    social_insurance = calculate_employee_social_insurance(salary)
    taxable_income = salary - social_insurance
    if taxable_income<5000:
        iit=0
    else:
        iit = calculate_iit(taxable_income-5000)
    taxed_salary = salary - social_insurance - iit
    return taxed_salary

# Function to calculate employee cost
def calculate_employee_cost(salary):
    """
    Calculate total employee cost (gross salary + employer contributions).
    """
    employer_contributions = calculate_employer_social_insurance(salary)
    return salary + employer_contributions

# Generate salary range starting from the minimum salary
salaries = np.arange(MIN_SALARY, 100000, 1)  # From 2,690 to 100,000 CNY in steps of 100

# Calculate taxed salaries and employee costs
taxed_salaries = [calculate_taxed_salary(s) for s in salaries]
employee_costs = [calculate_employee_cost(s) for s in salaries]

# Plot the two curves
plt.figure(figsize=(10, 6))
plt.plot(salaries, taxed_salaries, label='Taxed Salary (Net Salary)', color='blue')
plt.plot(salaries, employee_costs, label='Employee Cost (Gross Salary + Employer Contributions)', color='green')
plt.title('Taxed Salary vs Employee Cost in Shanghai (2023)', fontsize=14)
plt.xlabel('Gross Salary (CNY)', fontsize=12)
plt.ylabel('Amount (CNY)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# Set x-axis to logarithmic scale
plt.xscale('log')

# Add hover functionality using mplcursors
cursor = mplcursors.cursor(hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(
    f"Salary: {sel.target[0]:.2f} CNY\nValue: {sel.target[1]:.2f} CNY"
))

plt.show()
