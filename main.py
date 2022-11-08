from flask import Flask
from flask_restful import Resource, Api, reqparse
from PyPDF2 import PdfReader, PdfWriter


app = Flask(__name__)
api = Api(app)

rotate_pdf_parser = reqparse.RequestParser()
rotate_pdf_parser.add_argument('file_path')
rotate_pdf_parser.add_argument('angle_of_rotation')
rotate_pdf_parser.add_argument('page_number')


class Rotate(Resource):

    # method to rotate pdf pages
    def get(self):
        args = rotate_pdf_parser.parse_args()
        file_path = args.get("file_path", None)
        page_number = args.get("page_number", None)
        angle_of_rotation = args.get("angle_of_rotation", None)

        page_number = int(page_number)
        angle_of_rotation = int(angle_of_rotation)

        # read the pdf file using the file path
        reader = PdfReader(f'.{file_path}')

        # get number of pages in the pdf file
        number_of_pages = reader.getNumPages()

        if page_number > number_of_pages or page_number < 1:
            return {"message": "Invalid page number"}, 400

        writer = PdfWriter()

        # rotate the pdf page
        for i in range(number_of_pages):
            if i == page_number-1:
                writer.add_page(reader.pages[i].rotate(angle_of_rotation))
            else:
                writer.add_page(reader.pages[i])

        # write to the file
        with open("./tmp/rotated_test.pdf", "wb") as file:
            writer.write(file)

        return {"message": "PDF rotated"}


api.add_resource(Rotate, '/')

if __name__ == '__main__':
    app.run(debug=True)
