
Getting a running container:
`id=docker run -t -d -it teds`
`docker exec -it $id /bin/bash`

Or more directly 
`docker exec -it $(docker run -t -d -it teds) /bin/bash`