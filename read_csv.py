import csv
from dan import db
from dan.models import *

def main():
    f = open("csvfiles/courses.csv")
    reader = csv.reader(f)
    for code, name in reader:
        course = Course(name=name, code=code)

        if(not Course.query.filter_by(code=code).first()):
            db.session.add(course)
            print(f"Added course {course.name}")


    db.session.commit()

if __name__ == "__main__":
    main()
