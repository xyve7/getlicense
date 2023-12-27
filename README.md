# getlicense
Python script which retrieves the requested license.

# Usage
## Prerequisites
Create a GitHub token and set the environment variable: `GITHUB_API_TOKEN` to the token.
Example:  
```
~/.bashrc 
export GITHUB_API_TOKEN="MY_GITHUB_API_TOKEN"
```
Restart your shell after this.
## Basic Usage
The script works as follows:  
```bash
$ getlicense --license [LICENSE] --path [PATH] --year [YEAR] --name [NAME]
```
For the sake of being concise, the arguments can be written in their short form:  

```bash
$ getlicense -l [LICENSE] -p [PATH] -y [YEAR] -n [NAME]
```
Here are the default values for all of the arguments:  

| Argument    | Default        |
|-------------|----------------|
| license, l  | none, required |
| path, p     | stdout         |
| year, y     | current year   |
| name, n     | "John Doe"     |

### Other features
To obtain a list of the most commonly used licenses, run:
```bash
$ getlicense list
```
**NOTE**: This is not an exhaustive list of all of the possible licenses which GitHub provides, only the commonly used ones.  
## Note

For indepth documentation, access the help page:  
```bash
$ getlicense -h 
```
