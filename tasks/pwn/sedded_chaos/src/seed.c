#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/time.h>

#define FLAG_FILE "flag.txt"

void timeout_handler(int sig) {
    printf("Timeout! Connection closed.\n");
    fflush(stdout);
    _exit(1);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    signal(SIGALRM, timeout_handler);
    alarm(3);

    srand(time(NULL) ^ getpid());
    int delay = rand() % 3 + 1;
    sleep(delay);
    time_t ts = time(NULL);
    unsigned int seed = ts;
    seed ^= (seed << 13);
    seed ^= (seed >> 7);
    seed += 0x12345678;
    seed ^= (seed * 0x1337);
    seed = ((seed * 0xdeadbeef) ^ (seed >> 3)) + 0x1337;
    srand(seed);
    unsigned long long secret = ((unsigned long long)rand() << 32) | rand();

    char guess[32];
    printf("Guess a 64-bit number: ");
    gets(guess);

    alarm(0);

    unsigned long long user_guess;
    sscanf(guess, "%llx", &user_guess);

    if (user_guess == secret) {
        FILE *fp = fopen(FLAG_FILE, "r");
        if (fp) {
            char flag[128];
            fgets(flag, sizeof(flag), fp);
            printf("Your flag: %s", flag);
            fclose(fp);
        } else {
            printf("Error reading the flag!\n");
        }
    } else {
        printf("Oh no, how so :(\n");
    }
    return 0;
}
