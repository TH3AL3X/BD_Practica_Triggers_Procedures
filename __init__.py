from views import app
import db.config as config

if __name__ == '__main__':
    # 0 = mariadb completed
    # 1 = sqlite not completed
    # 2 = mysql not completed and fixed
    config.Config.DB_SELECTED = config.Config.DB_TYPES[0]
    app.config.from_object(config.Config())
    app.run(debug=app.config['DEBUG'])