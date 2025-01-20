import os
import uuid

from flask import Flask

from app.detector import FujifilmRecipeDetector

detector = FujifilmRecipeDetector()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.post("/predict")
    def predict():
        from flask import request

        image = request.files["image"].read()

        image_path = uuid.uuid4().hex + ".jpg"

        with open(image_path, "wb") as f:
            f.write(image)

        result = detector.predict(image_path)

        os.remove(image_path)

        print(result)
        return result

    return app
