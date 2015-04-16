# csql2mongo
[![Build Status](https://travis-ci.org/stpettersens/csql2mongo.svg?branch=master)](https://travis-ci.org/stpettersens/csql2mongo) 
<!--[![Build status](https://ci.appveyor.com/api/projects/status/github/stpettersens/cmongo2sql?branch=master&svg=true)](https://ci.appveyor.com/project/stpettersens/cmongo2sql)-->

Utility to convert a SQL dump to a MongoDB JSON dump.
For migrating data from MySQL or similar RDBMS to MongoDB.

Usage: `csql2mongo -f data.sql -o data.json`

Tested with:
* Python 2.7.9, PyPy 2.5.1 and IronPython 2.7.5 (works).
* Jython 2.5.3 (use Jython tweaked version): 
* `jython cmongo2sql.jy.py -f data.json -o data.sql`)
