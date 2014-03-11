#ifndef STDINC_H_
#define STDINC_H_

#define _BSD_SOURCE

#define HELP "\nCorrect Program Usage:\nPrime [<number of workers >] [<type of workers>]\nNumber of workers will be assumed to be 10 if not specified\nType will be assumed to be Threads if not specified\n\nExamples of correct usage:\nPrime 10 threads\nPrime 5 processes\n"

#include <sys/types.h>	/* basic system data types */
#include <sys/time.h>	/* timeval{} for select() */

#include <sys/socket.h>	/* basic socket definitions */
#include <time.h>		/* timespec{} for pselect() */
#include <netinet/in.h>	/* sockaddr_in{} and other Internet defns */
#include <arpa/inet.h>	/* inet(3) functions */
#include <fcntl.h>		/* for nonblocking */
#include <netdb.h>
#include <sys/wait.h>
#include <sys/select.h>
#include <sys/stat.h>	/* for S_xxx file mode constants */
#include <sys/uio.h>		/* for iovec{} and readv/writev */

#include <signal.h>
#include <unistd.h>

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

#include <iostream>
#include <stdlib.h>
#include <errno.h>
#include <math.h>
#include <limits.h>
#include <float.h>
#include <string>
#include <strings.h>     /* for bzero */

#include <boost/thread.hpp>
#include <boost/foreach.hpp>

using boost::thread;
using boost::thread_group;

#endif /* STDINC_H_ */
