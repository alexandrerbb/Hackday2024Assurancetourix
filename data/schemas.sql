-- Schema migrations.

CREATE TABLE IF NOT EXISTS "customermessage" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "message" TEXT NOT NULL,
    "time" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "option_id" VARCHAR(25) NOT NULL REFERENCES "ticketresponseoption" ("name") 
        ON DELETE CASCADE,
    "ticket_id" INT NOT NULL REFERENCES "ticket" ("id") ON DELETE CASCADE
) /* A message from a customer to the customer service. */;

CREATE TABLE IF NOT EXISTS "customermessageresponse" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "message" TEXT NOT NULL,
    "responds_to_id" VARCHAR(25) NOT NULL REFERENCES "ticketresponseoption" ("name") 
        ON DELETE CASCADE
) /* A response to a customer message dependending on its selected option. */;

CREATE TABLE IF NOT EXISTS "ticket" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "owner_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
) /* A ticket (a full exchange) to the ticket support. */;

CREATE TABLE IF NOT EXISTS "ticketresponseoption" (
    "name" VARCHAR(25) NOT NULL  PRIMARY KEY,
    "description" TEXT NOT NULL,
    "start_exchange" INT NOT NULL  DEFAULT 0,
    "ticket_response_id" INT REFERENCES "customermessageresponse" ("id") 
        ON DELETE CASCADE
) /* Response options for a specified response to a customer message. */;

CREATE TABLE IF NOT EXISTS "user" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "username" VARCHAR(30) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL,
    "send_secret_message" INT NOT NULL  DEFAULT 0
) /* An API user. */;