from flask import Flask, render_template, request, redirect, send_file
from scraper_job import search_stackoverflow, search_indeed
import csv


app = Flask("__name__")

db = {}

def aggregate_jobs(param):
    stackoverflow_jobs = search_stackoverflow(param)
    indeed_jobs = search_indeed(param)
    jobs = stackoverflow_jobs + indeed_jobs

    return jobs

def save_to_file(jobs, param):
    file = open(f"csvs/{param}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Location", "Link"])

    for job in jobs:
        writer.writerow(list(job.values()))

    return

@app.route("/export")
def export():
    try:
        param = request.args.get("param").lower()
        print(param)
        if not param:
            raise Exception()
        jobs = db.get(param)
        if not jobs:
            raise Exception()

        save_to_file(jobs, param)

        return send_file(
            f"csv/{param}.csv",
            as_attachment=True,
            attachment_filename=f"{param}.csv",
            cache_timeout=0)
    except:
        return redirect("/")

@app.route("/report")
def search():
    param = request.args.get("param").lower()

    if param in db:
        jobs = db[param]
    else:
        jobs = aggregate_jobs(param)
        db[param] = jobs
    number_of_jobs = len(jobs)
    
    return render_template("report.html", jobs=jobs, number_of_jobs=number_of_jobs, param=param)
@app.route("/")
def home():
    return render_template("home.html")

# @app.route("/report")
# def report():
#     word = request.args.get('word')
#     if word:
#         word = word.lower() 
#         existingJobs = db.get(word)
#         if existingJobs:
#             jobs = existingJobs
#         else:
#             jobs = get_jobs(word)
#             db[word] = jobs

#     else:
#         return redirect("/")
#     return render_template("report.html", searchingBy = word, resultsNumber=len(jobs), jobs=jobs)
    

if __name__ == "__main__":
    app.run(debug=True)

