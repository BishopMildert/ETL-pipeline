# ETL Refactoring
This project is to be updated soon.

### Definition of Done
**For Code**
1. The code can carry out it's intended functionality
2. It has been thoroughly tested
3. Integration has been performed so it gets the information required to work

**For Tickets**
1. Ticket is added to the "In Review" card
2. Item is peer-reviewed by another member to ensure the task is complete to a high standard
3. Ticket is moved into the "Done" card

### Branch Structure
1. Master branch is the up-to-date and stable branch
2. Testing branch is the unstable branch where peer-reviewed integration tests take place
3. Feature branches will be used by one person to create and test features

When feature branches are considered done, they will be merged into the testing branch where a
peer-review process of the feature and it's integration will take place.

### Setting Up The .env File
The .env file must contain the following fields to allow for the docker containers to connect correctly;

1. POSTGRESQL_PASSWORD
2. POSTGRES_USER

These variable names are case sensitive so must be in all caps.

### New readme notes for refactoring of code:
The files have been rewritten to keep the 3 stages of ETL into 3 functions of extract transform and load.
These can be seen in src/extract.py, src/transform.py, and src/new_load.py respectively
Current improvements that can be made are:
1. row value validation and data cleaning. an example of this is connecting the check_datetime() from transform so that all datetime cells are checked to make sure they are in the right format
2. Unit testing for most functions to be done. (Possibly worth going through in the order of Extract transform and Load in the order that funcitons are called? I checked extract and the test was broken due to a syntax error so definitely needs work
3. End to end testing written (Can come after unit tests though)
4. Cleaning of codebase. Currently the code is very rudimentary and not well documented / commented.
