# Import Libraries
import re
import streamlit as st
from datetime import datetime
import random
import string
import pyperclip
import pandas as pd

# Set Page Configuration
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐")

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Include at least one uppercase letter.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Include at least one lowercase letter.")

    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Include at least one digit.")

    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")

    if len(set(password)) < len(password) / 2:
        feedback.append("Avoid repeating characters.")

    common_passwords = ['password', '123456', 'qwerty', 'abc123', 'password1']
    if password.lower() in common_passwords:
        feedback.append("Do not use common passwords like 'password', '123456', etc.")

    return score, feedback

# Password Generator Function
def generate_password(length=12, use_special_chars=True):
    characters = string.ascii_letters + string.digits
    if use_special_chars:
        characters += "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    # Ensure the password contains all required character types
    if not re.search(r'[A-Z]', password):
        password = password[:-1] + random.choice(string.ascii_uppercase)
    if not re.search(r'[a-z]', password):
        password = password[:-1] + random.choice(string.ascii_lowercase)
    if not re.search(r'[0-9]', password):
        password = password[:-1] + random.choice(string.digits)
    if use_special_chars and not re.search(r'[!@#$%^&*]', password):
        password = password[:-1] + random.choice("!@#$%^&*")
    return ''.join(random.sample(password, len(password)))

# Initialize Session State
if 'password_history' not in st.session_state:
    st.session_state['password_history'] = []

if 'generated_password' not in st.session_state:
    st.session_state['generated_password'] = ""

if 'show_history' not in st.session_state:
    st.session_state['show_history'] = False

# Sidebar Features
st.sidebar.title("🔧 App Settings")

if st.sidebar.button("🗑️ Clear Password History"):
    st.session_state['password_history'] = []
    st.sidebar.success("Password history cleared!")

if st.sidebar.button("📥 Download Password History"):
    df = pd.DataFrame(st.session_state['password_history'], columns=["Passwords", "Timestamp"])
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download CSV", data=csv, file_name="password_history.csv", mime="text/csv")

if st.sidebar.button("📜Show History"):
    st.session_state['show_history'] = not st.session_state['show_history']

if st.session_state['show_history']:
    st.sidebar.subheader("Password History")
    if not st.session_state['password_history']:
        st.sidebar.info("No passwords generated yet.")
    else:
        for pwd, timestamp in st.session_state['password_history']:
            st.sidebar.text(f"{pwd} - {timestamp}")

# Streamlit App Interface
st.title("🔐 Ultimate Password Strength Meter")
st.write("Evaluate your password security, generate strong passwords, and protect your data!")

password = st.text_input("Enter your Password", type="password")
show_password = st.checkbox("Show Password")

if show_password and password:
    st.write(f"Your Password: `{password}`")

if password:
    score, feedback = check_password_strength(password)
    strength_level = {1: "Very Weak", 2: "Weak", 3: "Moderate", 4: "Strong", 5: "Very Strong"}

    st.subheader(f"Password Strength: {strength_level.get(score, 'Very Weak')}")
    st.progress(score * 20)

    if score == 5:
        st.success("✅ Excellent! Your password is very strong.")
    elif score >= 3:
        st.warning("⚠️ Your password is moderate. Consider improving it.")
    else:
        st.error("❌ Your password is weak. Please improve it.")

    if feedback:
        st.write("### Suggestions to Improve Your Password:")
        for suggestion in feedback:
            st.write(f"- {suggestion}")

    st.write(f"🔍 Analysis done at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if st.button("Copy Password to Clipboard"):
        pyperclip.copy(password)
        st.success("Password copied to clipboard!")
        st.balloons()
else:
    st.info("Please enter a password to analyze.")

# Password Generator Feature
st.markdown("---")
st.subheader("🔑 Password Generator")
gen_length = st.slider("Select Password Length", min_value=8, max_value=20, value=12)
use_special_chars = st.checkbox("Include Special Characters", value=True)
if st.button("Generate Password"):
    generated_password = generate_password(gen_length, use_special_chars)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.session_state['generated_password'] = generated_password
    st.session_state['password_history'].append((generated_password, timestamp))
    st.success(f"Generated Password: `{generated_password}`")

if st.session_state['generated_password']:
    if st.button("Copy Generated Password"):
        pyperclip.copy(st.session_state['generated_password'])
        st.success("Generated password copied to clipboard!")
        st.balloons()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Hooriya Muhammad Fareed")
