#!/bin/bash
# Inspired by 
# https://www.codeenigma.com/community/blog/using-mdbtools-nix-convert-microsoft-access-mysql

# USAGE
# Rename your MDB file to migration-export.mdb 
# run ./mdb2sqlite.sh migration-export.mdb
# wait and wait a bit longer...

mdb-schema migration-export.mdb sqlite > schema.sql
mkdir sqlite
mkdir sql
for i in $( mdb-tables migration-export.mdb ); do echo $i ; mdb-export -D "%Y-%m-%d %H:%M:%S" -H -I sqlite migration-export.mdb $i > sql/$i.sql; done

mv schema.sql sqlite
mv sql sqlite
cd sqlite

cat schema.sql | sqlite3 db.sqlite3

for f in sql/* ; do echo $f && (echo 'BEGIN;'; cat $f; echo 'COMMIT;') | sqlite3 db.sqlite3; done