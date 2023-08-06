# Image Toolkit

This is the READ ME.

## Basic Usage

```
from imgtoolkit import tools

if __name__ == '__main__':
  # Find blur photos
	tools.find_blur()

  # Find duplicated photos
	tools.find_duplicate()
```


## Sample Output

```
Start finding blurs
|████████████████████████████████████████| 12148/12148 [100%] in 18:38.0 (10.87/s)
11 blur photos processed, moved to blur/
Elapsed Time:  0:18:38.067728
Start finding duplicates
Phase 1 - Hashing
|████████████████████████████████████████| 12137/12137 [100%] in 2:25.1 (83.63/s)
Phase 2 - Find Duplicates
Phase 3 - Move Duplicates
93 duplicated images moved to duplicate/
```
