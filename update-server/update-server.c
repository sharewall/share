#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>
#include <curl/curl.h>

void doSomeWork(void){

  //const int NUM_TIMES = 5;
  const int sleepValue = 10;

  CURL *curl;// = curl_easy_init();
  CURLcode res;
  const char *url = "http://share.loc/webmaster-area/thu-may/555/update-server/";
     
  //for(int i=0; i < NUM_TIMES; i++){
    //int sleepValue = (int)(rand() % 4);//(rand % 4)from 0 to 3
  for(int i=0;;i++){
    curl = curl_easy_init();

    if(curl){
      curl_easy_setopt(curl, CURLOPT_URL, url);
      /* example.com is redirected, so we tell libcurl to follow redirection */ 
      curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
      /* Perform the request, res will get the return code */ 
      printf("curl %s\nResponse: ", url);
      res = curl_easy_perform(curl);
      printf("\n");
      /* Check for errors */ 
      if(res != CURLE_OK)
        fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
       
      /* always cleanup */ 
      curl_easy_cleanup(curl);
    }

    sleep(sleepValue);
    printf("Done pass %d, sleepValue: %d\n", i, sleepValue);
  }
}

int main(int argc, char *argv[]){

  printf("\n");
  printf("I am: %d\n", (int)getpid());

  pid_t pid = fork();//If we call fork in cycle, need to be very carefull, or we truncate system by fork BOMB!
  time_t t;//time for srand(seed)
  srand((unsigned)time(&t));//srand() for rand()
  printf("Fork returned: %d\n", (int)pid);

  if(pid < 0){
    perror("Fork failed");
  }

  if(pid == 0){
    printf("I am child created by fork, and my pid: %d\n", (int)getpid());
    printf("Child running...\n");
    //sleep(5);//sleep(n), n in sec
    //printf("Child ending\n");
    setpgid(0,0);//chgroup to make background process
    doSomeWork();
    exit(0);//exit(n), n = Any of integer value, 0 = by default success
  }
  //if in child call exit(0), we exactly know what we are parent in this phase:
  //else{
    printf("I am parent, and i waiting for child end. My pid: %d\n", (int)getpid());
    //int status = 0;
    //pid_t pidChild = wait(&status);//pidChild = Id for child, status = returned status from child. WEXITSTATUS(status) = macro for get correct status
    wait(NULL);// IF we dont use wait in parent, we can get ZOMBIE process, in ps -a marked like <defunct>
    printf("Parent ending\n");
  //}

  //printf("I am: %d\n", (int)getpid());

  return 0;
}
