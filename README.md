## Testing

### py.tests in docker

`make build` - builds new image tagged with **dasigraphservice:testing**

configure pycharm to use a remote docker python interpreter (image: dasigraphservice:testing)

you can configure pycharm to run tests

if you're getting weird import errors, run `make clean` to remove the __pycache__ for pytests