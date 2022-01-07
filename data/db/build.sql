CREATE TABLE IF NOT EXISTS exp(
    UserID integer PRIMARY KEY,
    XP integer ,
    Level integer,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);
