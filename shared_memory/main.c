
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

#include <string.h>
#include <unistd.h>

void *create_shared_memory(size_t size);

int main()
{
    char parent_message[] = "parent message";  // parent process will write this message
    char child_message[] = "child message"; // child process will then write this one

    printf("hello world\n");
    void *shmem = create_shared_memory(2000);

    memcpy(shmem, parent_message, sizeof(parent_message));

    int pid = fork();

    if (pid == 0)
    {
        printf("Child read: %s\n", (char *)shmem);
        memcpy(shmem, child_message, sizeof(child_message));
        printf("Child wrote: %s\n", (char *)shmem);
    }
    else
    {
        printf("Parent read: %s\n", (char *)shmem);
        sleep(1);
        printf("After 1s, parent read: %s\n", (char *)shmem);
    }
}



void *create_shared_memory(size_t size)
{
    // Our memory buffer will be readable and writable:
    int protection = PROT_READ | PROT_WRITE;

    // The buffer will be shared (meaning other processes can access it), but
    // anonymous (meaning third-party processes cannot obtain an address for it),
    // so only this process and its children will be able to use it:
    int visibility = MAP_SHARED | MAP_ANONYMOUS;

    // The remaining parameters to `mmap()` are not important for this use case,
    // but the manpage for `mmap` explains their purpose.
    return mmap(NULL, size*sizeof(int), protection, visibility, -1, 0);
    // char *tab = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED , -1, 0);
    // return tab;

}
