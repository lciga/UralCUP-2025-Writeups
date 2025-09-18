#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/types.h>

char global_buf[0x100];

void *bankai(void *arg) {
    sleep(1);
    puts("Byakuya uses Senbonzakura Kageyoshi!");
    for (int i = 5; i >= 0; --i) {
        sleep(1);
        printf("%d... ", i);
    }
    puts("The petals of his blade surround you...");
    sleep(1);
    puts("Byakuya ends the battle...");
    system("kill -9 $PPID");
    return NULL;
}

char *safe_fgets(char *buf, size_t size, FILE *stream) {
    memset(buf, 0, size);
    if (!fgets(buf, size, stream)) {
        perror("fgets");
        exit(1);
    }
    buf[strcspn(buf, "\r\n")] = 0;
    return buf;
}

void filter(const char *payload) {
    size_t len = strlen(payload);
    for (size_t i = 0; i < len; ++i) {
        if (payload[i] != '%' && payload[i] != 'p' && payload[i] != '.') {
            puts("No no no no! Too complicated for me...");
            exit(1);
        }
    }
}

int main(int argc, char **argv, char **envp) {
    char payload[64];

    setvbuf(stdout, NULL, _IONBF, 0);

    puts("You stand before Byakuya Kuchiki. It's time to reveal your Bankai!");
    puts("Show your power. Unleash your Bankai!");
    printf("Your Bankai: ");
    safe_fgets(payload, sizeof(payload), stdin);
    filter(payload);
    puts("Byakuya judges your Bankai...");
    printf(payload);
    putchar('\n');

    pthread_t thread;
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    puts("The dust settles after a burst of spiritual energy...");
    sleep(1);
    puts("You and Byakuya stare at each other...");
    sleep(1);
    puts("Suddenly, Byakuya activates his Bankai!");
    sleep(1);

    pthread_create(&thread, NULL, bankai, NULL);

    sleep(1);
    printf("Shout the name of your Bankai! ");
    gets(global_buf);
    printf("You shout: %s\nByakuya watches to see if you survived his attack...\n", global_buf);
    sleep(1);
    puts("You're still standing! Byakuya is surprised.");
    printf("Now it's your turn to attack! Enter your command: ");
    gets(global_buf);
    system(global_buf);

    return 0;
}