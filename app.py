import streamlit as st
from bs4 import BeautifulSoup
import tempfile

# Custom CSS with working title styling
st.markdown("""
<style>
    .instagram-title {
        color: #E1306C;
        background: linear-gradient(45deg, #833AB4, #E1306C, #F77737);
        -webkit-background-clip: text;
        -moz-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        -moz-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
        margin: 20px 0;
        display: block;
        position: relative;
        z-index: 999;
    }

    @media (max-width: 768px) {
        .instagram-title {
            font-size: 2rem;
        }
    }

    .stDownloadButton button {
        background: linear-gradient(45deg, #833AB4, #E1306C) !important;
        color: white !important;
        margin-top: 20px;
    }

    .instructions {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<span class="instagram-title">Instagram Non-Followers Checker</span>', unsafe_allow_html=True)

# Instructions Section
st.markdown("""
<div class="instructions">
    <h3 style="color: #E1306C; margin-top: 0;">📌 How to Use</h3>
    <ol>
        <li>Open Instagram mobile app</li>
        <li>Go to <strong>Settings → Privacy → Download data</strong></li>
        <li>Request download and wait for email</li>
        <li>Upload the <code>followers.html</code> and <code>following.html</code> files below</li>
    </ol>
</div>
""", unsafe_allow_html=True)

def validate_instagram_file(content, file_type):
    """Validate Instagram HTML file structure"""
    try:
        soup = BeautifulSoup(content, "html.parser")
        if file_type == "followers":
            return bool(soup.find("h2", string="Followers"))
        elif file_type == "following":
            return bool(soup.find("h2", string="Following"))
        return False
    except Exception:
        return False

def extract_usernames(file_content):
    """Extract and deduplicate usernames from HTML"""
    try:
        soup = BeautifulSoup(file_content, "html.parser")
        return {a.text.strip() for a in soup.find_all("a") if a.text.strip()}
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

# File Upload Section
st.markdown("### 📤 Upload Your Files")
col1, col2 = st.columns(2)
with col1:
    followers_file = st.file_uploader("Followers HTML", type=["html"], help="Upload followers.html file")
with col2:
    following_file = st.file_uploader("Following HTML", type=["html"], help="Upload following.html file")

if followers_file and following_file:
    try:
        with st.spinner("Analyzing your connections..."):
            # Read and validate files
            followers_content = followers_file.read().decode("utf-8")
            following_content = following_file.read().decode("utf-8")

            if not validate_instagram_file(followers_content, "followers"):
                st.error("Invalid followers file - please upload the correct followers.html")
                st.stop()
            if not validate_instagram_file(following_content, "following"):
                st.error("Invalid following file - please upload the correct following.html")
                st.stop()

            # Process files
            followers = extract_usernames(followers_content)
            following = extract_usernames(following_content)

            if not followers or not following:
                st.error("Failed to extract data from files")
                st.stop()

            # Calculate non-followers
            non_followers = sorted(following - followers)

            # Display results
            st.markdown("### 📝 Results")
            if non_followers:
                st.markdown(f"**Found {len(non_followers)} accounts not following you back:**")
                for user in non_followers:
                    st.markdown(f"""
                        <div style="margin: 5px 0; padding: 8px; border-radius: 5px; background: #f8f9fa;">
                        🔹 <a href="https://www.instagram.com/{user}" target="_blank" 
                           style="color: #E1306C; text-decoration: none;">@{user}</a>
                        </div>
                    """, unsafe_allow_html=True)

                # Create downloadable file
                with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as tmp:
                    tmp.write("""<html><head><style>
                        body { font-family: Arial, sans-serif; padding: 20px; }
                        h1 { color: #833AB4; }
                        li { margin: 10px 0; }
                        a { color: #E1306C; text-decoration: none; }
                        </style></head>
                        <body><h1>Non-Followers List</h1><ul>""")
                    for user in non_followers:
                        tmp.write(f'<li><a href="https://www.instagram.com/{user}" target="_blank">@{user}</a></li>')
                    tmp.write("</ul></body></html>")
                    tmp_path = tmp.name

                # Download button
                with open(tmp_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Full List",
                        data=f,
                        file_name="instagram_non_followers.html",
                        mime="text/html",
                        help="Download HTML file with clickable links to all non-followers"
                    )
                os.unlink(tmp_path)
                
            else:
                st.success("🎉 All your followers are following you back!")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
