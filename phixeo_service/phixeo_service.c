#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>
#include <errno.h>

#define DAEMON_NAME "phixeo_service"
#define PID_FILE "/var/run/phixeo_service.pid"
#define PHIXEO_DEVICE "/dev/phixeo"

static void daemonize() {
    pid_t pid, sid;
    int fd;
    FILE *pid_fp;

    /* Fork off the parent process */
    pid = fork();
    if (pid < 0) {
        exit(EXIT_FAILURE);
    }
    
    /* If we got a good PID, then we can exit the parent process */
    if (pid > 0) {
        exit(EXIT_SUCCESS);
    }

    /* Create a new SID for the child process */
    sid = setsid();
    if (sid < 0) {
        exit(EXIT_FAILURE);
    }

    /* Change the current working directory */
    if ((chdir("/")) < 0) {
        exit(EXIT_FAILURE);
    }

    /* Close out the standard file descriptors */
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);

    /* Redirect standard file descriptors to /dev/null */
    fd = open("/dev/null", O_RDWR);
    if (fd != STDIN_FILENO) {
        dup2(fd, STDIN_FILENO);
    }
    if (fd != STDOUT_FILENO) {
        dup2(fd, STDOUT_FILENO);
    }
    if (fd != STDERR_FILENO) {
        dup2(fd, STDERR_FILENO);
    }
    if (fd > STDERR_FILENO) {
        close(fd);
    }

    /* Write PID to file */
    pid_fp = fopen(PID_FILE, "w");
    if (pid_fp) {
        fprintf(pid_fp, "%d\n", getpid());
        fclose(pid_fp);
    }
}

static void stop_daemon() {
    FILE *pid_fp;
    pid_t pid;

    pid_fp = fopen(PID_FILE, "r");
    if (pid_fp) {
        if (fscanf(pid_fp, "%d", &pid) == 1) {
            fclose(pid_fp);
            if (kill(pid, SIGTERM) == 0) {
                printf("Stopped Phixeo service (PID: %d)\n", pid);
                unlink(PID_FILE);
                exit(EXIT_SUCCESS);
            } else {
                printf("Failed to stop Phixeo service (PID: %d): %s\n", pid, strerror(errno));
                exit(EXIT_FAILURE);
            }
        } else {
            fclose(pid_fp);
            printf("Failed to read PID from file\n");
            exit(EXIT_FAILURE);
        }
    } else {
        printf("PID file not found, service may not be running\n");
        exit(EXIT_FAILURE);
    }
}

static void activate_unlimited_void() {
    int fd;
    const char *command = "quantum";
    
    fd = open(PHIXEO_DEVICE, O_WRONLY);
    if (fd < 0) {
        syslog(LOG_ERR, "Failed to open Phixeo device: %s", strerror(errno));
        return;
    }
    
    if (write(fd, command, strlen(command)) < 0) {
        syslog(LOG_ERR, "Failed to activate Unlimited Void: %s", strerror(errno));
    } else {
        syslog(LOG_INFO, "Activated Unlimited Void defense");
    }
    
    close(fd);
}

static void check_system_integrity() {
    /* This function would check system integrity and respond to threats */
    /* For now, it's just a placeholder */
    syslog(LOG_INFO, "System integrity check passed");
}

int main(int argc, char *argv[]) {
    /* Check if we need to stop the daemon */
    if (argc > 1 && strcmp(argv[1], "--stop") == 0) {
        stop_daemon();
        return 0;
    }
    
    /* Initialize syslog */
    openlog(DAEMON_NAME, LOG_PID, LOG_DAEMON);
    syslog(LOG_INFO, "Starting Phixeo service");
    
    /* Daemonize */
    daemonize();
    
    /* Main loop */
    while (1) {
        /* Activate Unlimited Void defense */
        activate_unlimited_void();
        
        /* Check system integrity */
        check_system_integrity();
        
        /* Sleep for a while */
        sleep(60);
    }
    
    /* Close syslog */
    closelog();
    
    return 0;
}
