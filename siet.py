import re

def check_password_strength(password):
    score = 0
    suggestions = []

    # Length requirement
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Password should be at least 8 characters long")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Include at least one uppercase letter")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Include at least one lowercase letter")

    # Digit
    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Include at least one digit")

    # Special character
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Include at least one special character (e.g., !@#$%)")

    # Interpret score
    if score == 5:
        strength = "Very Strong"
    elif score >= 4:
        strength = "Strong"
    elif score == 3:
        strength = "Moderate"
    elif score == 2:
        strength = "Weak"
    else:
        strength = "Very Weak"

    return strength, suggestions

def main():
    pwd = input("Enter a password to evaluate: ")
    strength, suggestions = check_password_strength(pwd)
    print(f"Strength: {strength}")
    if suggestions:
        print("Suggestions to improve your password:")
        for s in suggestions:
            print(" –", s)

if __name__ == "__main__":
    main()

