from src.students_grades.database.database import init_db


def main():
     init_db()
     print("===== Система учета оценок студента =====")

if __name__ == "__main__":
     main()