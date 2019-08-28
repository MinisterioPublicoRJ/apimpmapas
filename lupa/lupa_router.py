class LupaRouter:
    """
    Router para controlar operações de banco de dados no app Lupa.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'lupa':
            return 'default'
        return None
