from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


def homepage() -> str:
    return """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Hello World</title>
    <script src="https://unpkg.com/react@16/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@16/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/react-beautiful-dnd@10.x/dist/react-beautiful-dnd.js"></script>
    <!--<script src="./dist/main.js"></script>-->
    <style>
    #root {
        display: flex;
        justify-content: space-between;
    }
    </style>
    <!-- Don't use this in production: -->
    <script src="https://unpkg.com/babel-standalone@6.x/babel.min.js"></script>
  </head>
  <body>
    <div id="root"></div>
    <script type="text/jsx" src="js/list.jsx"></script>
    <!--
      Note: this page is a great way to try React but it's not suitable for production.
      It slowly compiles JSX with Babel in the browser and uses a large development build of React.

      Read this section for a production-ready setup with JSX:
      https://reactjs.org/docs/add-react-to-a-website.html#add-jsx-to-a-project

      In a larger project, you can use an integrated toolchain that includes JSX instead:
      https://reactjs.org/docs/create-a-new-react-app.html

      You can also use React without JSX, in which case you can remove Babel:
      https://reactjs.org/docs/react-without-jsx.html
    -->
  </body>
</html>

"""


@app.route("/")
def home():
    return homepage()


if __name__ == "__main__":
    app.run()
