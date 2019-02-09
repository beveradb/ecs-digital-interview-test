
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

##### Language Choice
All of the languages allowed by the test requirements are more than capable for this purpose.
However, for a standalone script intended for execution as part of the software 
development lifecycle, I wanted something both:
1. Feature-rich, so I'm not reinventing the wheel too much and implementing my own 
   SQL client or pattern matching from scratch.
2. Portable, so the script can be useful to devs working from different operating systems.

Now, I've written my fair share of Bash scripts and they have their place, but shell 
scripting in general doesn't actually meet either of these requirements, so these 
should be avoided for anything more complex than system-specific automation tasks.

Between the three fully featured languages, Python has a clear advantage in portability,
as it is available out of the box in all major Linux distributions and on macOS.
It is also fairly common to see Python scripts in SDLC tooling alongside a codebase 
in another language, whereas choosing PHP or Ruby would be unusual unless the application
itself was built in one of those languages.

**Note:** The requirements explicitly reference Python 2.7, which is very bad practice 
now as the entire community is pushing to migrate away from the 2.x branch since 
it is being retired in less than 10 months (January 2020). I've written this solution
in Python 2.7 compatible code, but anyone still using it really needs to update now!

### Implementation

##### MySQL database, example SQL scripts
I set up a MySQL database on a remote host to run these on (ignoring SDLC best 
practices - for now this fictional dev team are deploying changes directly to production!),
and began creating SQL scripts to support the fictional scenario described above.

The scripts were then tweaked until there was a working set of migrations simulating the 
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
