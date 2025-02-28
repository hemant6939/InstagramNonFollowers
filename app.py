import streamlit as st
import os
from bs4 import BeautifulSoup

# Function to extract usernames from HTML file
def extract_usernames_from_html(file_content):
    try:
        soup = BeautifulSoup(file_content, "html.parser")
        usernames = [a.text.strip() for a in soup.find_all("a")]
        return usernames
    except Exception as e:
        st.error(f"Error extracting usernames: {e}")
        return None

# Streamlit App
st.title("Instagram Non-Followers Checker")

st.markdown("Upload your **Followers** and **Following** HTML files to find out who doesn't follow you back.")

# Upload Files
followers_file = st.file_uploader("Upload Followers HTML", type=["html"])
following_file = st.file_uploader("Upload Following HTML", type=["html"])

if followers_file and following_file:
    try:
        followers_content = followers_file.read().decode("utf-8")
        following_content = following_file.read().decode("utf-8")

        followers = extract_usernames_from_html(followers_content)
        following = extract_usernames_from_html(following_content)

        if followers is None or following is None:
            st.error("Invalid HTML file format. Please upload valid Instagram files.")
        else:
            # Find non-followers
            non_followers = [user for user in following if user not in followers]

            st.subheader("Accounts that don't follow you back:")
            if non_followers:
                for user in non_followers:
                    st.markdown(f"- [{user}](https://www.instagram.com/{user})")
                
                # Provide Download Link
                result_file = "non_followers.html"
                with open(result_file, "w") as file:
                    file.write("<html><body><h1>Non-Followers</h1><ul>")
                    for user in non_followers:
                        file.write(f'<li><a href="https://www.instagram.com/{user}" target="_blank">{user}</a></li>')
                    file.write("</ul></body></html>")

                with open(result_file, "rb") as file:
                    st.download_button("Download Non-Followers List", file, file_name="non_followers.html")
            else:
                st.success("Congratulations! Everyone you follow follows you back. 🎉")

    except Exception as e:
        st.error(f"Error processing files: {e}")
