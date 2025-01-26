Instagram Non-Followers Checker

Project Description

The Instagram Non-Followers Checker is a Python-based application that helps you identify Instagram accounts that do not follow you back. By comparing two lists (followers and following), the application generates a list of accounts that are not following you back.

This tool can be useful for managing your Instagram connections, cleaning up your follower list, or simply gaining insights into your social media network.

Features

Compares two lists: followers and following.

Generates a list of Instagram accounts that are not following you back.

Simple and easy-to-use Python script.

Saves results in a readable format.

How to Run

Prerequisites
Python (version 3.x or higher)

Pandas (for managing data)

Other dependencies (can be installed via requirements.txt)


Steps
Clone the repository:

git clone https://github.com/hemant6939/InstagramNonFollowers.git

cd InstagramNonFollowers

Install dependencies: If you don't have the dependencies installed, create a virtual environment and install them:

python -m venv venv

source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt


Prepare your files:

Create two files: followers.txt and following.txt.

List your followers and following in each respective file (one username per line).

Run the script: After preparing your files, you can run the script with:

python check_non_followers.py

View Results: The results will be saved in a file named non_followers.txt which contains the Instagram usernames that do not follow you back.



Example Input

followers.txt
user1
user2
user3
following.txt
user2
user4
Output

non_followers.txt
user1
user3
Contributing

Feel free to fork the repository, make improvements, and create a pull request if you'd like to contribute.

git clone https://github.com/hemant6939/InstagramNonFollowers.git


License

This project is open-source and available under the MIT License. 
