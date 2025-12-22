from flask import Flask, render_template, request
import json, copy


app = Flask(__name__, template_folder="templates")


def load_data(file):
    with open(file, "r") as f:
        data = json.load(f)
        # internally json.loads(f.read())
    return data


def clean_data(data):
    # Remove users with missing names.
    # create deepcopy so that changes donot place inplace
    data = copy.deepcopy(data)
    data["users"] = [user for user in data["users"] if user["name"].strip() != ""]
    # Remove duplicate friend entries.
    for user in data["users"]:
        user["friends"] = list(set(user["friends"]))
    data["users"] = [
        user
        for user in data["users"]
        if not (len(user["friends"]) == 0 and len(user["liked_pages"]) == 0)
    ]

    # Deduplicate pages based on IDs.
    unique_pages = {}
    for page in data["pages"]:
        unique_pages[page["id"]] = page
    data["pages"] = list(unique_pages.values())

    with open("Code_book.json", "w") as f:
        json.dump(data, f, indent=4)

    return data


sample_data = load_data("data.json")
messy_data = load_data("messy_data.json")
cleaned_data = clean_data(messy_data)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Data")
def sample():
    return render_template("sample.html", data=sample_data)


@app.route("/Messy")
def messy():
    return render_template("messy.html", data=messy_data)


@app.route("/Cleaned")
def clean():
    return render_template("clean.html", data=cleaned_data)


@app.route("/Mutual_friends", methods=["POST", "GET"])
def mutual_friends():
    def suggestions(user_id, data):
        user_friends = {}
        for user in data["users"]:
            user_friends[int(user["id"])] = set(map(int, user["friends"]))

        if user_id not in user_friends:
            return None

        direct_friends = user_friends[user_id]
        suggestions = {}
        for friend in direct_friends:
            for mutual in user_friends.get(friend, []):
                if mutual != user_id and mutual not in direct_friends:
                    suggestions[mutual] = (
                        suggestions.get(mutual, 0) + 1
                    )  # filling the user id with the no of mutual it has been with others

        sorted_suggestions = sorted(
            suggestions.items(), key=lambda x: x[1], reverse=True
        )  # sorting in decreasing order w.r.t value
        return [id for id, _ in sorted_suggestions]

    if request.method == "POST":
        user_id = int(request.form.get("user_id"))
        recommendations = suggestions(user_id, cleaned_data)
        return render_template(
            "find_mutual.html", recommendations=recommendations, searched=True
        )

    elif request.method == "GET":
        return render_template("find_mutual.html", recomendations=None, searched=None)


@app.route("/Mutual_pages", methods=["GET", "POST"])
def mutual_pages():
    def suggestions(user_id, data):
        # user_id -> liked pages
        user_pages = {}

        for user in data["users"]:
            user_pages[int(user["id"])] = set(map(int, user["liked_pages"]))

        # user not found
        if user_id not in user_pages:
            return None

        user_liked_pages = user_pages[user_id]
        page_suggestions = {}

        # compare with other users
        for other_user, pages in user_pages.items():
            if other_user != user_id:
                shared_pages = user_liked_pages.intersection(pages)

                if shared_pages:
                    for page in pages:
                        if page not in user_liked_pages:
                            page_suggestions[page] = page_suggestions.get(
                                page, 0
                            ) + len(shared_pages)

        # sort pages by score
        sorted_pages = sorted(
            page_suggestions.items(), key=lambda x: x[1], reverse=True
        )

        return [page_id for page_id, _ in sorted_pages]
        
    if request.method == "POST":
        user_id = int(request.form.get("user_id"))
        recommendations = suggestions(user_id, cleaned_data)

        return render_template(
            "find_mutual_pages.html", recommendations=recommendations, searched=True
        )

    return render_template(
        "find_mutual_pages.html", recommendations=None, searched=False
    )


if __name__ == "__main__":
    app.run(debug=True)
