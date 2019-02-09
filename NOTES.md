
## Notes

This is where I'll be documenting my own thought process and technical 
choices while implementing this solution, with review and conclusion once 
complete.

### Problem Overview

At first glance, this looks like we're reinventing the wheel and 
implementing a home-baked database migrations solution.
The approach required by the problem  using the intuitive 
(but naive) approach of running SQL scripts in sequence, keeping track of 
current database state using a simple version number stored in the database 
itself.

