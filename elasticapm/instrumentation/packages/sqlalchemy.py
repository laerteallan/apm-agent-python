from elasticapm.instrumentation.packages.dbapi2 import DbApi2Instrumentation, extract_signature
from elasticapm.traces import capture_span
from sqlalchemy.sql.selectable import Select


class SqlalchemyInstrumentation(DbApi2Instrumentation):
    name = "sqlalchemy"

    instrument_list = [("sqlalchemy.engine.base", "Connection.execute"),
                       ]

    def __extra_data(self, instance, query):
        database = instance.engine.name
        driver = instance.engine.driver
        data = {"query": query,
                "database": database,
                "driver": driver}
        return data

    def call(self, module, method, wrapped, instance, args, kwargs):
        if args:
            first_arg = args[0]
            if isinstance(first_arg, Select):
                query = str(first_arg)
                signature = extract_signature(query)
                data = self.__extra_data(instance, query)
                with capture_span(signature, "query", data, leaf=True):
                    return wrapped(*args, **kwargs)

        return wrapped(*args, **kwargs)
