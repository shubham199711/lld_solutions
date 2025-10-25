package java_solution.logger.log_handler.impl;

import java_solution.logger.Log;
import java_solution.logger.formatter.LogFormatter;
import java_solution.logger.log_handler.LogHandler;

import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class FileLogHandler extends LogHandler {
    LogFormatter logFormatter;
    String filePath;
    Lock lock;
    
    public FileLogHandler(LogFormatter logFormatter, String filePath){
        this.logFormatter = logFormatter;
        this.filePath = filePath;
        this.lock = new ReentrantLock();
    }

    @Override
    public void write(Log message) {
        this.lock.lock();
        try (FileWriter writer = new FileWriter(this.filePath, true)){
            writer.write(this.logFormatter.format(message) + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        } finally{
            this.lock.unlock();
        }
    }
}
