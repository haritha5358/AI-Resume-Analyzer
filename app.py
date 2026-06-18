
import os
import pdfplumber

from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime



app = Flask(__name__)



# Upload folder

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)




# Database config

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resumes.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)





# Skills list

SKILLS = [

    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "aws",
    "react",
    "node",
    "docker",
    "kubernetes"

]





# Database table

class Resume(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    filename = db.Column(
        db.String(200)
    )


    skills = db.Column(
        db.String(500)
    )


    score = db.Column(
        db.Integer
    )


    recommendations = db.Column(
        db.String(500)
    )


    date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )






# Extract skills from PDF

def extract_skills(pdf_path):


    text = ""


    with pdfplumber.open(pdf_path) as pdf:


        for page in pdf.pages:


            page_text = page.extract_text()


            if page_text:


                text += page_text.lower()






    found_skills = []



    for skill in SKILLS:


        if skill in text:


            found_skills.append(skill)





    score = int(
        (len(found_skills) / len(SKILLS)) * 100
    )





    recommendations = []



    if "python" not in found_skills:


        recommendations.append(
            "Add Python projects"
        )



    if "sql" not in found_skills:


        recommendations.append(
            "Add SQL/database skills"
        )



    if "aws" not in found_skills:


        recommendations.append(
            "Add cloud skills like AWS"
        )



    if len(found_skills) < 5:


        recommendations.append(
            "Add more technical skills"
        )





    return found_skills, score, recommendations







# Upload page

@app.route("/", methods=["GET", "POST"])

def upload_file():



    skills = []

    filename = ""

    score = 0

    recommendations = []




    if request.method == "POST":



        file = request.files.get("file")



        if file:



            filename = file.filename




            path = os.path.join(

                app.config["UPLOAD_FOLDER"],

                filename

            )



            file.save(path)





            skills, score, recommendations = extract_skills(path)






            # Save data

            resume = Resume(

                filename=filename,

                skills=", ".join(skills),

                score=score,

                recommendations=", ".join(recommendations)

            )



            db.session.add(resume)

            db.session.commit()






    return render_template(

        "index.html",

        skills=skills,

        filename=filename,

        score=score,

        recommendations=recommendations

    )








# History page

@app.route("/history")

def history():



    resumes = Resume.query.all()



    return render_template(

        "history.html",

        resumes=resumes

    )



# Start app

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
