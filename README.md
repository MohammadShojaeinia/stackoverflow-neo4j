## Import stackexchange in neo4j

It's a fork from https://github.com/mdamien/stackoverflow-neo4j

steps:
- Use python 3
- Download the dump from archive.org: https://archive.org/details/stackexchange
- extract the community you want in `extracted/`, like `Posts.xml` or `Users.xml`
- you need to `sudo pip install xmltodict`
- `python to_csv.py extracted/` to get the csvs in `csvs/`
- delete your `graph.db` directory (or rename it to another name, if don't want to lose your old data)
- use `windows commant.bat` to import the csvs in neo4j (It's better to copy command in `CMD` or `Power Shell` in bin directory of neo4J on your computer)

Look at the scripts before using them to understand what they do :)

*Have fun!*
