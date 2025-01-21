from flask import Flask, request, render_template, send_file
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Function to extract usernames from HTML file
def extract_usernames_from_html(file):
    try:
        soup = BeautifulSoup(file, "html.parser")
        usernames = [a.text.strip() for a in soup.find_all("a")]
        return usernames
    except Exception as e:
        print(f"Error extracting usernames: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        followers_file = request.files.get("followers_file")
        following_file = request.files.get("following_file")

        if not followers_file or not following_file:
            return render_template("index.html", error="Please upload both Followers and Following HTML files.")

        try:
            # Extract usernames from both files
            followers = extract_usernames_from_html(followers_file)
            following = extract_usernames_from_html(following_file)

            if followers is None or following is None:
                return render_template("index.html", error="Invalid HTML file format.")

            # Find non-followers
            non_followers = [user for user in following if user not in followers]

            # Create an HTML result file
            result_file_path = os.path.join(RESULT_FOLDER, "non_followers.html")
            with open(result_file_path, "w") as result_file:
                result_file.write("<html><body><h1>Non-Followers</h1><ul>")
                for user in non_followers:
                    result_file.write(f'<li><a href="https://www.instagram.com/{user}" target="_blank">{user}</a></li>')
                result_file.write("</ul></body></html>")

            return render_template("result.html", non_followers=non_followers, download_link="/download")

        except Exception as e:
            print(f"Error: {e}")
            return render_template("index.html", error="Failed to process files. Please upload valid HTML files.")

    return render_template("index.html")

@app.route("/download")
def download():
    result_file = os.path.join(RESULT_FOLDER, "non_followers.html")
    return send_file(result_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
