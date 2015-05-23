# -*- coding: utf-8 -*-
#

import fource.parser.f_yaml
import fource.protocol.http
import fource.storage.mongo
import fource.template_engine.f_jinja2


PARSER_SELECT = {
    'yml': fource.parser.f_yaml.Parser,
}

STORAGE_SELECT = {
    'mongo': fource.storage.mongo.MongoStore,
}

PROTOCOL_SELECT = {
    'http': fource.protocol.http.HttpClass,
}

TEMPLATE_ENGINE = {
    'jinja2': fource.template_engine.f_jinja2.Jinja2Engine,
}


def execute(arguments):
    # import pdb; pdb.set_trace()
    StorageClass = STORAGE_SELECT.get('mongo')
    storage = StorageClass('localhost', 27017)
    template_engine = TEMPLATE_ENGINE.get('jinja2')()
    config_file = arguments.get('config')
    extension = config_file.split('.')[-1]
    ParserClass = PARSER_SELECT.get(extension)
    parser = ParserClass(config_file)
    task_list = parser.parse()
    for task in task_list:
        task_id = task.get('id')
        last_result = storage.get(task_id)
        task = template_engine.render_from_object(task, **last_result)
        protocol_name = task.get('protocol', 'http')
        ConnClass = PROTOCOL_SELECT.get(protocol_name)
        connection = ConnClass(task.get('parameters'))
        result = connection.execute()
        print '#'*80
        print result
        print '#'*80
        storage.save(task_id, result)
        print storage.get(task_id)
        print '#'*80
        # print protocol
    # print str(arguments)
