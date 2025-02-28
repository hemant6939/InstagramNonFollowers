import streamlit as st
from bs4 import BeautifulSoup

# Custom CSS for Instagram styling
st.markdown("""
<style>
    /* Main title gradient */
    .instagram-title {
        background: linear-gradient(45deg, #833AB4, #E1306C, #F77737);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 30px !important;
        display: inline-block; /* Ensure gradient applies correctly */
    }
    
    /* Section headers */
    h2 {
        color: #E1306C !important;
        border-bottom: 2px solid #833AB4;
        padding-bottom: 5px;
    }
    
    h3 {
        color: #833AB4 !important;
    }
    
    /* Download button styling */
    .stDownloadButton button {
        background: linear-gradient(45deg, #833AB4, #E1306C) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(131, 58, 180, 0.4);
    }
    
    /* File uploader styling */
    .stFileUploader {
        border: 2px solid #833AB4 !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    
    /* Instructions styling */
    .instructions {
        background: #fafafa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 30px !important;
    }
    
    .instructions ol {
        color: #666;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# App Title
st.markdown(
    '<h1 class="instagram-title">Instagram Non-Followers Checker</h1>',
    unsafe_allow_html=True
)

# Instructions Section
st.markdown("""
<div class="instructions">
    <h3 style="color: #E1306C !important; margin-top: 0;">How to Use</h3>
    <ol>
        <li>Go to your Instagram Settings</li>
        <li>Select <strong style="color: #833AB4;">Privacy and Security</strong></li>
        <li>Click <strong style="color: #833AB4;">Download Data</strong></li>
        <li>Request download and look for:<br>
            <code style="background: #f0f0f0; padding: 2px 5px; border-radius: 3px;">followers.html</code> and 
            <code style="background: #f0f0f0; padding: 2px 5px; border-radius: 3px;">following.html</code>
        </li>
    </ol>
</div>
""", unsafe_allow_html=True)

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
                    st.markdown(f'<span style="color: #E1306C">• </span>'
                                f'<a href="https://www.instagram.com/{user}" target="_blank" '
                                f'style="color: #833AB4; text-decoration: none;">@{user}</a>', 
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
