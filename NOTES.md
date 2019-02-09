
## Notes

This is where I'll be documenting my own thought process and technical 
choices while implementing this solution, with review and conclusion once 
complete.

### Problem Overview

At first glance, this looks like we're implementing a home-baked database migrations solution.
This is reinventing the wheel somewhat, as there are a wide variety of existing, mature 
options for handling database migrations which will be far more robust and future-proof 
(typically built into ORMs, e.g. SQLAlchemy in Python, Doctrine in PHP or Active Record in Ruby).
However, since this is a test with fixed requirements, let's pretend these don't exist
and we're inventing the concept of migrations for the first time.

The approach required by the problem definition is to use the intuitive (but naive) 
approach of running SQL scripts in sequence, keeping track of current database state using 
a simple version number stored in the database itself to track the most recent script run.

### Approach

##### Fictional scenario
To make it easier to make sensible assumptions for this use case, I decided to imagine 
this was being implemented by a developer who was part of a small and inexperienced team 
working on a web application for a furniture store.

Ths fictional dev team aren't sure of all the requirements, yet as the store owner
is still deciding various things! As such, they're pretty much designing the database schema
and application architecture on the fly - a situation where handling migrations well
is essential!

##### MySQL database, example SQL scripts
I set up a MySQL database on a remote host to run these on (ignoring SDLC best 
practices - for now this fictional dev team are deploying changes directly to production!),
and began creating SQL scripts to support the fictional scenario described above.

I tweaked the scripts until there was a working set of migrations simulating the 
progressive design and creation of a handful of semi-realistic tables:

![Schema Diagram](https://raw.githubusercontent.com/beveradb/ecs-digital-interview-test/master/schema-diagram.jpg "Schema Diagram")


##### Filename inconsistency
To meet the test requirements, I introduced a bit of human error / inconsistency in the 
filenames, as if these were being created by hand by careless developers.
They technically all start with a number, but these aren't sequential (which could easily
happen if the devs were attempting to collaborate in branches without good communication or 
any other tooling in their development process).
The filename patterns aren't consistent either, with a mix of hyphens, underscores, dots 
and spaces separating parts.
