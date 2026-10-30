from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"

# 20 sample aptitude questions: Quantitative, Logical, Verbal and Technical.
QUESTIONS = [
    {"topic":"Quantitative Aptitude","q":"What is 25% of 200?","options":["25","40","50","75"],"answer":"50","why":"25% means 25/100. So 200 × 25/100 = 50."},
    {"topic":"Quantitative Aptitude","q":"A shirt costs ₹800. Its price is reduced by 10%. New price?","options":["₹700","₹720","₹740","₹780"],"answer":"₹720","why":"10% of 800 is 80. 800 − 80 = 720."},
    {"topic":"Quantitative Aptitude","q":"Find the average of 10, 20 and 30.","options":["15","20","25","30"],"answer":"20","why":"Average = (10 + 20 + 30) / 3 = 20."},
    {"topic":"Quantitative Aptitude","q":"A car travels 120 km in 2 hours. Its speed is:","options":["40 km/h","50 km/h","60 km/h","80 km/h"],"answer":"60 km/h","why":"Speed = distance / time = 120 / 2 = 60 km/h."},
    {"topic":"Quantitative Aptitude","q":"If x + 7 = 15, find x.","options":["6","7","8","9"],"answer":"8","why":"Subtract 7 from both sides: x = 15 − 7 = 8."},
    {"topic":"Logical Reasoning","q":"Find the next number: 2, 4, 8, 16, ?","options":["20","24","30","32"],"answer":"32","why":"Each number is multiplied by 2."},
    {"topic":"Logical Reasoning","q":"Which one is different?","options":["Apple","Mango","Carrot","Banana"],"answer":"Carrot","why":"Carrot is a vegetable; the others are fruits."},
    {"topic":"Logical Reasoning","q":"If CAT is coded as DBU, DOG is coded as:","options":["EPH","EOG","FPH","DPH"],"answer":"EPH","why":"Each letter is moved one step forward."},
    {"topic":"Logical Reasoning","q":"Complete the series: A, C, E, G, ?","options":["H","I","J","K"],"answer":"I","why":"The series skips one letter each time."},
    {"topic":"Logical Reasoning","q":"A is taller than B. B is taller than C. Who is shortest?","options":["A","B","C","Cannot say"],"answer":"C","why":"A > B > C, so C is shortest."},
    {"topic":"Verbal Ability","q":"Choose the synonym of 'Quick'.","options":["Slow","Fast","Weak","Late"],"answer":"Fast","why":"'Fast' has the same meaning as 'Quick'."},
    {"topic":"Verbal Ability","q":"Choose the correct spelling.","options":["Recieve","Receive","Receeve","Receve"],"answer":"Receive","why":"The correct spelling is Receive."},
    {"topic":"Verbal Ability","q":"Fill in the blank: She ___ to college every day.","options":["go","going","goes","gone"],"answer":"goes","why":"With 'she' in the simple present tense, use 'goes'."},
    {"topic":"Verbal Ability","q":"Choose the antonym of 'Expand'.","options":["Increase","Grow","Enlarge","Contract"],"answer":"Contract","why":"'Contract' means to become smaller; it is the opposite of expand."},
    {"topic":"Verbal Ability","q":"Choose the correct sentence.","options":["He are happy.","He is happy.","He am happy.","He be happy."],"answer":"He is happy.","why":"'He' takes the verb 'is'."},
    {"topic":"Technical Aptitude","q":"Which data structure follows FIFO?","options":["Stack","Queue","Tree","Graph"],"answer":"Queue","why":"FIFO means First In, First Out. A queue follows FIFO."},
    {"topic":"Technical Aptitude","q":"Which SQL command is used to retrieve data?","options":["INSERT","UPDATE","SELECT","DELETE"],"answer":"SELECT","why":"SELECT fetches records from a database."},
    {"topic":"Technical Aptitude","q":"Which OOP concept hides internal details?","options":["Inheritance","Encapsulation","Looping","Compilation"],"answer":"Encapsulation","why":"Encapsulation bundles data and methods and controls access."},
    {"topic":"Technical Aptitude","q":"Which language commonly runs in a web browser?","options":["C","JavaScript","SQL","C++"],"answer":"JavaScript","why":"JavaScript is natively supported by web browsers."},
    {"topic":"Technical Aptitude","q":"What does CPU stand for?","options":["Central Processing Unit","Computer Personal Unit","Central Program Utility","Control Process User"],"answer":"Central Processing Unit","why":"CPU stands for Central Processing Unit."}
]

INTERVIEW = {
    "Software Developer": ["Tell me about yourself.","What is OOP?","What is the difference between C and Python?","What is a database?","Explain one project you built."],
    "Data Analyst": ["Tell me about yourself.","What is data cleaning?","What is the difference between SQL and Excel?","What is a dashboard?","Explain one data project."],
    "AI/ML Engineer": ["Tell me about yourself.","What is machine learning?","Explain supervised vs unsupervised learning.","What is overfitting?","Explain one AI/ML project."],
    "General / Fresher": ["Tell me about yourself.","What are your strengths?","What is one weakness you are improving?","Why should we select you?","Where do you see yourself in five years?"]
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        session["student"] = {
            "name": request.form.get("name", "Student").strip() or "Student",
            "role": request.form.get("role", "General / Fresher"),
            "skills": request.form.get("skills", "")
        }
        session["answers"] = {}
        return redirect(url_for("aptitude", number=1))
    return render_template("profile.html")

@app.route("/aptitude/<int:number>", methods=["GET", "POST"])
def aptitude(number):
    if "student" not in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        selected = request.form.get("answer")
        if selected:
            answers = session.get("answers", {})
            answers[str(number)] = selected
            session["answers"] = answers
        if number < len(QUESTIONS):
            return redirect(url_for("aptitude", number=number + 1))
        return redirect(url_for("aptitude_done"))

    if number < 1 or number > len(QUESTIONS):
        return redirect(url_for("aptitude", number=1))
    return render_template("aptitude.html", q=QUESTIONS[number-1], number=number,
                           total=len(QUESTIONS), selected=session.get("answers", {}).get(str(number)))

@app.route("/aptitude-done")
def aptitude_done():
    if "student" not in session:
        return redirect(url_for("profile"))
    answers = session.get("answers", {})
    score = sum(1 for i, q in enumerate(QUESTIONS, 1) if answers.get(str(i)) == q["answer"])
    return render_template("aptitude_done.html", score=score, total=len(QUESTIONS))

@app.route("/interview", methods=["GET", "POST"])
def interview():
    if "student" not in session:
        return redirect(url_for("profile"))
    role = session["student"]["role"]
    questions = INTERVIEW.get(role, INTERVIEW["General / Fresher"])
    if request.method == "POST":
        session["interview_answers"] = [request.form.get(f"answer{i}", "") for i in range(5)]
        return redirect(url_for("results"))
    return render_template("interview.html", questions=questions, role=role)

@app.route("/results")
def results():
    if "student" not in session:
        return redirect(url_for("profile"))
    answers = session.get("answers", {})
    score = sum(1 for i, q in enumerate(QUESTIONS, 1) if answers.get(str(i)) == q["answer"])
    topic_scores = {}
    for i, q in enumerate(QUESTIONS, 1):
        topic_scores.setdefault(q["topic"], [0, 0])
        topic_scores[q["topic"]][1] += 1
        if answers.get(str(i)) == q["answer"]:
            topic_scores[q["topic"]][0] += 1
    return render_template("results.html", student=session["student"], score=score,
                           total=len(QUESTIONS), topic_scores=topic_scores,
                           interview_answers=session.get("interview_answers", []))

@app.route("/dashboard")
def dashboard():
    if "student" not in session:
        return redirect(url_for("profile"))
    return render_template("dashboard.html", student=session["student"])

if __name__ == "__main__":
    app.run(debug=True)
