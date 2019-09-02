class Router:
    """
    Router para controlar operações de banco de dados.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read from mprj_plus should go to mprj_plus dbase
        Any other reading should go to default
        """
        if model._meta.app_label == 'mprj_plus':
            return 'mprj_plus'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write from mprj_plus should go to mprj_plus dbase
        Any other writing should go to default
        """
        if model._meta.app_label == 'mprj_plus':
            return 'mprj_plus'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        No cross-database relation should be allowed.
        (At least at this point - later releases may change it)
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        The app mprj_plus should migrate on the mprj_plus db.
        Any other apps should migrate on the default db.
        """
        if app_label == 'mprj_plus':
            return db == 'mprj_plus'
        return db == 'default'
