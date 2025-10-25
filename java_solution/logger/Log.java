package java_solution.logger;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;


public class Log {
    String message;
    LogLevel logLevel;
    String time;

    Log(String message, LogLevel logLevel){
        this.message = message;
        this.logLevel = logLevel;
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        this.time = formatter.format(LocalDateTime.now());
    }

    @Override
    public String toString() {
        return this.time + " " + "[" + this.logLevel.getName() + "]: " + this.message;
    }

    public String getMessage() {
        return this.message;
    }

    public LogLevel getLogLevel() {
        return this.logLevel;
    }

    public String getTime() {
        return this.time;
    }
}
