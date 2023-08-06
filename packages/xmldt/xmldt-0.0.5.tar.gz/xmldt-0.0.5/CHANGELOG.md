# Changelog

### 0.0.5 - January 24th

 - `pydt` new interface:
   - `-i` or `--indent` to indent function names
   - `-d` or `--debug` to activate debug
   - `-n` or `--name` to set the processor name
   - `-a` or `--average-pcdata` to compute pcdata average length
 - Fixed element.root accessor
 - Added support for custom class processing

### 0.0.4 - January 22nd

 - Renamed main class to XmlDt
 - Created class for parsing HTML: HtmlDt
 - Fixed behavior for 'zero' type

### 0.0.3 - January 20th

 - Added support for tag-names with non valid method characters
 - Added support for types
 - Added support for HTML files 
 - pydt: added support for multiple input files (pydt f1.xml f2.xml ...)
 - Added recovery flag
 - Added support for comments (ignored by default, but can be processed)

### 0.0.2 - January 4th

 - Fixed pydt command
 - Added support to the `@XMLDT.tag` decorator
 - Added tests to _Skel_ code
 - Support for `father` and `gfather` accessors

### 0.0.1

 - First version
