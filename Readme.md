# Coders of Delhi – Flask-Based Recommendation System

This project is a **Flask web application** that demonstrates core social-network
recommendation features such as **People You May Know** and **Pages You Might Like**
using **pure Python logic** and JSON data.

The goal of this project is to practice **data cleaning, graph-style logic, and Flask
backend development** without relying on heavy data-science libraries.

---

## 🚀 Features

- Load and parse JSON user data
- Clean messy and inconsistent datasets
- Find mutual connections between users
- Recommend pages based on common interests
- Flask routes rendered with Jinja templates
- Simple local setup for learning and testing

---

## 🛠 Tech Stack

- Python 3
- Flask
- Jinja2
- JSON

---

## 📁 Project Structure

```text
project-root/
├── .venv/
│   ├── Include
│   ├── Lib
│   ├── Scripts
│   └── pyvenv.cfg
├── Code_book.json
├── OS_Structure.py
├── Readme.md
├── app.py
├── data.json
├── messy_data.json
├── requirments.txt
└── templates/
    ├── base.html
    ├── clean.html
    ├── find_mutual_pages.html
    ├── home.html
    ├── messy.html
    └── sample.html
