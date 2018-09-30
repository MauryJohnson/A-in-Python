Server Control and Server State should always run at the start.

If Server Control shuts off, this means that robot has collided with obstacle
Also this can be confirmed by calling turtlebot_Mclient.py and receiving service "unavailable" message

If that happens, must restart program and try again, Call Function which starts
these processes again and kills the old processes. Can use command or pipe(pipe preferred)

Server State and Server Control should run until all maps have been used
