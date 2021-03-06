import os

from psycopg2 import sql

import database_common
from utils import RANK_CALC as CALC

ANSWER_DATA_PATH = os.getenv("ANSWER_DATA_PATH") if "ANSWER_DATA_PATH" in os.environ else "sample_data/answer.csv"
QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
TABLE_HEADERS = {"vote_number": "Votes", "title": "Title", "message": "Message", "submission_time": "Date",
                 "view_number": "Views", "id":"ID"}
SORT_BY_INT = ["vote_number", "Published on", "view_number"]
reverse = 0


@database_common.connection_handler
def get_question_bd(cursor):
    cursor.execute("""
        SELECT *
        FROM question
        """)
    return cursor.fetchall()


@database_common.connection_handler
def vote_for_answers(cursor, answer_id, vote_number, question_id):
    if vote_number == "-1":
        query = """
            UPDATE answer
            SET votes_down = votes_down + 1
            WHERE id = %(answer_id)s"""
        cursor.execute(query, {'vote_number': vote_number, 'answer_id': answer_id, 'question_id': question_id})
    else:
        query = """
        UPDATE answer
        SET votes_up = votes_up + 1
        WHERE id = %(answer_id)s"""
        cursor.execute(query, {'vote_number': vote_number, 'answer_id': answer_id, 'question_id': question_id})


@database_common.connection_handler
def edit_answer(cursor, answer_id, edited_answer):
    query = sql.SQL("""
        UPDATE answer
        SET message = %(edited_answer)s
        WHERE id = %(answer_id)s
        """).format(
        answer_id=sql.Identifier('id'),
        edited_answer=sql.Identifier('message')
    )
    cursor.execute(query, {'answer_id': answer_id, 'edited_answer': edited_answer})


@database_common.connection_handler
def return_question_id_and_message(cursor, answer_id):
    query = """
        SELECT question_id, message
        FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def find_title_and_message(cursor, question_id):
    query = sql.SQL("""
        SELECT title, message, image, user_id, u.username,
        votes_up, votes_down
        FROM question
        LEFT JOIN public.user as u
        ON question.user_id = u.id
        WHERE question.id = %(question_id)s
        ORDER BY title""").format(
        question_id=sql.Identifier('question_id')
    )
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_db_by_question_id(cursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE id = %(question_id)s
        """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def save_new_answer(cursor, message, question_id, submission_time, image):
    query = """
        INSERT INTO answer
        (submission_time, vote_number, question_id, message, image)
        VALUES (%(submission_time)s, %(question_id)s, %(message)s, %(image)s);"""

    cursor.execute(query, {'submission_time': submission_time,
                           'question_id': question_id, 'message': message, 'image': image})


@database_common.connection_handler
def save_new_question(cursor, message, title, user_id, image=None):
    query = """
        INSERT INTO question
        (submission_time, message, image, title, user_id)
        VALUES (NOW(), %(message)s, %(image)s, %(title)s, %(user_id)s);"""
    cursor.execute(query, {'title': title, 'message': message, 'image': image, 'user_id': user_id})


@database_common.connection_handler
def save_edited_question(cursor, title, message, question_id):
    query = sql.SQL("""
        UPDATE question
        SET message = %(message)s, title = %(title)s
        WHERE id = %(question_id)s""").format(
        question_id=sql.Identifier('question_id')
    )
    cursor.execute(query, {'title': title, 'question_id': question_id, 'message': message})


@database_common.connection_handler
def find_all_answer_to_question(cursor, question_id):
    query = sql.SQL("""
        SELECT answer.submission_time, answer.id, answer.vote_number, answer.message, answer.user_id,
        answer.image, "user".username, answer.question_id, answer.votes_up, answer.votes_down,
        answer.acceptation_status
        FROM answer
        LEFT JOIN "user" ON answer.user_id = "user".id
        WHERE question_id = %(question_id)s
        ORDER BY vote_number DESC""").format(
        question_id=sql.Identifier('question_id')
    )
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def delete_answers_from_question(cursor, question_id):
    query = """
        DELETE FROM answer
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def delete_answers_from_comment(cursor, question_id):
    query = """
        DELETE FROM comment
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def delete_answers_from_question_tag(cursor, question_id):
    query = """
        DELETE FROM question_tag
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def delete_answer_from_db_by_id(cursor, answer_id):
    query = """
        DELETE FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@database_common.connection_handler
def delete_answer_from_comment_by_id(cursor, answer_id):
    query = """
        DELETE FROM comment
        WHERE answer_id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})



@database_common.connection_handler
def get_question_id_by_answer_id_db(cursor, answer_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE id=%s
    """
    cursor.execute(query, (answer_id,))
    real_dict = cursor.fetchall()
    real_dict_to_list = []
    for item in real_dict:
        real_dict_to_list.append(dict(item))
    return real_dict_to_list[0]["question_id"]


@database_common.connection_handler
def write_answer_to_db(cursor, question_id, message, user_id, image=None):
    query = """
    INSERT INTO answer (submission_time, question_id, message, image, user_id) 
    VALUES (NOW(),%(question_id)s,%(message)s,%(image)s, %(user_id)s)
    """
    cursor.execute(query, {"question_id": question_id, "message": message, "image": image, "user_id": user_id})


@database_common.connection_handler
def delete_answer_from_cvs_by_id_db(cursor, id):
    query = sql.SQL("""
    DELETE FROM answer
    WHERE id = %(id)s""").format(id=sql.Identifier('id'))
    cursor.execute(query, {"id": id})


@database_common.connection_handler
def delete_comment_by_question_id(cursor, question_id):
    query = sql.SQL("""
    DELETE FROM comment
    WHERE question_id = %(question_id)s""").format(id=sql.Identifier('question_id'))
    cursor.execute(query, {"question_id": question_id})


@database_common.connection_handler
def delete_comment_by_answer_id(cursor, answer_id):
    query = sql.SQL("""
    DELETE FROM comment
    WHERE answer_id = %(answer_id)s""").format(id=sql.Identifier('answer_id'))
    cursor.execute(query, {"answer_id": answer_id})

    
@database_common.connection_handler
def get_comment_data_by_comment_id(cursor, comment_id):
    query = """
        SELECT *
        FROM comment
        WHERE id = %(comment_id)s"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchall()


@database_common.connection_handler
def edit_comment_by_comment_id(cursor, message, edited_count, comment_id):
    query = """
        UPDATE comment
        SET message = %(message)s,
            edited_count = %(edited_count)s,
            submission_time = NOW()   
        WHERE id = %(comment_id)s;"""
    cursor.execute(query, {'message': message, 'edited_count': edited_count,
                           'comment_id': comment_id})


@database_common.connection_handler
def get_comment_data_by_question_id(cursor, question_id):
    query = """
        SELECT * 
        FROM comment
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_data_by_answer_id(cursor, answer_id):
    query = """
        SELECT * 
        FROM comment
        WHERE answer_id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_bd(cursor):
    cursor.execute("""
        SELECT *
        FROM question
        ORDER BY submission_time DESC
        """)
    return cursor.fetchall()
# ORDER BY submission_time DESC


@database_common.connection_handler
def add_comment(cursor, message, question_id, user_id, answer_id=None):
    query = """
            INSERT INTO comment (question_id, answer_id, message, submission_time, user_id) 
            VALUES (%(question_id)s, %(answer_id)s, %(message)s, NOW(), %(user_id)s)
    """
    arguments = {'message': message, 'question_id': question_id, 'answer_id': answer_id, 'user_id': user_id}
    cursor.execute(query, arguments)


@database_common.connection_handler
def add_vote_counter(cursor,id):
    query = sql.SQL("""
        UPDATE question
        SET votes_up = votes_up + 1
        WHERE id = %(id)s""").format(id=sql.Identifier("id"))
    cursor.execute(query, {"id": id})


@database_common.connection_handler
def substract_vote_counter(cursor, id):
    query = sql.SQL("""
        UPDATE question
        SET votes_down = votes_down + 1
        WHERE id = %(id)s""").format(id=sql.Identifier("id"))
    cursor.execute(query, {"id": id})


@database_common.connection_handler
def get_data_to_main_list(cursor):
    cursor.execute("""
        SELECT title, message, submission_time,  vote_number, view_number, id
        FROM question
        ORDER BY id DESC 
        LIMIT 5;
        """)
    return cursor.fetchall()


@database_common.connection_handler
def search_user_phrase_question(cursor, searching_phrase):
    query = """
        SELECT title, message, submission_time, id
        FROM question
        WHERE title LIKE %(searching_phrase)s or
        message LIKE %(searching_phrase)s 
        ORDER BY id DESC ;
        """
    cursor.execute(query, {"searching_phrase": f"%{searching_phrase}%"})
    return cursor.fetchall()


@database_common.connection_handler
def search_user_phrase_answer(cursor, searching_phrase):
    query = ("""
        SELECT message, submission_time, question_id
        FROM answer
        WHERE message LIKE %(searching_phrase)s
        ORDER BY id DESC;
        """)

    cursor.execute(query, {"searching_phrase": f"%{searching_phrase}%"})
    return cursor.fetchall()


@database_common.connection_handler
def search_user_phrase_comment(cursor, searching_phrase):
    query = ("""
        SELECT message, submission_time, question_id
        FROM comment
        WHERE message LIKE %(searching_phrase)s
        ORDER BY id DESC;
        """)
    cursor.execute(query, {"searching_phrase": f"%{searching_phrase}%"})
    return cursor.fetchall()


@database_common.connection_handler
def search_comment_by_id(cursor, question_id):
    query = ("""
        SELECT comment.id, comment.question_id, comment.answer_id, comment.message, comment.submission_time, 
        comment.edited_count, "user".username
        FROM comment
        LEFT JOIN public."user" ON comment.user_id = "user".id 
        WHERE question_id = %(question_id)s
        ORDER BY id ASC;
        """)
    cursor.execute(query, {"question_id": f"{question_id}"})
    return cursor.fetchall()


@database_common.connection_handler
def delete_comment_from_database(cursor, comment_id):
    query = """
        DELETE FROM comment
        WHERE id = %(comment_id)s"""
    cursor.execute(query, {'comment_id': comment_id})


@database_common.connection_handler
def get_id_list(cursor):
    query = ("""
        SELECT * FROM tag;
        """)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_comment_from_question(cursor, comment_id):
    query = """
        DELETE FROM comment
        WHERE id = %(comment_id)s"""
    cursor.execute(query, {'comment_id': comment_id})


@database_common.connection_handler
def login(cursor, username):
    query = """
    SELECT password, id
    FROM public.user
    WHERE username = %(username)s
    """
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


@database_common.connection_handler
def sort_questions_by_column_name_asc(cursor, column_name):
    query = sql.SQL("""
    SELECT id, submission_time,view_number,vote_number,title,message,image, votes_up, votes_down
    FROM question
    ORDER BY {column_name} ASC""").format(column_name=sql.Identifier(column_name))
    cursor.execute(query, {"column": column_name})
    return cursor.fetchall()


@database_common.connection_handler
def sort_questions_by_column_name_desc(cursor, column_name):
    query = sql.SQL("""
    SELECT id, submission_time,view_number,vote_number,title,message,image, votes_up, votes_down
    FROM question
    ORDER BY {column_name} DESC""").format(column_name=sql.Identifier(column_name))
    cursor.execute(query, {"column": column_name})
    return cursor.fetchall()


@database_common.connection_handler
def get_all_users(cursor):
    query = sql.SQL("""
    SELECT u.id, u.username, u.registration_date,u.reputation,COUNT(DISTINCT q.id) AS questions, COUNT(DISTINCT a.id) AS answers, COUNT(DISTINCT c.id) AS comments
    FROM public."user" AS u
    LEFT JOIN answer AS a
    on u.id = a.user_id
    LEFT JOIN question AS q 
    on q.user_id = u.id
    LEFT JOIN comment c 
    on u.id = c.user_id
    GROUP BY u.id
    ORDER BY u.id DESC
    """)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def create_account(cursor, username, password):
    query = """
        INSERT INTO public.user
        (username, password, registration_date)
        VALUES (%(username)s, %(password)s, NOW())"""
    cursor.execute(query, {'username': username, 'password': password})


@database_common.connection_handler
def get_user_data(cursor, user_id):
    query = """
        SELECT username, registration_date, reputation
        FROM public.user
        WHERE id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_user_question_data(cursor, user_id):
    query = """
        SELECT question.title, question.id
        FROM question
        INNER JOIN public.user
            ON question.user_id = public.user.id
        WHERE public.user.id = %(user_id)s
        GROUP BY question.title, question.id"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_user_answer_data(cursor, user_id):
    query = """
        SELECT answer.message, answer.question_id
        FROM answer
        INNER JOIN public.user
            ON answer.user_id = public.user.id
        WHERE public.user.id = %(user_id)s
        GROUP BY answer.message, answer.question_id"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_user_comment_data(cursor, user_id):
    query = """
        SELECT comment.message, comment.question_id
        FROM comment
        INNER JOIN public.user
            ON comment.user_id = public.user.id
        WHERE public.user.id = %(user_id)s
        GROUP BY comment.message, comment.question_id"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def find_user_id_by_username(cursor, username):
    query = """
        SELECT public.user.id, public.user.username
        FROM public.user
        WHERE username = %(username)s"""
    cursor.execute(query, {'username': username})
    return cursor.fetchall()


@database_common.connection_handler
def get_tags_with_counter(cursor):
    query = sql.SQL("""
    SELECT t.name as name, count(qt.question_id) AS questions_with_tag
    FROM question_tag AS qt
    RIGHT JOIN tag AS t
    ON qt.tag_id = t.id
    GROUP BY t.name
    """)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags(cursor, question_id):
    query = ("""
        SELECT t.name, t.id FROM question_tag AS qt
        LEFT JOIN tag AS t
        ON qt.tag_id = t.id
        WHERE qt.question_id = %(question_id)s ;
        """)
    cursor.execute(query, {"question_id": f"{question_id}"})
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag_list(cursor, question_id):
    query = ("""
        DELETE FROM question_tag
        WHERE question_id = %(question_id)s 
        """)
    cursor.execute(query, {"question_id": f"{question_id}"})


@database_common.connection_handler
def delete_tag(cursor, tag_id, question_id):
    query = ("""
    DELETE FROM question_tag
    WHERE tag_id = %(tag_id)s and question_id = %(question_id)s
    """)
    cursor.execute(query, {'tag_id': tag_id, 'question_id': question_id})


@database_common.connection_handler
def save_tag_list(cursor, question_id, tag_id):
    query = ("""
        INSERT INTO question_tag
        VALUES (%(question_id)s, %(tag_id)s);
        """)
    cursor.execute(query, {"question_id": f"{question_id}", "tag_id": f"{tag_id}"})


@database_common.connection_handler
def save_new_tag(cursor, name):
    query = ("""
    INSERT INTO tag (name)
    VALUES (%(name)s);
    """)
    cursor.execute(query, {'name': name})


@database_common.connection_handler
def count_rank_points(cursor, user_id):
    query = """
        SELECT SUM(public.question.votes_up * %(question_up)s + public.answer.votes_up * %(answer_up)s)+ 
        SUM(public.question.votes_down * %(question_down)s + public.answer.votes_down * %(answer_down)s) + 
        COUNT(public.answer.acceptation_status) * %(answer_accept)s as votes
        FROM public.answer
        INNER JOIN public.question on public.answer.question_id = question.id
        WHERE answer.user_id = %(user_id)s
        GROUP BY answer.user_id"""
    cursor.execute(query, {'user_id': user_id, 'question_up': CALC['question_up'], 'answer_up': CALC['answer_up'],
                           'question_down': CALC['question_down'], 'answer_down': CALC['answer_down'], 'answer_accept': CALC['answer_accept']})
    return cursor.fetchone()


@database_common.connection_handler
def get_all_usersnames(cursor):
    query = """
        SELECT id, "username"
        FROM "user"
        ORDER BY id DESC"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def count_answer_points(cursor, user_id):
    query = """
        SELECT SUM(public.answer.votes_up) * %(answer_up)s + SUM(public.answer.votes_down) * %(answer_down)s + 
        SUM(public.answer.acceptation_status) * %(answer_accept)s as a_points
        FROM public.answer
        WHERE answer.user_id = %(user_id)s
        GROUP BY answer.user_id;"""
    cursor.execute(query, {'user_id': user_id, 'answer_up': CALC['answer_up'], 'answer_down': CALC['answer_down'],
                           'answer_accept': CALC['answer_accept']})
    return cursor.fetchone()


@database_common.connection_handler
def count_question_points(cursor, user_id):
    query = """
        SELECT SUM(public.question.votes_up) * %(question_up)s + SUM(public.question.votes_down) * %(question_down)s as q_points
        FROM public.question
        WHERE question.user_id = %(user_id)s
        GROUP BY question.user_id;"""
    cursor.execute(query, {'user_id': user_id, 'question_up': CALC['question_up'], 'question_down': CALC['question_down']})
    return cursor.fetchone()


@database_common.connection_handler
def get_all_usersnames(cursor):
    query = """
        SELECT id, "username"
        FROM "user"
        ORDER BY id DESC"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def mark_acceptable_status(cursor, answer_id, bool_value):
    query = """
        UPDATE answer
        SET acceptation_status = %(bool_value)s
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'bool_value': bool_value, 'answer_id': answer_id})