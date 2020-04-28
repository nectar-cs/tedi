[![codecov](https://codecov.io/gh/nectar-cs/teds/branch/master/graph/badge.svg)](https://codecov.io/gh/nectar-cs/teds)

Getting a running container:
`id=docker run -t -d -it teds`
`docker exec -it $id /bin/bash`

Or more directly 
`docker exec -it $(docker run -t -d -it teds) /bin/bash`


clone_into_dir = lambda: os.environ.get('CLONE_INTO_DIR', '/tmp/teds/in')
working_dir = lambda: os.environ.get('WORKING_DIR', '/tmp/teds/work')
in_repo_subpath = lambda: os.environ.get('REPO_SUBPATH', '')
repo_name = lambda: os.environ.get('REPO_NAME')
overrides_path = lambda: os.environ.get('OVERRIDES_PATH')
values_path = lambda: f"{working_dir()}/values.yaml"
