# SemVer

Semver is a library that accepts a list of Semantic Versions.  
Versions are then sorted according to Semantic Versioning 1.0 and 2.0 specifications.  
Sorted versions are returned as a list of lists. Nested lists are provided because according to specifications a version core is the same as a version core with build. It means that if user is looking for a specific version, user may have to choose between different builds.  

Semver triggers a custom exception if a version from the provided list does not match Semantic Versioning regex.  
Semver offers mutiple options to filter the results for instance duplicates may be removed. The list of lists can be flattened to a single list. A dictionary can be returned instead of a version for each version provided. The version dictionary contains all the regex groups.  

Use `tests.py` to test Semantic Versioning specifications.  
Use `samples.py` to try SemVer functionalities.  
