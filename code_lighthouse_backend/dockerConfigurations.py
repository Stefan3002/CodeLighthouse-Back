docker_config = {
    'detach': True,
    # 'command': 'sleep infinity',
    'image': 'img',
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