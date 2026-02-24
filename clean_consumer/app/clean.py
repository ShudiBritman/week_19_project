import re



def clean_and_upper_case_text(instructions_special):
    clean = re.sub(r'[^\w]', "", instructions_special)
    cap_letter = clean.lower()
    return cap_letter