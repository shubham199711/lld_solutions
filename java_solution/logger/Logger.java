package java_solution.logger;

import java.util.HashSet;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import java_solution.logger.log_handler.LogHandler;


public class Logger {
    LogLevel level;
    Lock lock;
    HashSet<LogHandler> hanlder;
    
    Logger(LogLevel level){
        this.level = level;
        this.lock = new ReentrantLock();
        this.hanlder = new HashSet<>();
    }

    void addHandler(LogHandler newLogHandler){
        this.hanlder.add(newLogHandler);
    }

    void log(String message, LogLevel level){
        if(level.getSeverity() < this.level.getSeverity()){
            return;
        }
        Log newLog = new Log(message, level);
        this.lock.lock();
        try {
            for (LogHandler logHanlder : this.hanlder) {
                logHanlder.write(newLog);
            }
        } finally {
            this.lock.unlock();
        }
    }

    void debug(String message){
        this.log(message, LogLevel.DEBUG);
    }

    void info(String message){
        this.log(message, LogLevel.INFO);
    }

    void warning(String message){
        this.log(message, LogLevel.WARN);
    }

    void error(String message){
        this.log(message, LogLevel.ERROR);
    }

}
