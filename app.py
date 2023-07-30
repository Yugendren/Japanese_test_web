from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tB7225041@',
    'database': 'mydatabase'
}

# Fetch kanji data from the database
def fetch_kanji_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT kanji_character, meaning FROM kanji")
    kanji_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return kanji_data

# Fetch example sentences and answers from the database
# Fetch example sentences from the database
def fetch_example_sentences():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT sentence FROM example_sentences")
    example_sentences = cursor.fetchall()
    cursor.close()
    conn.close()
    return example_sentences

# Fetch test answers from the database
def fetch_test_answers():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM test_answers")
    test_answers = cursor.fetchall()
    cursor.close()
    conn.close()
    return test_answers

@app.route('/')
def index():
    kanji_data = fetch_kanji_data()
    return render_template('index.html', kanji_data=kanji_data)

@app.route('/meaning/<kanji_id>')
def meaning(kanji_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT kanji_character, meaning, furigana FROM kanji WHERE kanji_character = %s", (kanji_id,))
    result = cursor.fetchone()
    kanji_character = result[0] if result else 'Kanji not found.'
    meaning = result[1] if result else 'Meaning not found.'
    furigana = result[2] if result else 'Furigana not found.'
    cursor.close()
    conn.close()
    return render_template('meaning.html', kanji_character=kanji_character, meaning=meaning, furigana=furigana)


@app.route('/test')
def test():
    example_sentences = fetch_example_sentences()
    test_answers = fetch_test_answers()
    return render_template('test.html', sentences=example_sentences, answers=test_answers)


@app.route('/test_result', methods=['POST'])
def test_result():
    score = 0
    example_sentences = fetch_example_sentences()
    for sentence in example_sentences:
        answer = request.form.get(sentence[0])
        if answer and answer.strip().lower() == sentence[0].lower():
            score += 1
    return render_template('test_result.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
