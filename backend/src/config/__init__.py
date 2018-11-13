import os

class ShakuntlaDeviConfig(object):

    # Restplus
    RESTPLUS_VALIDATE = True

    @staticmethod
    def get_config():
        """Gets the config on basis of the `SD_ENVIRONMENT` environment variable.
        Possible values of the env variable are:
        1. `PRODUCTION`
        2. 'STAGING'
        3. `DEVELOPMENT`

        This method will also try to import ProductionConfig (from config.production),
        StagingConfig (from config.staging) & DevelopmentConfig (from config.development)
        and throw an exception in case it is not able to import any one of them. This is
        important as all of these files (`config/staging.py`, `config/development.py`,
        `config/production.py`) will be in .gitignore to ensure security.


        *Note:* This also checks that value of SD_ENVIRONMENT and FLASK_ENV should be the same.

        Return:
        A config class object which will be an instance of ShakuntlaDeviConfig.
        """

        # get the SD_ENVIRONMENT environment variable
        mode = os.environ.get('SD_ENVIRONMENT')
        if mode not in ['production', 'development', 'staging']:
            raise Exception('`SD_ENVIRONMENT` environment variable is either set incorrectly or not set.')

        # get the FLASK_ENV environment variable
        flask_env = os.environ.get('FLASK_ENV')
        if flask_env != mode:
            raise Exception('The values of `FLASK_ENV` and `SD_ENVIRONMENT` need to be the same.')

        # get the required config as per environment variable
        if mode == "PRODUCTION":
            from .production import ProductionConfig
            Config = ProductionConfig
        elif mode == "STAGING":
            from .staging import StagingConfig
            Config = StagingConfig
        else:
            from .development import DevelopmentConfig
            Config = DevelopmentConfig

        # check if the imported class is an instance of ShakuntlaDeviConfig
        if issubclass(Config, ShakuntlaDeviConfig):
            return Config()
        else:
            raise Exception("The imported config is not a subclass of `ShakuntlaDeviConfig`")
