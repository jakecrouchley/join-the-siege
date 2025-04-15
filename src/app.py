from flask import Flask, request, jsonify
from src.classifier import classify_file
from src.models.file import UnprocessedFile, MissingFileException, InvalidFileTypeException

app = Flask(__name__)

@app.route('/classify_file', methods=['POST'])
def classify_file_route():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    try:
        unprocessed_file = UnprocessedFile(file)
    except MissingFileException as e:
        return jsonify({"error": str(e)}), 400
    except InvalidFileTypeException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

    processed_file = unprocessed_file.extract_text()
    file_class = classify_file(processed_file)
    return jsonify({"file_class": file_class}), 200


if __name__ == '__main__':
    app.run(debug=True)
