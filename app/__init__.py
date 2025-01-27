from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    # Import blueprints if you plan to modularize routes later
    from app.face_recognition import register_user, verify_user
    from app.voting import process_vote
    from app.blockchain_utils import register_on_blockchain, record_vote

    # Register routes if using blueprints (Optional)
    # from app.routes import main
    # app.register_blueprint(main)

    return app
