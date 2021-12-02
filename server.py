from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import time, connection
import os
import data_manager

app = Flask(__name__)
pictures_questions = ".\\static\\uploads_pictures_questions"
app.config["UPLOAD_PICTURE_FOLDER"] = pictures_questions
pictures_answers = '.\\static\\uploads_pictures_answers'
app.config["UPLOAD_PICTURE_ANSWERS"] = pictures_answers
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG", "PNG"]


@app.route("/vote/<id>/<value>")
def list_voting(id, value):
    if value == "+":
        data_manager.add_vote_counter(id)
    elif value == "-":
        data_manager.substract_vote_counter(id)
    return redirect("/")



# @app.route("/question/vote/<question_id>/<answer_id>/<vote_number>")
# def list_answer_voting(question_id, answer_id, vote_number):
#     print(vote_number)
#     print(answer_id)
#     data_manager.vote_for_answers(answer_id, vote_number, question_id)
#     # connection.export_data("sample_data/answer.csv", ans_list, data_manager.ANSWER_HEADERS, "w")
#     return redirect(f"/question/{question_id}")

@app.route("/")
def main():
    questions = data_manager.get_data_to_main_list()
    return render_template("index.html", questions=questions, table_header=data_manager.TABLE_HEADERS)


@app.route("/list")
def question_list():
    questions_list = data_manager.get_question_bd()
    
    return render_template("list.html", questions_list=questions_list, table_headers=data_manager.TABLE_HEADERS)



# @app.route("/<value>/<descend>")
# def prepare_sorted_table_to_display(descend, value):
#     questions_list, table_headers = data_manager.prepare_table_to_display(int(descend), value)
#     return render_template("list.html", questions_list=questions_list, table_headers=table_headers)


# @app.route("/add-question", methods=['GET', 'POST'])
# def add_information_about_question():
#     if request.method == "POST":
#         ID = data_manager.ID_gen()
#         unix_time = int(time.time())
#         title = request.form["title"]
#         question = request.form["question"]
#         image = request.files["image"]
#         if image.filename != "":
#             if not data_manager.allowed_image(image.filename):
#                 return redirect(request.url)
#             image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))
#
#             dic = {"id": str(ID), "submission_time": str(unix_time), "view_number": "0", "vote_number": "0",
#                    "title": title, "message": question,
#                    "Image": "../static/uploads_pictures_questions/" + str(image.filename)}
#         else:
#             dic = {"id": str(ID), "submission_time": str(unix_time), "view_number": "0", "vote_number": "0",
#                    "title": title, "message": question, "Image": ""}
#         connection.export_data("./sample_data/question.csv", dic, data_manager.QUESTION_HEADERS, "a")
#         return redirect("/")
#     return render_template("add-question.html")


@app.route("/<value>/<descend>")
def prepare_sorted_table_to_display(value,descend=1):
    questions_list = data_manager.sort_questions_by_column(value)
    table_headers = data_manager.TABLE_HEADERS
    return render_template("list.html", questions_list=questions_list, table_headers=table_headers)


# Witold
@app.route('/question')
@app.route('/question/<question_id>')
def question(question_id):
<<<<<<< HEAD
    question_data = data_manager.find_title_and_message(int(question_id))
=======
    question_data = data_manager.find_title_and_message(question_id)
>>>>>>> kuba-bogacki
    answer_data = data_manager.find_all_answer_to_question(question_id)
    comment_to_question_data = data_manager.get_comment_data_by_question_id(question_id)
    comment_to_answer_data = data_manager.get_comment_data_by_answer_id(question_id)
    # print(question_id)
    # print(comment_to_question_data)
    # print(question_data)
    answers_number = len(answer_data)

    return render_template('question.html', question_data=question_data, question_id=question_id,
                           answer_data=answer_data, comment_to_question_data=comment_to_question_data,
                           answers_number=answers_number)


@app.route('/new_answer/<question_id>')
def saving_new_answer(question_id):
<<<<<<< HEAD
    question_data = data_manager.get_question_db_by_question_id(int(question_id))
=======
    question_data = data_manager.get_question_db_by_question_id(question_id)
>>>>>>> kuba-bogacki

    return render_template("new_answer.html", question_data=question_data, question_id=question_id)


@app.route('/new_answer/<question_id>/new-answer', methods=["POST"])
def summary_new_answer(question_id):
    if request.method == "POST":
        message = request.form.get("message")
        submission_time = str(datetime.now())[:-7]
        vote_number = 0
        image = "None"
        # image_file = request.files['image']
        # image = image_file.filename
        # if image != "":
        #     image_file.save(os.path.join('E:\\Web and SQL - Python Flask\\ask-mate-2-python-kuba-bogacki\\static\\uploads_pictures_answers', image))
        data_manager.save_new_answer(message, question_id, vote_number, submission_time, image)
    # question_id = int(question_id) + 1
    return redirect(f'/question/{question_id}')


@app.route('/new_question')
def add_new_question():

    return render_template("add-question.html")


@app.route('/new_question/add_new_question', methods=["POST"])
def summary_new_question():
    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("question")
        submission_time = str(datetime.now())[:-7]
        vote_number = 0
        view_number = 0
        image = "None"
        # image_file = request.files['image']
        # image = image_file.filename
        # if image != "":
        #     image_file.save(os.path.join('E:\\Web and SQL - Python Flask\\ask-mate-2-python-kuba-bogacki\\static\\uploads_pictures_answers', image))
        data_manager.save_new_question(message, title, vote_number, view_number, submission_time, image)

    return redirect('/list')


@app.route('/edit_question/<question_id>')
def saving_edit_question(question_id):
    question_data = data_manager.get_question_db_by_question_id(question_id)
    print(question_id)

    return render_template("edit_question.html", question_data=question_data, question_id=question_id)


@app.route('/edit_question/<question_id>/edited_question', methods=["POST"])
def summary_edited_question(question_id):
    if request.method == "POST":
        # question_id = int(question_id) - 1
        title = request.form.get("title")
        message = request.form.get("question")
        image = "None"
        print(question_id, title, message, image)
        # image_file = request.files['image']
        # image = image_file.filename
        # if image != "":
        #     image_file.save(os.path.join('E:\\Web and SQL - Python Flask\\ask-mate-2-python-kuba-bogacki\\static\\uploads_pictures_answers', image))
        data_manager.save_edited_question(question_id, title, message, image)

    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/delete/<question_id>", methods=["POST", "GET"])
def delete_answer(answer_id, question_id):
    data_manager.delete_answer_from_db_by_id(answer_id)
    data_manager.delete_answer_from_comment_by_id(answer_id)

    return redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/delete', methods=["POST"])
def delete_question(question_id):
    data_manager.delete_answers_from_comment(question_id)
    data_manager.delete_answers_from_question_tag(question_id)
    data_manager.delete_answers_from_question(question_id)
    data_manager.delete_question(question_id)
    questions_list = data_manager.get_question_bd()

    return render_template('list.html', questions_list=questions_list, table_headers=data_manager.TABLE_HEADERS)


@app.route('/edit_answer/<answer_id>')
def edit_answer(answer_id):
    answer_data = data_manager.return_question_id_and_message(answer_id)

    return render_template('edit_answer.html', answer_data=answer_data, answer_id=answer_id)


@app.route('/edit_answer/<answer_id>/edit/<question_id>', methods=["POST"])
def after_edit_answer(answer_id, question_id):
    if request.method == "POST":
        edited_answer = request.form.get('new-answer')
        data_manager.edit_answer(answer_id, edited_answer)

    return redirect(f'/question/{question_id}')


<<<<<<< HEAD
@app.route('/search')
def get_search():
    searching_phrase = request.args.get("q")
    questions = data_manager.search_user_phrase_question(searching_phrase)
    answers = data_manager.search_user_phrase_answer(searching_phrase)
    comments = data_manager.search_user_phrase_comment(searching_phrase)
    return render_template("search.html", questions=questions, answers=answers, searching_phrase=searching_phrase, comments=comments)




# @app.route('/comment/<comment_id>')
# def edit_comment(comment_id):
#     data_manager.
#
#     return render_template('comment.html', comment_id=comment_id)
#
#
# @app.route('/comment/<comment_id>/edit/<question_id>', methods=["POST"])
# def after_edit_comment(comment_id, question_id):
#
#     return redirect(f'/question/{question_id}')
=======
@app.route('/comment/<comment_id>')
def edit_comment(comment_id):
    comment_data = data_manager.get_comment_data_by_comment_id(comment_id)
    edited_count = comment_data['edited_count']
    if edited_count is None:
        edited_count = 0

    return render_template('comment.html', comment_id=comment_id, comment_data=comment_data, edited_count=edited_count)


@app.route('/comment/<comment_id>/<question_id>/<edited_count>/edit', methods=["POST"])
def after_edit_comment(comment_id, question_id, edited_count):
    if request.method == "POST":
        message = request.form.get("message")
        edited_count += 1
        submission_time = str(datetime.now())[:-7]
        data_manager.edit_comment_by_comment_id(comment_id, edited_count, submission_time, message)

    return redirect(f'/question/{question_id}')

>>>>>>> kuba-bogacki


if __name__ == "__main__":
    app.run(debug=True)
