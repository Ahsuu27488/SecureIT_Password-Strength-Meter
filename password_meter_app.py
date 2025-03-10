import streamlit as st
import re
import random
import string

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Extra credit: Check for common patterns (bonus point)
    if not re.search(r"(123|abc|qwerty|password)", password.lower()):
        score += 1
    else:
        feedback.append("❌ Avoid common patterns like '123', 'abc', or 'password'.")
    
    return score, feedback

def generate_strong_password(length=12):
    lowercase = random.sample(string.ascii_lowercase, 3)
    uppercase = random.sample(string.ascii_uppercase, 3)
    digits = random.sample(string.digits, 2)
    special = random.sample("!@#$%^&*", 2)
    
    # Combine all characters and fill remaining length with random choices
    all_chars = lowercase + uppercase + digits + special
    remaining = length - len(all_chars)
    all_chars += random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=remaining)
    
    # Shuffle the characters
    random.shuffle(all_chars)
    return ''.join(all_chars)

# Common weak passwords blacklist
COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "admin", "welcome",
    "1234", "12345678", "password123", "abc123", "letmein"
]

# Streamlit app
st.set_page_config(page_title="SecureIt - Password Strength Meter", page_icon="🔐")

st.title("🔐 SecureIt - Password Strength Meter")
st.markdown("Check how strong your password is and get suggestions to improve it.")

# Create tabs for checking and generating passwords
tab1, tab2 = st.tabs(["Check Password", "Generate Password"])

with tab1:
    password = st.text_input("Enter your password:", type="password")
    
    if st.button("Check Strength", key="check_btn"):
        if password:
            # Check if password is in common passwords list
            if password.lower() in COMMON_PASSWORDS:
                st.error("This is a commonly used password! Please choose something more unique.")
            else:
                score, feedback = check_password_strength(password)
                
                # Display score with a progress bar
                st.write(f"Score: {score}/5")
                st.progress(score/5)
                
                # Display strength rating
                if score == 5:
                    st.success("✅ Strong Password! Excellent job.")
                elif score >= 3:
                    st.warning("⚠️ Moderate Password - Consider adding more security features.")
                else:
                    st.error("❌ Weak Password - Please improve it using the suggestions below.")
                
                # Display feedback
                if feedback:
                    st.subheader("Improvement suggestions:")
                    for suggestion in feedback:
                        st.write(suggestion)
        else:
            st.warning("Please enter a password to check.")

with tab2:
    st.subheader("Generate a Strong Password")
    
    col1, col2 = st.columns(2)
    with col1:
        password_length = st.slider("Password Length", min_value=8, max_value=32, value=12)
    with col2:
        auto_gen = st.checkbox("Auto-generate on page load", value=False)
    
    if auto_gen or st.button("Generate Password", key="gen_btn"):
        strong_password = generate_strong_password(password_length)
        st.code(strong_password, language=None)
        
        # Check and display the generated password strength
        score, _ = check_password_strength(strong_password)
        st.write(f"Password Strength Score: {score}/5")
        st.progress(score/5)
        
        # Copy to clipboard button (note: this is simulated as Streamlit doesn't directly support clipboard)
        st.info("Click the password to select it, then copy using Ctrl+C or Cmd+C")

# Add sidebar with information
with st.sidebar:
    st.header("Password Security Tips")
    st.markdown("""
    ### What makes a strong password?
    - At least 8 characters (longer is better)
    - Mix of uppercase & lowercase letters
    - Includes numbers (0-9)
    - Contains special characters (!@#$%^&*)
    - Avoids common patterns or words
    
    ### Best Practices
    - Use a different password for each account
    - Consider using a password manager
    - Change passwords periodically
    - Don't share your passwords
    
    ### Password Managers
    Password managers can help you create and store strong, unique passwords for all your accounts.
    """)

# Footer
st.markdown("---")
st.caption("GIAIC Q3 Project 02: Password Strength Meter")