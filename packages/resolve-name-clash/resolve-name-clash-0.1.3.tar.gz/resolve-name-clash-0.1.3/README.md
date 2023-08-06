# resolve-name-clash

Say you want to copy file `a.txt` into directory `/path/to/destination/` but if `/path/to/destination/a.txt` exists, you don't want to overwrite it but instead copy the file to `/path/to/destination/a_1.txt`. This is a simple utility that does exactly one thing: given a source filename and a destination directory, it figures out a form of the source file's name in the destination directory that doesn't clash with any existing file. 

The algorithm it uses to find a unique filename is as follows. Given a path to a source file and a path to a destination directory:
* Set `src_filename` to the filename (last path segment) of the path to the source file
* If `path/to/dest/src_filename` does not exist, return it
* If `path/to/dest/src_filename` exists:
  * Set `src_file_basename` to `src_filename` with all the extensions removed and `src_file_extensions` to all the extensions of `src_filename`
  * Successively try `path/to/dest/src_file_basename + "_1" + src_file_extensions`, `path/to/dest/src_file_basename + "_2" + src_file_extensions`, and so on until one is found that doesn't exist. Return that one.

You can use it on the command line: 
```
$ resolve-name-clash ~/src/a.txt ~/dest/
/Users/spather/dest/a_1.txt
```

It's particularly useful used in a subshell with a copy or move command:
```
cp ~/src/a.txt $(resolve-name-clash ~/src/a.txt ~/dest)
```

Or you can us it in a python program:

```python
from resolve_name_clash import resolve_name_clash

src = Path("/path/to/src/a.txt")
dest = Path("/path/to/dest")
unique_path = resolve_name_clash(src, dest)
# unique_path will be a Path object to something like /path/to/dest/a_1.txt
```
