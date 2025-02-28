import streamlit as st
import os
from bs4 import BeautifulSoup

# Custom CSS for Instagram styling
st.markdown("""
    <style>
        .instagram-title {
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(45deg, #833AB4, #E1306C, #F77737);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        h2 {
            color: #E1306C !important;
            border-bottom: 2px solid #833AB4;
            padding-bottom: 5px;
        }
        h3 {
            color: #833AB4 !important;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<h1 class="instagram-title">Instagram Non-Followers Checker</h1>', unsafe_allow_html=True)

# Instructions Section
st.markdown("""
### 📌 How to Use:
1. **Go to Instagram Settings**  
2. **Select Privacy and Security**  
3. **Download Data** from Instagram  
4. Upload:
   - `followers.html`
   - `following.html`
""")

# Function to extract usernames from HTML file
def extract_usernames_from_html(file_content):
    try:
        soup = BeautifulSoup(file_content, "html.parser")
        usernames = [a.text.strip() for a in soup.find_all("a")]
        return usernames
    except Exception as e:
        st.error(f"Error extracting usernames: {e}")
        return None

# File Upload Section
st.markdown("### 📁 Upload Your Files")
col1, col2 = st.columns(2)
with col1:
    followers_file = st.file_uploader("Followers HTML", type=["html"], key="followers")
with col2:
    following_file = st.file_uploader("Following HTML", type=["html"], key="following")

if followers_file and following_file:
    try:
        followers_content = followers_file.read().decode("utf-8")
        following_content = following_file.read().decode("utf-8")

        followers = extract_usernames_from_html(followers_content)
        following = extract_usernames_from_html(following_content)

        if followers is None or following is None:
            st.error("❌ Invalid HTML file format. Please upload valid Instagram files.")
        else:
            # Find non-followers
            non_followers = [user for user in following if user not in followers]

            st.markdown("### 📋 Results")
            if non_followers:
                st.markdown(f"**Found {len(non_followers)} accounts not following you back:**")
                for user in non_followers:
                    st.markdown(f'<a href="https://www.instagram.com/{user}" target="_blank" '
                                f'style="color: #833AB4; text-decoration: none; font-weight: bold;">@{user}</a>', 
                                unsafe_allow_html=True)
                
                # Provide Download Link
                result_file = "non_followers.html"
                with open(result_file, "w") as file:
                    file.write("""<html><head><style>
                                body { font-family: Arial, sans-serif; padding: 20px; }
                                h1 { color: #833AB4; }
                                li { margin: 10px 0; }
                                a { color: #E1306C; text-decoration: none; }
                                </style></head>
                                <body><h1>Non-Followers List</h1><ul>""")
                    for user in non_followers:
                        file.write(f'<li><a href="https://www.instagram.com/{user}" target="_blank">@{user}</a></li>')
                    file.write("</ul></body></html>")

                with open(result_file, "rb") as file:
                    st.download_button(
                        label="📥 Download Full List",
                        data=file,
                        file_name="non_followers.html",
                        help="Download HTML file with clickable links to all non-followers"
                    )
            else:
                st.success("🎉 Congratulations! Everyone you follow follows you back!")

    except Exception as e:
        st.error(f"❌ Error processing files: {e}")
