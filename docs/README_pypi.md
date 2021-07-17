# ppf.jabref

ppf.jabref provides a [python](https://www.python.org) interface to
[JabRef](https://www.jabref.org) SQL databases. It maps database relations
to python classes using [SQLAlchemy](https://www.sqlalchemy.org).
Also, ppf.jabref provides tools to parse the data stored inside the 
database tables.


## Using ppf.jabref

ppf.jabref relies on SQLAlchemy for database access. All that ppf.jabref
adds to this is a data model which makes sqlalchemy understand how a 
JabRef database is structured (by providing classes Entry and Field).

A simple example that queries all entries and prints a selection of
the fields looks like this:

```python
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from ppf.jabref import Entry, File

    engine = create_engine('<your connection string here>', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    q = session.query(Entry)
    for entry in q:
        print(entry.fields['author'], '\t',
            entry.fields['title'], '\t',
            entry.fields['year'], '\t', end='')

        files = File.from_string(entry.fields['file'])
        for i in range(len(files)):
            f = files[i]
            print(f.path, '\t', end='')
```

The first 6 lines are setup code to import required packages and to set up
the database connection. The query then uses ppf.jabref's Entry class to
obtain all Entries (=references) in the JabRef database. The for-loop
shows how to access fields and uses the File class to find out where the
documets linked to this entry are stored.
