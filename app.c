#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define INITIAL_MEMORY_MB 100
#define LEAK_MEMORY_MB 1024  // 1 GB
#define LEAK_CHUNK_MB 10
#define SLEEP_INTERVAL_SEC 1
#define DELAY_BEFORE_LEAK_SEC 60  // Delay before starting the memory leak

void start_memory_leak() {
    // Start leaking memory until 1 GB is leaked
    size_t total_leaked = 0;
    while (total_leaked < LEAK_MEMORY_MB * 1024 * 1024) {
        char *leak = malloc(LEAK_CHUNK_MB * 1024 * 1024);
        if (leak == NULL) {
            fprintf(stderr, "Failed to allocate leak memory\n");
            break;
        }
        memset(leak, 0, LEAK_CHUNK_MB * 1024 * 1024);
        total_leaked += LEAK_CHUNK_MB * 1024 * 1024;
        printf("Leaked %zu MB of memory\n", total_leaked / (1024 * 1024));
        sleep(SLEEP_INTERVAL_SEC);
    }
}

int main() {
    char *initial_memory = malloc(INITIAL_MEMORY_MB * 1024 * 1024);
    if (initial_memory == NULL) {
        fprintf(stderr, "Failed to allocate initial memory\n");
        return 1;
    }
    memset(initial_memory, 0, INITIAL_MEMORY_MB * 1024 * 1024);

    printf("Initial 100 MB of memory allocated. PID: %d\n", getpid());
    printf("Waiting for %d seconds before starting the memory leak...\n", DELAY_BEFORE_LEAK_SEC);

    sleep(DELAY_BEFORE_LEAK_SEC);

    // start_memory_leak();

    while (1) {
        sleep(10);
    }

    free(initial_memory);
    return 0;
}
