# gha-csp
This repo serve as a test for auto-generate png for csp-11

To have your result generated please clone develop and add your results and push to it

``` bash
  git clone https://github.com/jafranc/gha-csp -b develop
  cp /path/to/sparse/spe/a/spe11a_time_series.csv ./groupA/a/sparse/
  git add ./groupA/a/sparse/spe11a_time_series.csv
  cp /path/to/sparse/spe/a/spe11a_map_*.csv ./groupA/a/dense/
  git add ./groupA/a/dense/spe11a_map_*.csv
  git commit -m 'adding results for spe11a'
  git push 
```

Once pushed the CI checks should generate *png* leveraging the scripts in *script* and commiting them to _a/sparse_ and _a/dense_ branches respectively. It should also merge back those to develop in _groupA/a/sparse/illustrations_ and _groupA/a/dense/illustrations_. The generated *png*s will still be accessible on the intermediate branches _a/sparse_ and _a/dense_.

_main_ branch is locked and admin-mergeable only.
