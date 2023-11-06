docker_config = {
    'detach': True,
    # 'command': 'sleep infinity',
    'image': 'python_cl_img',
    # 'remove': False,
    'tty': True,
    # 'name': 'C1',
    'volumes': {
        '/volum': {
            'bind': '/app/vol',
            'mode': 'rw'
        }
    }
}

docker_config_js = {
    'detach': True,
    # 'command': 'sleep infinity',
    'image': 'node_cl_img',
    # 'remove': False,
    'tty': True,
    # 'name': 'C1',
    'volumes': {
        '/volum': {
            'bind': '/app/vol',
            'mode': 'rw'
        }
    }
}

docker_config_ruby = {
    'detach': True,
    # 'command': 'sleep infinity',
    'image': 'ruby_cl_img',
    # 'remove': False,
    'tty': True,
    # 'name': 'C1',
    'volumes': {
        '/volum': {
            'bind': '/app/vol',
            'mode': 'rw'
        }
    }
}