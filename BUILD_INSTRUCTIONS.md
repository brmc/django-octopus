# Instructions for building the javascript libraries

Any js development should be done in `js/` rather than directly in   
`octopus/static/octopus`. The build commands should be used to install  
it in the appropriate places.

## Dependencies:

* node
* npm
* browserify
* jquery-builder

### For the lazy:
 (debian-flavored linux only)

    sudo apt-get install nodejs nodejs-legacy npm
    sudo npm install n
    sudo n stable
    sudo npm install browserify jquery-builder
    
## Build commands
 
Look in package.json for the most up-to-date list

|command         |purpose|  
|:--|:--|
| build          | installs the js library into the python package |
| build-test     | runs `collectstatic` from within `tests` |
| build-all      | runs `build` and `build-test` |
| build-jquery   | custom builds jquery with the minimum required components: ajax, css, effects, and events |
| install-jquery | installs jquery into the python package |

#### tip: set up a file watcher to automatically run build-all as you  
code   

For pycharm users: https://www.jetbrains.com/help/pycharm/2016.3/file-watchers.html