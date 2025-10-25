package java_solution.logger;

public enum LogLevel {
    INFO("INFO", 1),
    DEBUG("DEBUG", 2),
    WARN("WARN", 3),
    ERROR("ERROR", 4);

    private final String name;
    private final int severity;

    LogLevel(String name, int severity) {
        this.name = name;
        this.severity = severity;
    }

    public String getName() {
        return name;
    }

    public int getSeverity() {
        return severity;
    }
}
