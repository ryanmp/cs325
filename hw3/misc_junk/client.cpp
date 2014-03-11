//============================================================================
// Name        : Client.cpp
// Author      : Joshua Villwock
// Version     :
// Copyright   : Your copyright notice
// Description : Finds Perfect Numbers, and sends them to a server.
//============================================================================

#include "stdinc.h"		//global includes here

using namespace std;	//namespace for ease of use

/* Define some port number that can be used for client-servers */
#define	SERV_PORT		 2541			/* TCP and UDP client-servers */
#define	SERV_PORT_STR	"2541"			/* TCP and UDP client-servers */

/* Miscellaneous constants */
#define	LISTENQ		1024	/* 2nd argument to listen() */
#define	MAXLINE		4096	/* max text line length */
#define	MAXSOCKADDR  128	/* max socket address structure size */
#define	BUFFSIZE	8192	/* buffer size for reads and writes */

//Global Variables
int each = 0;
int currNum = 0;

//Method Declarations
void signal_handler(int sigNum, int frame);
bool dealFoundPerfect(int num);
void dealKeepAlive(string payload);
void dealRangeAggignment(int beginning)
void findPerfectNumbers(int min, bool disable);
int calcSpeed();
void sendJson(int id, string payload);
void handle_close();
void handle_read(string JSON);

int main(int argc, char **argv){
	int	i;
	int sockfd[5];
	struct sockaddr_in	servaddr;
	char sendline[MAXLINE];
	char recvline[MAXLINE];


	if (argc != 2){
		perror("usage: client <IPaddress>");
		exit(-1);
	}

	for (i = 0; i < 5; i++) {
		sockfd[i] = socket(AF_INET, SOCK_STREAM, 0);

		bzero(&servaddr, sizeof(servaddr));
		servaddr.sin_family = AF_INET;
		servaddr.sin_port = htons(SERV_PORT);
		inet_pton(AF_INET, argv[1], &servaddr.sin_addr);

		connect(sockfd[i], (struct sockaddr *) &servaddr, sizeof(servaddr));
	}
	
	while (fgets(sendline, MAXLINE, stdin) != NULL) {
		
		write(sockfd[0], sendline, strlen(sendline));
		
		bzero(recvline, MAXLINE);

		if (read(sockfd[0], recvline, MAXLINE) == 0){
			perror("str_cli: server terminated prematurely");
			exit(-1);
		}
		
		fputs(recvline, stdout);
	}
	
	exit(0);
}
