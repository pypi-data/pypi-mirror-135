# jsw-nx
> Next toolkit for python.

## installation
```shell
pip install jsw-nx
```

## usage
```python
import jsw_nx as nx

## common methods
nx.includes([1,2,3], 2) # => True
nx.includes([1,2,3], 5) # => False
```

## next core methods
- base/filter
- base/find
- base/find_index
- base/foreach
- base/forin
- base/get
- base/includes
- base/index
- base/map
- base/reduce
- base/set
- base/type

## ruby style
- rubify/times
- rubify/to_a
- rubify/to_b
- rubify/to_f
- rubify/to_i
- rubify/to_n
- rubify/to_s

## next packages
- days
- qs
- [tmpl](https://js.work/posts/34ef06b7870ec)

## next classes
+ date
  - format 
  - now 
  - create
+ fileutils
  - mkdir_p
  - cd
  - pwd
  - ls
  - rmdir
  - touch
  - cp_r
  - isfile
  - isdir
  - exists
+ tar
  - gz
  - xz
+ [JSON](https://js.work/posts/3dc24683e53c4)
  - parse
  - stringify