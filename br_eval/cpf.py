import re
from .exceptions.cpf_exceptions import (
    CPFError,
    InvalidCPFError,
    RepeatedDigitsCPFError,
    InvalidFormatCPFError,
    InvalidLengthCPFError
)


def format_cpf(cpf):
    """
    Formats a CPF string in the pattern XXX.XXX.XXX-XX.
    
    Args:
        cpf (str): The CPF string with exactly 11 digits.
    
    Returns:
        str: The formatted CPF string.
    
    Raises:
        ValueError: If the CPF does not have exactly 11 digits.
    """
    # Remove all non-digit characters from the CPF
    cpf_numbers = re.sub(r'\D', '', cpf)
    
    # Verify if the CPF has exactly 11 digits
    if len(cpf_numbers) != 11:
        raise ValueError("CPF must have exactly 11 digits.")
    
    # Format the CPF
    formatted_cpf = f"{cpf_numbers[:3]}.{cpf_numbers[3:6]}.{cpf_numbers[6:9]}-{cpf_numbers[9:]}"
    
    return formatted_cpf


def clean_cpf(cpf):
    """
    Removes all non-digit characters from the CPF.
    Raises an exception if the CPF does not have 11 digits after cleaning.
    """
    if re.search(r'[a-zA-Z]', cpf):
        raise InvalidFormatCPFError("CPF contains letters.")

    cpf_numbers = re.sub(r'\D', '', cpf)
    if len(cpf_numbers) != 11:
        raise InvalidLengthCPFError(len(cpf_numbers))
    return cpf_numbers

def validate_cpf(cpf):
    """
    Validates a CPF by checking the verification digits.
    Raises specific exceptions for different validation errors.
    """
    cpf_numbers = clean_cpf(cpf)

    # Check if all digits are the same
    if cpf_numbers == cpf_numbers[0] * 11:
        raise RepeatedDigitsCPFError()

    # Calculate the first verification digit
    sum_total = sum(int(cpf_numbers[i]) * (10 - i) for i in range(9))
    remainder = (sum_total * 10) % 11
    if remainder == 10 or remainder == 11:
        digit1 = '0'
    else:
        digit1 = str(remainder)

    # Verify first digit
    if cpf_numbers[9] != digit1:
        raise InvalidCPFError("First verification digit does not match.")

    # Calculate the second verification digit
    sum_total = sum(int(cpf_numbers[i]) * (11 - i) for i in range(10))
    remainder = (sum_total * 10) % 11
    if remainder == 10 or remainder == 11:
        digit2 = '0'
    else:
        digit2 = str(remainder)

    # Verify second digit
    if cpf_numbers[10] != digit2:
        raise InvalidCPFError("Second verification digit does not match.")

    return True