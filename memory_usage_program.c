#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define INITIAL_MEMORY_MB 100
#define TOTAL_MEMORY_MB 1124  // Initial 100 MB + additional 1024 MB
#define MEMORY_STEP_MB 10
#define SLEEP_INTERVAL_SEC 1
#define DELAY_BEFORE_INCREASE_SEC 60  // Delay before increasing memory usage

void increase_memory_usage() {
    // Increase memory usage until TOTAL_MEMORY_MB is reached
    size_t total_memory_allocated = INITIAL_MEMORY_MB * 1024 * 1024;
    while (total_memory_allocated < TOTAL_MEMORY_MB * 1024 * 1024) {
        char *additional_memory = malloc(MEMORY_STEP_MB * 1024 * 1024);
        if (additional_memory == NULL) {
            fprintf(stderr, "Failed to allocate additional memory\n");
            break;
        }
        memset(additional_memory, 0, MEMORY_STEP_MB * 1024 * 1024);
        total_memory_allocated += MEMORY_STEP_MB * 1024 * 1024;
        printf("Total memory allocated: %zu MB\n", total_memory_allocated / (1024 * 1024));
        sleep(SLEEP_INTERVAL_SEC);
    }
}

int main() {
    // Allocate initial 100 MB of memory
    char *initial_buffer = malloc(INITIAL_MEMORY_MB * 1024 * 1024);
    if (initial_buffer == NULL) {
        fprintf(stderr, "Failed to allocate initial memory\n");
        return 1;
    }
    memset(initial_buffer, 0, INITIAL_MEMORY_MB * 1024 * 1024);

    printf("Initial %d MB of memory allocated. PID: %d\n", INITIAL_MEMORY_MB, getpid());
    printf("Waiting for %d seconds before increasing memory usage...\n", DELAY_BEFORE_INCREASE_SEC);

    sleep(DELAY_BEFORE_INCREASE_SEC);

    // increase_memory_usage();

    while (1) {
        sleep(10);
    }

    free(initial_buffer);
    return 0;
}
