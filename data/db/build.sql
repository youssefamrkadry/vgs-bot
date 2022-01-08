CREATE TABLE IF NOT EXISTS members(
    MemberID integer PRIMARY KEY,
    UserID integer,
    Name text,
    Committee text,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS committees(
    CommitteeID integer PRIMARY KEY,
    CommitteeName text
);
